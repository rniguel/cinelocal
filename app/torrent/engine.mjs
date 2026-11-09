import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import WebTorrent from './node_modules/webtorrent/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const APP_DIR = path.resolve(__dirname, '..');
const ROOT_DIR = path.resolve(APP_DIR, '..');
const CACHE_DIR = path.join(APP_DIR, 'data', 'torrent_cache');

// Garante que o diretório de cache exista
if (!fs.existsSync(CACHE_DIR)) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
}

const PORT = parseInt(process.env.TORRENT_PORT || '8888', 10);
const HOST = '0.0.0.0';

let client = new WebTorrent();
let torrentServer = client.createServer({ pathname: '/webtorrent' });

let currentTorrent = null;
let currentMetadata = {
  active: false,
  ready: false,
  name: '',
  infoHash: '',
  title: '',
  year: '',
  error: null,
  videoFileIndex: 0,
  cachePath: ''
};

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

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

const VIDEO_EXTENSIONS = new Set(['.mp4', '.mkv', '.avi', '.webm', '.m4v', '.ts', '.mov', '.wmv']);

function isVideoFile(fileName) {
  const ext = path.extname(fileName).toLowerCase();
  return VIDEO_EXTENSIONS.has(ext);
}

function getTorrentStatus() {
  if (!currentTorrent) {
    return {
      active: false,
      ready: false,
      name: '',
      infoHash: '',
      title: currentMetadata.title || '',
      downloadSpeed: 0,
      uploadSpeed: 0,
      downloadSpeedFormatted: '0 KB/s',
      uploadSpeedFormatted: '0 KB/s',
      progress: 0,
      progressPercent: '0.0%',
      numPeers: 0,
      downloaded: 0,
      downloadedFormatted: '0 B',
      total: 0,
      totalFormatted: '0 B',
      timeRemaining: 0,
      files: [],
      videoFile: null,
      streamUrl: '',
      error: currentMetadata.error
    };
  }

  const t = currentTorrent;
  const files = (t.files || []).map((f, idx) => ({
    index: idx,
    name: f.name,
    path: f.path.replace(/\\/g, '/'),
    length: f.length,
    lengthFormatted: formatBytes(f.length),
    isVideo: isVideoFile(f.name),
    streamUrl: `/webtorrent/${t.infoHash}/${encodeURIComponent(f.path.replace(/\\/g, '/'))}`
  }));

  let videoFile = null;
  if (files.length > 0) {
    if (files[currentMetadata.videoFileIndex] && files[currentMetadata.videoFileIndex].isVideo) {
      videoFile = files[currentMetadata.videoFileIndex];
    } else {
      const videoFiles = files.filter(f => f.isVideo);
      videoFile = videoFiles.length > 0 ? videoFiles[0] : files[0];
    }
  }

  const progress = t.progress || 0;
  return {
    active: true,
    ready: currentMetadata.ready,
    name: t.name || currentMetadata.name || '',
    infoHash: t.infoHash || '',
    title: currentMetadata.title || t.name || '',
    year: currentMetadata.year || '',
    downloadSpeed: t.downloadSpeed || 0,
    uploadSpeed: t.uploadSpeed || 0,
    downloadSpeedFormatted: formatBytes(t.downloadSpeed || 0) + '/s',
    uploadSpeedFormatted: formatBytes(t.uploadSpeed || 0) + '/s',
    progress: progress,
    progressPercent: (progress * 100).toFixed(1) + '%',
    numPeers: t.numPeers || 0,
    downloaded: t.downloaded || 0,
    downloadedFormatted: formatBytes(t.downloaded || 0),
    total: t.length || 0,
    totalFormatted: formatBytes(t.length || 0),
    timeRemaining: t.timeRemaining || 0,
    files: files,
    videoFile: videoFile,
    streamUrl: videoFile ? videoFile.streamUrl : '',
    piecesTotal: t.pieces ? t.pieces.length : 0,
    error: currentMetadata.error
  };
}

