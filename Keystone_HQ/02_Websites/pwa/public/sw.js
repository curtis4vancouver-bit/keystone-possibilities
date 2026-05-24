const CACHE_NAME = 'keystone-v1';
const OFFLINE_URL = '/offline';

// Core shell files to cache on install
const PRECACHE_URLS = [
  '/offline',
];

// Install: cache the offline page
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS);
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch: network-first strategy with offline fallback
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip Supabase/API requests
  if (event.request.url.includes('supabase.co')) return;
  if (event.request.url.includes('/api/')) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache successful responses for static assets
        if (response.status === 200 && (
          event.request.url.includes('/_next/static/') ||
          event.request.url.includes('/icon-') ||
          event.request.url.endsWith('.css') ||
          event.request.url.endsWith('.js')
        )) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, clone);
          });
        }
        return response;
      })
      .catch(() => {
        // If offline and it's a navigation request, show offline page
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        // Otherwise try cached version
        return caches.match(event.request);
      })
  );
});

// Push notification listeners for system tradesmen notifications
self.addEventListener('push', (event) => {
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { title: 'Keystone Notification', body: event.data.text() };
    }
  }

  const title = data.title || 'Keystone Update';
  const options = {
    body: data.body || 'New operational update is available.',
    icon: '/icon-512.png',
    badge: '/icon-512.png', // Fallback to icon for high contrast
    data: data.data || {}
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((clientList) => {
      for (const client of clientList) {
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});

