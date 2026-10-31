// Service worker JuriLex.
//
// Met en cache UNIQUEMENT les ressources statiques de l'interface (app shell).
// Ne met JAMAIS en cache les données sensibles : documents importés, textes
// extraits, explications, traductions, fichiers audio (cf. §6.6 du cahier
// des charges). Toute requête vers /api/ est ignorée.

const CACHE_NAME = 'jurilex-static-v1'
const PRECACHE = ['/', '/index.html', '/manifest.webmanifest', '/icon-192.png', '/icon-512.png']

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url)

  // Ne jamais intercepter ni mettre en cache les appels à l'API (données sensibles).
  if (url.pathname.startsWith('/api/')) {
    return
  }
  // Seules les requêtes GET vers des ressources statiques sont mises en cache.
  if (event.request.method !== 'GET') {
    return
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetched = fetch(event.request)
        .then((response) => {
          if (response && response.status === 200 && url.origin === self.location.origin) {
            const copy = response.clone()
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy))
          }
          return response
        })
        .catch(() => cached)
      return cached || fetched
    })
  )
})