function stopCurrentTorrent(deleteCache = false) {
  return new Promise((resolve) => {
    if (!currentTorrent) {
      currentMetadata = { active: false, ready: false, name: '', infoHash: '', title: '', year: '', error: null, videoFileIndex: 0, cachePath: '' };
      return resolve({ success: true, message: 'Nenhum torrent em execução' });
    }

    const t = currentTorrent;
    const infoHash = t.infoHash;
    const torrentPath = currentMetadata.cachePath;

    try {
      client.remove(t.infoHash, { destroyStore: deleteCache }, (err) => {
        currentTorrent = null;
        currentMetadata = { active: false, ready: false, name: '', infoHash: '', title: '', year: '', error: null, videoFileIndex: 0, cachePath: '' };
        if (err) console.error('Erro ao remover torrent:', err);

        if (deleteCache && torrentPath && fs.existsSync(torrentPath)) {
          try {
            fs.rmSync(torrentPath, { recursive: true, force: true });
          } catch (e) {
            console.error('Erro ao limpar cache de torrent:', e);
          }
        }
        resolve({ success: true, message: 'Torrent encerrado com sucesso' });
      });
    } catch (e) {
      currentTorrent = null;
      currentMetadata = { active: false, ready: false, name: '', infoHash: '', title: '', year: '', error: null, videoFileIndex: 0, cachePath: '' };
      resolve({ success: true, message: 'Torrent encerrado' });
    }
  });
}

function startTorrent(torrentId, title = '', year = '') {
  return new Promise((resolve, reject) => {
    // Para qualquer torrent em execução anterior
    stopCurrentTorrent(false).then(() => {
      currentMetadata = {
        active: true,
        ready: false,
        name: title || 'Carregando metadados...',
        infoHash: '',
        title: title,
        year: year,
        error: null,
        videoFileIndex: 0,
        cachePath: ''
      };

      try {
        const opts = {
          path: CACHE_DIR,
          destroyStoreOnDestroy: false,
          announce: DEFAULT_TRACKERS
        };

        const torrent = client.add(torrentId, opts);
        currentTorrent = torrent;
        currentMetadata.infoHash = torrent.infoHash;

        torrent.on('infoHash', () => {
          currentMetadata.infoHash = torrent.infoHash;
        });

        torrent.on('metadata', () => {
          currentMetadata.name = torrent.name;
          currentMetadata.cachePath = path.join(CACHE_DIR, torrent.name || torrent.infoHash);
        });

        torrent.on('ready', () => {
          currentMetadata.ready = true;
          currentMetadata.name = torrent.name;
          currentMetadata.cachePath = path.join(CACHE_DIR, torrent.name || torrent.infoHash);

          // Identifica o arquivo de vídeo principal (maior arquivo de vídeo)
          let bestVideoIdx = 0;
          let maxLen = -1;
          torrent.files.forEach((f, idx) => {
            if (isVideoFile(f.name) && f.length > maxLen) {
              maxLen = f.length;
              bestVideoIdx = idx;
            }
          });
          currentMetadata.videoFileIndex = bestVideoIdx;

          // Configuração de Streaming Sequencial com Janela Deslizante (Issue #16):
          // 1. Desmarca o download completo não-sequencial para economizar banda
          if (torrent.pieces && torrent.pieces.length > 0) {
            try {
              torrent.deselect(0, torrent.pieces.length - 1);
            } catch (e) {
              console.warn('Deselect pieces warning:', e.message);
            }

            // 2. Prioridade Máxima (Critical): Primeiras 15 peças (cabeçalhos de container e índices de áudio)
            const headPieces = Math.min(15, torrent.pieces.length - 1);
            try {
              torrent.critical(0, headPieces);
            } catch (e) {
              console.warn('Critical head pieces warning:', e.message);
            }

            // 3. Prioridade Alta: Últimas 10 peças (átomo 'moov' / índice de seek MP4/MKV)
            const tailPieces = Math.max(0, torrent.pieces.length - 10);
            try {
              torrent.critical(tailPieces, torrent.pieces.length - 1);
            } catch (e) {
              console.warn('Critical tail pieces warning:', e.message);
            }

            // 4. Seleciona o arquivo de vídeo principal
            if (torrent.files[bestVideoIdx]) {
              try {
                torrent.files[bestVideoIdx].select();
              } catch (e) {
                console.warn('Select video file warning:', e.message);
              }
            }
          }

          console.log(`[Torrent Ready] "${torrent.name}" (${formatBytes(torrent.length)}) - Arquivo: "${torrent.files[bestVideoIdx]?.name}"`);
        });

        torrent.on('error', (err) => {
          console.error('[Torrent Error]', err);
          currentMetadata.error = err.message || String(err);
        });

        resolve({
          success: true,
          message: 'Torrent iniciado com sucesso',
          infoHash: torrent.infoHash,
          title: title
        });
      } catch (err) {
        console.error('Erro ao adicionar torrent:', err);
        currentMetadata.error = err.message;
        reject(err);
      }
    });
  });
}

