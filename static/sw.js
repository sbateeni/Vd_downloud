self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('ytd-store').then((cache) => {
      return cache.addAll([
        '/',
        '/static/style.css',
        '/static/script.js',
      ]);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
}); 