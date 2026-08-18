// Cache version - increment on each deploy
const CACHE_VERSION = '20260818-v42-techflow817';

const CACHE_NAME = 'finance-dashboard-v2-' + CACHE_VERSION;
const ASSETS = [
  './index.html', './manifest.json', './chart.umd.min.js', './html2canvas.min.js',
  './echarts.common.min.js', './fonts/JetBrainsMono-Regular.woff2', './fonts/JetBrainsMono-Bold.woff2'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))));
  self.clients.claim();
});
// Network-first for HTML (always fresh), cache-first for static assets
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname.endsWith('/')) {
    e.respondWith(fetch(e.request).then(r => {
      const clone = r.clone();
      caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
      return r;
    }).catch(() => caches.match(e.request)));
  } else {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(resp => {
      const clone = resp.clone();
      caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
      return resp;
    })));
  }
});
