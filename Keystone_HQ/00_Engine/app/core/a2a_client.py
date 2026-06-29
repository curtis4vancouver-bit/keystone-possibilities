import asyncio
import httpx
import json
import sys
from typing import Dict, Any, List, Optional, AsyncGenerator

class A2AClient:
    def __init__(self, base_url: str, timeout_sec: float = 30.0):
        """
        Resilient client connection wrapper targeting a local Spoke HTTP port.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_sec
        # We reuse HTTPX connection pools to speed up operations and bypass handshake latencies
        self.limits = httpx.Limits(max_keepalive_connections=16, max_connections=32)

    async def handshake(self) -> Dict[str, Any]:
        """
        Queries Spoke agent configuration endpoints to verify capabilities and status.
        """
        async with httpx.AsyncClient(limits=self.limits) as client:
            try:
                response = await client.get(f"{self.base_url}/handshake", timeout=5.0)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise RuntimeError(f"Handshake failed with status: {response.status_code}")
            except Exception as e:
                raise ConnectionError(f"Failed to connect to Spoke agent at {self.base_url}: {str(e)}")

    async def submit_task(self, instructions: List[Dict[str, Any]], context_slice: Optional[Dict[str, Any]] = None, task_id: Optional[str] = None) -> str:
        """
        Dispatches task instructions and secure context slice payloads to the target Spoke.
        """
        payload = {
            "instructions": instructions,
            "context_slice": context_slice
        }
        if task_id:
            payload["task_id"] = task_id

        async with httpx.AsyncClient(limits=self.limits) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/tasks",
                    json=payload,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    res_data = response.json()
                    return res_data["task_id"]
                else:
                    raise RuntimeError(f"Task submission rejected: {response.text}")
            except Exception as e:
                raise ConnectionError(f"Task submission crashed for Spoke at {self.base_url}: {str(e)}")

    async def stream_events(self, task_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Subscribes to target Spoke SSE events dynamically.
        Implements reconnection resiliency to handle subprocess or connection dropouts.
        """
        reconnect_delay = 1.0
        max_reconnect_attempts = 5
        attempts = 0

        while attempts < max_reconnect_attempts:
            try:
                async with httpx.AsyncClient(limits=self.limits) as client:
                    async with client.stream("GET", f"{self.base_url}/tasks/{task_id}/events", timeout=None) as response:
                        if response.status_code != 200:
                            raise ConnectionError(f"Failed to open SSE stream: status {response.status_code}")
                        
                        # Reset connection attempt count on successful stream open
                        attempts = 0
                        
                        async for line in response.iter_lines():
                            line = line.strip()
                            if line.startswith("data:"):
                                data_str = line[len("data:"):].strip()
                                try:
                                    event = json.loads(data_str)
                                    yield event
                                    
                                    # Terminate loop gracefully if task is in final state
                                    if event.get("state") in ["completed", "failed"]:
                                        return
                                except Exception as parse_err:
                                    print(f"[A2AClient] SSE JSON parsing error: {parse_err}", file=sys.stderr)
                                    
            except (httpx.RequestError, ConnectionError) as conn_ex:
                attempts += 1
                if attempts >= max_reconnect_attempts:
                    print(f"[A2AClient] 🛑 Max reconnection attempts reached for {task_id}.", file=sys.stderr)
                    yield {"event_type": "status_update", "task_id": task_id, "state": "failed", "message": f"Connection lost: {str(conn_ex)}", "progress": 1.0}
                    return
                
                print(f"[A2AClient] Connection dropped. Retrying in {reconnect_delay}s (Attempt {attempts}/{max_reconnect_attempts})...", file=sys.stderr)
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 8.0) # Exponential backoff capped at 8s
