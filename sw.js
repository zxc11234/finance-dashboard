// Cache version - increment on each deploy
const CACHE_VERSION = '20260718-v2-local-js';

const CACHE_NAME = 'finance-dashboard-v2-' + CACHE_VERSION;
const ASSETS = ['./index.html', './manifest.json', './chart.umd.min.js', './html2canvas.min.js'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
