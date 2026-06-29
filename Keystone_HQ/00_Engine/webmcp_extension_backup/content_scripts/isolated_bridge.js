/**
 * Keystone WebMCP Isolated Bridge Content Script
 * Runs in the default ISOLATED world.
 * Bridges messages between service_worker.js and google_flow.js (MAIN world).
 */
(function() {
    console.log("WebMCP: Isolated Bridge Content Script loaded.");

    // Store callbacks for messages waiting on responses from MAIN world script
    const pendingCallbacks = new Map();

    // 1. Listen for messages from background service worker
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log("WebMCP: Isolated bridge received message from background worker:", message);

        const requestId = Math.random().toString(36).substring(2, 11);
        pendingCallbacks.set(requestId, sendResponse);

        // Forward command to MAIN world content script
        window.postMessage({
            source: 'WEBMCP_BACKGROUND',
            type: 'WEBMCP_TO_MAIN',
            payload: {
                ...message,
                id: requestId
            }
        }, '*');

        // Return true to keep message channel open for asynchronous sendResponse
        return true;
    });

    // 2. Listen for messages from MAIN world page script
    window.addEventListener("message", function(event) {
        // Only trust messages from our window
        if (event.source !== window) return;

        const data = event.data;
        if (!data || typeof data !== 'object') return;

        // Message type A: Response to background command
        if (data.source === 'WEBMCP_MAIN' && data.type === 'WEBMCP_FROM_MAIN_RESPONSE') {
            const { id, result } = data;
            const sendResponse = pendingCallbacks.get(id);
            if (sendResponse) {
                console.log(`WebMCP: Resolving callback for request ${id} with result:`, result);
                sendResponse(result);
                pendingCallbacks.delete(id);
            }
        }

        // Message type B: Proactive payload to background worker (e.g. download or credits status)
        if (data.source === 'WEBMCP_MAIN' && data.type === 'WEBMCP_TO_BACKGROUND') {
            console.log("WebMCP: Isolated bridge forwarding payload to background worker:", data.payload);
            chrome.runtime.sendMessage(data.payload);
        }
    });
})();
