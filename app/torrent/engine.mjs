import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import WebTorrent from './node_modules/webtorrent/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const APP_DIR = path.resolve(__dirname, '..');
const ROOT_DIR = path.resolve(APP_DIR, '..');
const localAppData = process.env.LOCALAPPDATA || process.env.APPDATA || path.join(APP_DIR, 'data');
const CACHE_DIR = path.join(localAppData, 'CineLocal', 'torrent_cache');

if (!fs.existsSync(CACHE_DIR)) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
}

const PORT = parseInt(process.env.TORRENT_PORT || '8888', 10);
const HOST = '0.0.0.0';

const DEFAULT_TRACKERS = [
  'udp://tracker.opentrackr.org:1337/announce',
  'udp://open.stealth.si:80/announce',
  'udp://tracker.torrent.eu.org:451/announce',
  'udp://explodie.org:6969/announce',
  'udp://tracker.coppersurfer.tk:6969/announce',
  'wss://tracker.openwebtorrent.com',
  'wss://tracker.webtorrent.dev',
  'wss://tracker.btorrent.xyz'
];

const client = new WebTorrent();
const torrentServer = client.createServer({ pathname: '/webtorrent' });

// Mapa de múltiplos torrents ativos (Issue #18)
const torrentsMap = new Map();

function formatBytes(bytes, decimals = 2) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

const VIDEO_EXTENSIONS = new Set(['.mp4', '.mkv', '.avi', '.webm', '.m4v', '.ts', '.mov', '.wmv']);

function isVideoFile(fileName) {
  const ext = path.extname(fileName || '').toLowerCase();
  return VIDEO_EXTENSIONS.has(ext);
}

function getTorrentEntryStatus(item) {
  const t = item.torrent;
  const progress = t ? (t.progress || 0) : item.progress || 0;
  const downloadSpeed = t ? (t.downloadSpeed || 0) : 0;
  const uploadSpeed = t ? (t.uploadSpeed || 0) : 0;
  const numPeers = t ? (t.numPeers || 0) : 0;
  const downloaded = t ? (t.downloaded || 0) : 0;
  const total = t ? (t.length || 0) : 0;

  const files = (t && t.files ? t.files : []).map((f, idx) => ({
    index: idx,
    name: f.name,
    path: f.path.replace(/\\/g, '/'),
    length: f.length,
    lengthFormatted: formatBytes(f.length),
    isVideo: isVideoFile(f.name),
    isMkv: f.name.toLowerCase().endsWith('.mkv'),
    streamUrl: `/webtorrent/${t.infoHash}/${encodeURIComponent(f.path.replace(/\\/g, '/'))}`
  }));

  let videoFile = null;
  if (files.length > 0) {
    const videoFiles = files.filter(f => f.isVideo);
    videoFile = videoFiles.length > 0 ? videoFiles[0] : files[0];
  }

  const isMkv = videoFile ? videoFile.isMkv : false;
  const streamUrl = videoFile ? videoFile.streamUrl : (t && t.infoHash ? /webtorrent/ : '');
  const initialBufferReady = downloaded >= 2 * 1024 * 1024 || progress >= 0.005 || (item.ready && downloaded > 500 * 1024);

  return {
    infoHash: item.infoHash,
    name: item.name || (t ? t.name : '') || 'Torrent',
    title: item.title || item.name || (t ? t.name : '') || 'Torrent',
    year: item.year || '',
    poster: item.poster || '',
    overview: item.overview || '',
    imdbId: item.imdbId || '',
    active: !t ? false : !t.paused,
    ready: item.ready,
    initialBufferReady: initialBufferReady,
    downloadSpeed: downloadSpeed,
    uploadSpeed: uploadSpeed,
    downloadSpeedFormatted: formatBytes(downloadSpeed) + '/s',
    uploadSpeedFormatted: formatBytes(uploadSpeed) + '/s',
    progress: progress,
    progressPercent: (progress * 100).toFixed(1) + '%',
    numPeers: numPeers,
    downloaded: downloaded,
    downloadedFormatted: formatBytes(downloaded),
    total: total,
    totalFormatted: formatBytes(total),
    timeRemaining: t ? t.timeRemaining : 0,
    files: files,
    videoFile: videoFile,
    isMkv: isMkv,
    streamUrl: streamUrl,
    vlcUrl: streamUrl ? `http://localhost:${PORT}${streamUrl}` : '',
    piecesTotal: t && t.pieces ? t.pieces.length : 0,
    error: item.error || null,
    addedAt: item.addedAt
  };
}

