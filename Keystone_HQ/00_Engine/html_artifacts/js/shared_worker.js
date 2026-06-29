/**
 * Chronos Multi-Screen WebSocket Shared Worker
 * Coordinates socket frames across multiple browser tabs / screens (Screen 1 & Screen 2)
 * using a single background connection to eliminate socket exhaustion.
 */

const ports = new Set();
let socket = null;
let reconnectTimer = null;

// WebSocket connection parameters
const WS_URL = "ws://127.0.0.1:8000/ws/central";

function connectWebSocket() {
    if (socket && (socket.readyState === WebSocket.CONNECTING || socket.readyState === WebSocket.OPEN)) {
        return;
    }

    console.log("[SharedWorker] Establishing central WebSocket connection...");
    socket = new WebSocket(WS_URL);

    socket.onopen = () => {
        console.log("[SharedWorker] WebSocket successfully connected.");
        broadcast({ type: "connection_status", status: "connected" });
        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
            reconnectTimer = null;
        }
    };

    socket.onmessage = (event) => {
        try {
            const payload = JSON.parse(event.data);
            console.log("[SharedWorker] Broadcast incoming payload: ", payload);
            broadcast({ type: "server_message", data: payload });
        } catch (e) {
            console.error("[SharedWorker] JSON parse failure: ", event.data);
        }
    };

    socket.onclose = () => {
        console.warn("[SharedWorker] WebSocket connection lost. Reconnecting in 3s...");
        broadcast({ type: "connection_status", status: "disconnected" });
        socket = null;
        reconnectTimer = setTimeout(connectWebSocket, 3000);
    };

    socket.onerror = (error) => {
        console.error("[SharedWorker] WebSocket exception encountered: ", error);
    };
}

function broadcast(message) {
    const msgStr = JSON.stringify(message);
    for (const port of ports) {
        try {
            port.postMessage(msgStr);
        } catch (e) {
            ports.delete(port);
        }
    }
}

self.onconnect = (e) => {
    const port = e.ports[0];
    ports.add(port);
    console.log(`[SharedWorker] Client connected. Total tabs active: ${ports.size}`);

    // Immediately connect WebSocket if not active
    connectWebSocket();

    port.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        console.log("[SharedWorker] Received frame from tab: ", payload);

        // 1. Cross-tab synchronization events (like selecting an agent or copying text)
        if (payload.sync) {
            broadcast({ type: "sync_view", sender: payload.sender, event: payload.event, data: payload.data });
        }

        // 2. Outgoing messages destined for the FastAPI central router
        if (payload.send_to_server && socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(payload.data));
        }
    };

    port.start();
};
