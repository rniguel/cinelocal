// CineLocal Service Worker - Cache-Free & Always Live
const CACHE_NAME = 'cinelocal-live-v6';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.claim())
      .then(() => {
        // Notifica todas as janelas para recarregar se necessário
        return self.clients.matchAll({ type: 'window' }).then(clients => {
          clients.forEach(c => c.postMessage({ action: 'force-reload' }));
        });
      })
  );
});

self.addEventListener('fetch', (event) => {
  // Always fetch fresh network copies for HTML, JS and JSON to ensure TV is always updated
  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).catch(() => caches.match(event.request))
  );
});