function getAllTorrentsStatus() {
  const list = [];
  let totalSpeed = 0;
  for (const item of torrentsMap.values()) {
    const s = getTorrentEntryStatus(item);
    totalSpeed += s.downloadSpeed;
    list.push(s);
  }
  // Ordena por data de adição (mais recente primeiro)
  list.sort((a, b) => (b.addedAt || 0) - (a.addedAt || 0));

  return {
    activeCount: list.filter(i => i.active).length,
    totalCount: list.length,
    totalDownloadSpeedFormatted: formatBytes(totalSpeed) + '/s',
    torrents: list
  };
}

function addTorrent(torrentId, title = '', year = '', poster = '', overview = '', imdbId = '') {
  return new Promise((resolve, reject) => {
    try {
      const opts = {
        path: CACHE_DIR,
        destroyStoreOnDestroy: false,
        announce: DEFAULT_TRACKERS
      };

      const torrent = client.add(torrentId, opts);
      const infoHash = torrent.infoHash;

      let item = torrentsMap.get(infoHash);
      if (!item) {
        item = {
          infoHash: infoHash,
          name: title || 'Carregando metadados...',
          title: title,
          year: year,
          poster: poster,
          overview: overview,
          imdbId: imdbId,
          torrent: torrent,
          ready: false,
          error: null,
          addedAt: Date.now()
        };
        torrentsMap.set(infoHash, item);
      } else {
        item.torrent = torrent;
        if (title) item.title = title;
        if (year) item.year = year;
        if (poster) item.poster = poster;
        if (overview) item.overview = overview;
      }

      torrent.on('infoHash', () => {
        item.infoHash = torrent.infoHash;
      });

      torrent.on('metadata', () => {
        item.name = torrent.name;
        if (!item.title || item.title === 'Carregando metadados...') {
          item.title = torrent.name;
        }
        item.ready = true;
      });

      torrent.on('ready', () => {
        item.ready = true;
        item.name = torrent.name;
        if (!item.title) item.title = torrent.name;

        // Identifica melhor arquivo de vídeo
        let bestIdx = 0;
        let maxLen = -1;
        torrent.files.forEach((f, idx) => {
          if (isVideoFile(f.name) && f.length > maxLen) {
            maxLen = f.length;
            bestIdx = idx;
          }
        });

        // Seleciona arquivo de vídeo principal
        if (torrent.files[bestIdx]) {
          try {
            torrent.files[bestIdx].select();
          } catch (e) {}
        }

        // Prioridade máxima nas peças iniciais para buffer instantâneo (sem deselect para não parar o download)
        if (torrent.pieces && torrent.pieces.length > 0) {
          const headPieces = Math.min(30, torrent.pieces.length - 1);
          try {
            torrent.critical(0, headPieces);
          } catch (e) {}

          const tailPieces = Math.max(0, torrent.pieces.length - 15);
          try {
            torrent.critical(tailPieces, torrent.pieces.length - 1);
          } catch (e) {}
        }

        console.log(`[Torrent Ready] "${torrent.name}" (${formatBytes(torrent.length)}) - Arquivo principal: "${torrent.files[bestIdx]?.name}"`);
      });

      torrent.on('error', (err) => {
        console.error(`[Torrent Error] ${infoHash}:`, err);
        item.error = err.message || String(err);
      });

      resolve({
        success: true,
        message: 'Torrent adicionado à fila de downloads',
        infoHash: torrent.infoHash,
        title: item.title
      });
    } catch (err) {
      console.error('Erro ao adicionar torrent:', err);
      reject(err);
    }
  });
}