const server = http.createServer((req, res) => {
  // CORS Headers universais
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

  // Roteamento para streaming de vídeo WebTorrent
  if (pathname.startsWith('/webtorrent')) {
    return torrentServer.wrapRequest(req, res);
  }

  // API: Status
  if (pathname === '/api/torrent/status' && req.method === 'GET') {
    const status = getTorrentStatus();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(status));
    return;
  }

  // API: Iniciar Torrent
  if (pathname === '/api/torrent/start' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const magnet = data.magnet || data.torrentUrl || data.url;
        const title = data.title || '';
        const year = data.year || '';

        if (!magnet) {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Magnet link não fornecido' }));
          return;
        }

        const result = await startTorrent(magnet, title, year);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // API: Parar Torrent
  if (pathname === '/api/torrent/stop' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const deleteCache = Boolean(data.deleteCache);
        const result = await stopCurrentTorrent(deleteCache);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // API: Salvar na Coleção Permanente (Issue #16)
  if (pathname === '/api/torrent/save' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const title = data.title || (currentTorrent && currentTorrent.name) || 'Filme Torrent';
        const year = data.year || '';
        const folderName = year ? `${title} (${year})` : title;
        const safeFolderName = folderName.replace(/[<>:"/\\|?*]/g, '').trim();

        const destDir = path.join(ROOT_DIR, 'media', 'filmes', safeFolderName);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }

        const status = getTorrentStatus();
        if (!status.videoFile) {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Nenhum arquivo de vídeo encontrado no torrent' }));
          return;
        }

        // Procura o arquivo no cache do torrent
        const currentFile = currentTorrent ? currentTorrent.files[currentMetadata.videoFileIndex] : null;
        if (!currentFile) {
          res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Arquivo do torrent não acessível' }));
          return;
        }

        const ext = path.extname(currentFile.name) || '.mp4';
        const finalFileName = `${safeFolderName}${ext}`;
        const finalFilePath = path.join(destDir, finalFileName);

        // Caminho na pasta de cache
        const cacheFilePath = path.join(CACHE_DIR, currentFile.path);

        if (fs.existsSync(cacheFilePath)) {
          // Copia ou move o arquivo baixado
          fs.copyFileSync(cacheFilePath, finalFilePath);
          console.log(`[Torrent Save] Arquivo salvo em "${finalFilePath}"`);
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
            error: 'Arquivo ainda não foi completamente baixado para o disco'
          }));
        }
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // Rota de Health Check
  if (pathname === '/api/torrent/health' || pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ status: 'ok', version: '2.5.0', engine: 'WebTorrent' }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('CineLocal Torrent Engine - Rota não encontrada');
});

server.listen(PORT, HOST, () => {
  console.log(`=======================================================`);
  console.log(`🚀 CineLocal Torrent Streaming Engine rodando em:`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   Stream endpoint: http://localhost:${PORT}/webtorrent/`);
  console.log(`   Cache dir: ${CACHE_DIR}`);
  console.log(`=======================================================`);
});

// Finalização limpa ao receber sinais de encerramento
process.on('SIGINT', () => {
  console.log('Encerrando Torrent Engine...');
  stopCurrentTorrent(false).then(() => {
    client.destroy(() => {
      server.close(() => process.exit(0));
    });
  });
});

process.on('SIGTERM', () => {
  console.log('Encerrando Torrent Engine...');
  stopCurrentTorrent(false).then(() => {
    client.destroy(() => {
      server.close(() => process.exit(0));
    });
  });
});
