#!/usr/bin/env python3
"""
Keystone Flow Proxy Daemon
Runs a WebSocket server (port 3847) to communicate with the Chrome extension,
and a FastAPI server (port 8100) to expose Google Flow endpoints as a local REST API.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import json
import logging
import time
import uuid
import secrets
from typing import Optional, List, Dict
import uvicorn
import websockets
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("flow_proxy_daemon")

# ─── Configuration ───────────────────────────────────────────
API_HOST = "127.0.0.1"
API_PORT = 8100
WS_HOST = "127.0.0.1"
WS_PORT = 3847

GOOGLE_FLOW_API = "https://aisandbox-pa.googleapis.com"
GOOGLE_API_KEY = "AIzaSyBtrm0o5ab1c-Ec8ZuLcGt3oJAA5VWt3pY"

# ─── Flow Client ─────────────────────────────────────────────
class FlowClient:
    def __init__(self):
        self._extension_ws = None
        self._pending: Dict[str, asyncio.Future] = {}
        self.flow_key: Optional[str] = None
        self.token_captured_at: Optional[float] = None
        self.callback_secret: str = secrets.token_urlsafe(32)

    def set_extension(self, ws):
        self._extension_ws = ws
        logger.info("Extension connected to WebSocket")

    def clear_extension(self):
        self._extension_ws = None
        # Cancel all pending requests
        pending_copy = list(self._pending.items())
        for req_id, future in pending_copy:
            if not future.done():
                future.set_exception(ConnectionError("Extension disconnected"))
        self._pending.clear()
        logger.warning("Extension disconnected, cleared pending requests")

    @property
    def connected(self) -> bool:
        return self._extension_ws is not None

    async def handle_message(self, data: dict):
        """Handle incoming WebSocket message from extension."""
        msg_type = data.get("type")
        if msg_type == "token_captured":
            self.flow_key = data.get("flowKey")
            self.token_captured_at = time.time()
            logger.info("Bearer token successfully captured from extension")
            return
        elif msg_type == "extension_ready":
            logger.info("Extension ready, token present: %s", "yes" if data.get("flowKeyPresent") else "no")
            return
        elif msg_type == "ping":
            if self._extension_ws:
                await self._extension_ws.send(json.dumps({"type": "pong"}))
            return
        elif msg_type == "pong":
            return

        # Response to a pending request (fallback to WS)
        req_id = data.get("id")
        if req_id and req_id in self._pending:
            future = self._pending[req_id]
            if not future.done():
                future.set_result(data)

    async def send_request(self, method: str, params: dict, timeout: float = 300) -> dict:
        """Send request to extension via WS and wait for response."""
        if not self.connected:
            return {"error": "Extension not connected"}

        req_id = str(uuid.uuid4())
        future = asyncio.get_running_loop().create_future()
        self._pending[req_id] = future

        try:
            await self._extension_ws.send(json.dumps({
                "id": req_id,
                "method": method,
                "params": params
            }))
            # Wait for response (resolved by ws message or HTTP callback)
            result = await asyncio.wait_for(future, timeout=timeout)
            return result
        except asyncio.TimeoutError:
            return {"error": f"Timeout ({timeout}s) waiting for response on {method}"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            self._pending.pop(req_id, None)

# Global Client Instance
client = FlowClient()

# ─── FastAPI Application ─────────────────────────────────────
app = FastAPI(title="Keystone Flow Proxy API", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/status")
async def get_status():
    return {
        "extension_connected": client.connected,
        "token_present": client.flow_key is not None,
        "token_age_seconds": (time.time() - client.token_captured_at) if client.token_captured_at else None,
        "ws_endpoint": f"ws://{WS_HOST}:{WS_PORT}"
    }

@app.post("/api/ext/callback")
async def ext_callback(request: Request):
    """HTTP callback for extension to deliver API responses (highly reliable)."""
    data = await request.json()
    req_id = data.get("id")
    if req_id and req_id in client._pending:
        future = client._pending[req_id]
        if not future.done():
            future.set_result(data)
            return {"ok": True}
    return {"ok": False, "reason": "no matching pending request"}

@app.post("/create_project")
async def create_project(payload: dict):
    """Create a project via tRPC."""
    title = payload.get("projectTitle", "New Project")
    tool_name = payload.get("toolName", "PINHOLE")
    
    url = "https://labs.google/fx/api/trpc/project.createProject"
    body = {"json": {"projectTitle": title, "toolName": tool_name}}

    res = await client.send_request("trpc_request", {
        "url": url,
        "method": "POST",
        "headers": {
            "content-type": "application/json",
            "accept": "*/*"
        },
        "body": body
    }, timeout=30)
    
    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Failed to create project"))
    return res.get("data", res)

@app.post("/generate_image")
async def generate_image(payload: dict):
    """Generate images using Nano Banana Pro (GEM_PIX_2)."""
    project_id = payload.get("projectId")
    prompt = payload.get("prompt")
    aspect_ratio = payload.get("imageAspectRatio", "IMAGE_ASPECT_RATIO_PORTRAIT")
    character_media_ids = payload.get("characterMediaIds")
    user_paygate_tier = payload.get("userPaygateTier", "PAYGATE_TIER_TWO")

    if not project_id or not prompt:
        raise HTTPException(status_code=400, detail="Missing projectId or prompt")

    ts = int(time.time() * 1000)
    ctx = {
        "projectId": str(project_id),
        "recaptchaContext": {
            "applicationType": "RECAPTCHA_APPLICATION_TYPE_WEB",
            "token": ""
        },
        "sessionId": f";{ts}",
        "tool": "PINHOLE",
        "userPaygateTier": user_paygate_tier
    }

    request_item = {
        "clientContext": {**ctx, "sessionId": f";{ts}"},
        "seed": ts % 1000000,
        "structuredPrompt": {"parts": [{"text": prompt}]},
        "imageAspectRatio": aspect_ratio,
        "imageModelName": "GEM_PIX_2"  # Nano Banana Pro
    }

    if character_media_ids:
        request_item["imageInputs"] = [
            {"name": mid, "imageInputType": "IMAGE_INPUT_TYPE_REFERENCE"}
            for mid in character_media_ids
        ]

    body = {
        "clientContext": ctx,
        "requests": [request_item]
    }
    if character_media_ids:
        body["mediaGenerationContext"] = {"batchId": str(uuid.uuid4())}
        body["useNewMedia"] = True

    url = f"{GOOGLE_FLOW_API}/v1/projects/{project_id}/flowMedia:batchGenerateImages?key={GOOGLE_API_KEY}"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "POST",
        "body": body,
        "captchaAction": "IMAGE_GENERATION"
    }, timeout=90)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Image generation failed"))
    return res.get("data", res)

@app.post("/generate_video")
async def generate_video(payload: dict):
    """Generate 10s video from start image using Omni Flash."""
    project_id = payload.get("projectId")
    start_image_media_id = payload.get("startImageMediaId")
    prompt = payload.get("prompt")
    scene_id = payload.get("sceneId", "scene-1")
    aspect_ratio = payload.get("aspectRatio", "VIDEO_ASPECT_RATIO_PORTRAIT")
    user_paygate_tier = payload.get("userPaygateTier", "PAYGATE_TIER_TWO")

    if not project_id or not start_image_media_id or not prompt:
        raise HTTPException(status_code=400, detail="Missing projectId, startImageMediaId, or prompt")

    ts = int(time.time() * 1000)
    ctx = {
        "projectId": str(project_id),
        "recaptchaContext": {
            "applicationType": "RECAPTCHA_APPLICATION_TYPE_WEB",
            "token": ""
        },
        "sessionId": f";{ts}",
        "tool": "PINHOLE",
        "userPaygateTier": user_paygate_tier
    }

    # Model resolution depending on aspect ratio & tier
    # TIER TWO defaults: veo_3_1_i2v_lite_low_priority
    model_key = "veo_3_1_i2v_lite_low_priority"

    request = {
        "aspectRatio": aspect_ratio,
        "seed": ts % 10000,
        "textInput": {"structuredPrompt": {"parts": [{"text": prompt}]}},
        "videoModelKey": model_key,
        "startImage": {"mediaId": start_image_media_id},
        "metadata": {"sceneId": scene_id}
    }

    body = {
        "mediaGenerationContext": {"batchId": str(uuid.uuid4())},
        "clientContext": ctx,
        "requests": [request],
        "useV2ModelConfig": True
    }

    url = f"{GOOGLE_FLOW_API}/v1/video:batchAsyncGenerateVideoStartImage?key={GOOGLE_API_KEY}"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "POST",
        "body": body,
        "captchaAction": "VIDEO_GENERATION"
    }, timeout=60)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Video generation submission failed"))
    return res.get("data", res)

@app.post("/check_video_status")
async def check_video_status(payload: dict):
    """Check status of video generation operations."""
    operations = payload.get("operations")
    if not operations:
        raise HTTPException(status_code=400, detail="Missing operations list")

    body = {"operations": operations}
    url = f"{GOOGLE_FLOW_API}/v1/video:batchCheckAsyncVideoGenerationStatus?key={GOOGLE_API_KEY}"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "POST",
        "body": body
    }, timeout=30)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Failed to check status"))
    return res.get("data", res)

@app.post("/upload_image")
async def upload_image(payload: dict):
    """Upload an image to Google Flow."""
    project_id = payload.get("projectId", "")
    file_name = payload.get("fileName", "upload.jpg")
    image_base64 = payload.get("imageBytes")  # Base64 string
    mime_type = payload.get("mimeType", "image/jpeg")

    if not image_base64:
        raise HTTPException(status_code=400, detail="Missing imageBytes")

    body = {
        "clientContext": {
            "projectId": project_id,
            "tool": "PINHOLE"
        },
        "fileName": file_name,
        "imageBytes": image_base64,
        "isHidden": False,
        "isUserUploaded": True,
        "mimeType": mime_type
    }

    url = f"{GOOGLE_FLOW_API}/v1/flow/uploadImage?key={GOOGLE_API_KEY}"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "POST",
        "body": body
    }, timeout=60)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Image upload failed"))
    return res.get("data", res)

@app.get("/media/{media_id}")
async def get_media(media_id: str):
    """Fetch media metadata / signed URL."""
    url = f"{GOOGLE_FLOW_API}/v1/media/{media_id}?key={GOOGLE_API_KEY}&clientContext.tool=PINHOLE"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "GET"
    }, timeout=15)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Failed to fetch media"))
    return res.get("data", res)

@app.post("/upscale_video")
async def upscale_video(payload: dict):
    """Upscale video to 1080p or 4K."""
    media_id = payload.get("mediaId")
    scene_id = payload.get("sceneId", "scene-1")
    aspect_ratio = payload.get("aspectRatio", "VIDEO_ASPECT_RATIO_PORTRAIT")
    resolution = payload.get("resolution", "VIDEO_RESOLUTION_1080P")

    if not media_id:
        raise HTTPException(status_code=400, detail="Missing mediaId")

    model_key = "veo_3_1_upsampler_1080p" if resolution == "VIDEO_RESOLUTION_1080P" else "veo_3_1_upsampler_4k"

    body = {
        "clientContext": {
            "sessionId": f";{int(time.time() * 1000)}",
            "recaptchaContext": {
                "applicationType": "RECAPTCHA_APPLICATION_TYPE_WEB",
                "token": ""
            }
        },
        "requests": [{
            "aspectRatio": aspect_ratio,
            "resolution": resolution,
            "seed": int(time.time()) % 100000,
            "metadata": {"sceneId": scene_id},
            "videoInput": {"mediaId": media_id},
            "videoModelKey": model_key
        }]
    }

    url = f"{GOOGLE_FLOW_API}/v1/video:batchAsyncGenerateVideoUpsampleVideo?key={GOOGLE_API_KEY}"
    res = await client.send_request("api_request", {
        "url": url,
        "method": "POST",
        "body": body,
        "captchaAction": "VIDEO_GENERATION"
    }, timeout=60)

    if "error" in res or res.get("status", 200) >= 400:
        raise HTTPException(status_code=res.get("status", 500), detail=res.get("error", "Upscale submission failed"))
    return res.get("data", res)

# ─── WebSocket Server Runner ─────────────────────────────────
async def ws_handler(websocket, path=None):
    """Handle connection from Chrome Extension."""
    client.set_extension(websocket)
    # Send callback secret to extension
    await websocket.send(json.dumps({"type": "callback_secret", "secret": client.callback_secret}))
    
    try:
        async for raw in websocket:
            try:
                data = json.loads(raw)
                await client.handle_message(data)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received from extension")
            except Exception as e:
                logger.exception("Error handling extension message: %s", e)
    except websockets.ConnectionClosed:
        pass
    finally:
        client.clear_extension()

async def run_ws_server():
    async with websockets.serve(ws_handler, WS_HOST, WS_PORT):
        logger.info("WebSocket server listening on ws://%s:%d", WS_HOST, WS_PORT)
        await asyncio.Future()  # Keep running

# ─── Daemon Launcher ─────────────────────────────────────────
async def main():
    # Start Websocket Server
    ws_task = asyncio.create_task(run_ws_server())
    
    # Run FastAPI via Uvicorn in the same event loop
    config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()
    ws_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Daemon stopped by user")