function removeTorrent(infoHash, deleteCache = false) {
  return new Promise((resolve) => {
    const item = torrentsMap.get(infoHash);
    if (!item) {
      return resolve({ success: true, message: 'Torrent não encontrado na fila' });
    }

    // Remove imediatamente da fila para atualização instantânea da interface
    torrentsMap.delete(infoHash);

    try {
      if (item.torrent) {
        item.torrent.destroy({ destroyStore: false }, () => {
          if (deleteCache && item.name) {
            setTimeout(() => {
              try {
                const cacheFolder = path.join(CACHE_DIR, item.name);
                if (fs.existsSync(cacheFolder)) {
                  fs.rmSync(cacheFolder, { recursive: true, force: true });
                }
              } catch (e) {}
            }, 600);
          }
        });
      }
    } catch (e) {
      try { client.remove(infoHash); } catch (e2) {}
    }

    resolve({ success: true, message: 'Torrent removido com sucesso' });
  });
}

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Range, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  // Roteamento WebTorrent (Range Requests HTTP 206)
  if (pathname.startsWith('/webtorrent')) {
    return torrentServer.wrapRequest(req, res);
  }

  // API: Listar Todos os Torrents (Multi-Torrent Issue #18)
  if (pathname === '/api/torrent/list' && req.method === 'GET') {
    const list = getAllTorrentsStatus();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(list));
    return;
  }

  // API: Status de um torrent específico ou ativo
  if (pathname === '/api/torrent/status' && req.method === 'GET') {
    const infoHash = url.searchParams.get('infoHash');
    let item = null;
    if (infoHash && torrentsMap.has(infoHash)) {
      item = torrentsMap.get(infoHash);
    } else if (torrentsMap.size > 0) {
      // Retorna o mais recente
      item = Array.from(torrentsMap.values()).pop();
    }

    if (!item) {
      const empty = { active: false, ready: false, name: '', infoHash: '', title: '', downloadSpeedFormatted: '0 B/s', progressPercent: '0.0%', numPeers: 0, files: [], videoFile: null, streamUrl: '' };
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(empty));
      return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(getTorrentEntryStatus(item)));
    return;
  }

  // API: Iniciar/Adicionar Torrent
  if (pathname === '/api/torrent/start' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const magnet = data.magnet || data.torrentUrl || data.url;
        const title = data.title || '';
        const year = data.year || '';
        const poster = data.poster || '';
        const overview = data.overview || '';
        const imdbId = data.imdbId || '';

        if (!magnet) {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Magnet link não fornecido' }));
          return;
        }

        const result = await addTorrent(magnet, title, year, poster, overview, imdbId);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // API: Remover Torrent da fila
  if ((pathname === '/api/torrent/remove' || pathname === '/api/torrent/stop') && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const infoHash = data.infoHash;
        const deleteCache = Boolean(data.deleteCache);

        if (infoHash) {
          const result = await removeTorrent(infoHash, deleteCache);
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify(result));
        } else {
          // Remove todos
          for (const hash of Array.from(torrentsMap.keys())) {
            await removeTorrent(hash, deleteCache);
          }
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, message: 'Todos os torrents encerrados' }));
        }
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // API: Salvar na Coleção Permanente
  if (pathname === '/api/torrent/save' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const infoHash = data.infoHash;
        let item = infoHash ? torrentsMap.get(infoHash) : Array.from(torrentsMap.values()).pop();

        if (!item || !item.torrent) {
          res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Torrent não encontrado para salvar' }));
          return;
        }

        const title = data.title || item.title || item.name || 'Filme Torrent';
        const year = data.year || item.year || '';
        const folderName = year ? `${title} (${year})` : title;
        const safeFolderName = folderName.replace(/[<>:"/\\|?*]/g, '').trim();

        const destDir = path.join(ROOT_DIR, 'media', 'filmes', safeFolderName);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }

        // Procura arquivo de vídeo
        const t = item.torrent;
        const videoFiles = (t.files || []).filter(f => isVideoFile(f.name));
        const vFile = videoFiles.length > 0 ? videoFiles[0] : (t.files && t.files[0]);

        if (!vFile) {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Nenhum arquivo de vídeo encontrado' }));
          return;
        }

        const ext = path.extname(vFile.name) || '.mp4';
        const finalFilePath = path.join(destDir, `${safeFolderName}${ext}`);
        const cacheFilePath = path.join(CACHE_DIR, vFile.path);

        if (fs.existsSync(cacheFilePath)) {
          fs.copyFileSync(cacheFilePath, finalFilePath);
          console.log(`[Torrent Save] Salvo em "${finalFilePath}"`);
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({
            success: true,
            message: `Filme salvo com sucesso em media/filmes/${safeFolderName}/`,
            savedPath: finalFilePath
          }));
        } else {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({
            success: false,
            error: 'Arquivo ainda não foi suficientemente baixado no disco para ser copiado'
          }));
        }
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // Health
  if (pathname === '/api/torrent/health' || pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ status: 'ok', version: '2.5.0', engine: 'WebTorrent Multi', count: torrentsMap.size }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('CineLocal Multi-Torrent Engine');
});

server.listen(PORT, HOST, () => {
  console.log(`🚀 CineLocal Multi-Torrent Engine ativo na porta ${PORT}`);
});
