self.addEventListener('install', function(event) {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', function(event) {
    var payload = {};
    if (event.data) {
        try {
            payload = event.data.json();
        } catch (e) {
            payload = { body: event.data.text() };
        }
    }

    var title = payload.title || 'Уведомление';
    var options = {
        body: payload.body || '',
        icon: payload.icon,
        badge: payload.badge,
        data: payload.data || {},
        actions: payload.actions || []
    };
    
    // Ensure data.url exists if payload.url is present
    if (payload.url && !options.data.url) {
        options.data.url = payload.url;
    }

    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
    var data = event.notification && event.notification.data ? event.notification.data : {};
    var actionUrls = data.action_urls || {};
    var url = data.url || '/';
    var actionUrl = event.action ? actionUrls[event.action] : null;

    event.notification.close();

    event.waitUntil((async function() {
        if (actionUrl) {
            try {
                await fetch(actionUrl, { method: 'POST', credentials: 'include' });
                return;
            } catch (e) {
            }
        }

        var clientsList = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
        for (var i = 0; i < clientsList.length; i++) {
            var client = clientsList[i];
            if ('focus' in client) {
                client.navigate(url);
                return client.focus();
            }
        }
        if (self.clients.openWindow) {
            return self.clients.openWindow(url);
        }
    })());
});
