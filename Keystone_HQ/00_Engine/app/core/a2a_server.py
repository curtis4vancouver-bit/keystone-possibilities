import asyncio
import uuid
import json
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse

# =========================================================================
# Serialized Message Parts & Data Schemas (Parts Model)
# =========================================================================
class TextPart(BaseModel):
    type: str = "text"
    text: str

class FilePart(BaseModel):
    type: str = "file"
    file_path: str
    description: Optional[str] = None

class DataPart(BaseModel):
    type: str = "data"
    payload: Dict[str, Any]

PartType = Union[TextPart, FilePart, DataPart]

class TaskRequest(BaseModel):
    task_id: Optional[str] = None
    instructions: List[PartType]
    context_slice: Optional[Dict[str, Any]] = None

class TaskStatusUpdateEvent(BaseModel):
    event_type: str = "status_update"
    task_id: str
    state: str
    message: str
    progress: float  # 0.0 to 1.0

class TaskArtifactUpdateEvent(BaseModel):
    event_type: str = "artifact_update"
    task_id: str
    artifact_name: str
    data: Dict[str, Any]

# =========================================================================
# Subagent Registration Profile (AgentCard)
# =========================================================================
class AgentCard(BaseModel):
    agent_name: str
    port: int
    capabilities: List[str]
    description: str
    rules: List[str]
    status: str = "idle"

# =========================================================================
# Durable Event Queue Manager (Thread-Safe Event Streams)
# =========================================================================
class EventQueue:
    def __init__(self):
        self.queues: Dict[str, List[asyncio.Queue]] = {}
        self.lock = asyncio.Lock()

    async def register_listener(self, task_id: str) -> asyncio.Queue:
        async with self.lock:
            if task_id not in self.queues:
                self.queues[task_id] = []
            q = asyncio.Queue()
            self.queues[task_id].append(q)
            return q

    async def deregister_listener(self, task_id: str, queue: asyncio.Queue):
        async with self.lock:
            if task_id in self.queues:
                self.queues[task_id].remove(queue)
                if not self.queues[task_id]:
                    del self.queues[task_id]

    async def broadcast_event(self, task_id: str, event: Union[TaskStatusUpdateEvent, TaskArtifactUpdateEvent]):
        async with self.lock:
            if task_id in self.queues:
                for q in self.queues[task_id]:
                    await q.put(event)

# =========================================================================
# A2A Spoke Starlette Application Wrapper
# =========================================================================
class A2AServer:
    def __init__(self, card: AgentCard):
        self.card = card
        self.app = FastAPI(title=f"A2A Spoke - {card.agent_name}", version="2.0.0")
        self.event_queue = EventQueue()
        
        # In-memory store for active tasks and states
        # lifecycle: submitted -> working -> completed / failed / input-required
        self.tasks_state: Dict[str, Dict[str, Any]] = {}
        
        # Bind routes
        self._register_routes()

    def _register_routes(self):
        @self.app.get("/handshake", response_model=AgentCard)
        async def handshake():
            """Returns the Spoke's AgentCard describing its identity and capabilities."""
            self.card.status = "idle" if not self.tasks_state else "working"
            return self.card

        @self.app.post("/tasks")
        async def submit_task(request: TaskRequest, background_tasks: BackgroundTasks):
            """Submits a cognitive execution instruction block to the spoke agent."""
            task_id = request.task_id or str(uuid.uuid4())[:12]
            
            if task_id in self.tasks_state:
                raise HTTPException(status_code=400, detail="Task ID already exists.")
            
            self.tasks_state[task_id] = {
                "task_id": task_id,
                "state": "submitted",
                "instructions": request.instructions,
                "context_slice": request.context_slice,
                "progress": 0.0,
                "logs": []
            }
            
            # Broadcast the submission event
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="submitted", message="Task submitted successfully", progress=0.0)
            )
            
            # Dispatch background task execution
            background_tasks.add_task(self._execute_task_pipeline, task_id)
            return {"status": "success", "task_id": task_id}

        @self.app.get("/tasks/{task_id}/events")
        async def stream_task_events(task_id: str):
            """Server-Sent Events (SSE) route streaming real-time status and artifact outputs."""
            if task_id not in self.tasks_state:
                raise HTTPException(status_code=404, detail="Task not found.")
                
            async def event_generator():
                listener_queue = await self.event_queue.register_listener(task_id)
                try:
                    # Stream initial state
                    current = self.tasks_state.get(task_id, {})
                    yield f"data: {json.dumps(current)}\n\n"
                    
                    while True:
                        event = await listener_queue.get()
                        yield f"data: {event.model_dump_json()}\n\n"
                        
                        # Stop generator if terminal state is reached
                        if isinstance(event, TaskStatusUpdateEvent) and event.state in ["completed", "failed"]:
                            break
                except asyncio.CancelledError:
                    pass
                finally:
                    await self.event_queue.deregister_listener(task_id, listener_queue)
                    
            return StreamingResponse(event_generator(), media_type="text/event-stream")

    async def _execute_task_pipeline(self, task_id: str):
        """
        Coordinates state transitions dynamically.
        Simulates task execution with cooperative async loops.
        """
        task = self.tasks_state[task_id]
        task["state"] = "working"
        
        try:
            # 1. State transition: working (0%)
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="working", message="Initializing execution sequence", progress=0.1)
            )
            await asyncio.sleep(1.0)
            
            # 2. Decontextualized compilation validation (30%)
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="working", message="Compiling contextual brain tokens", progress=0.3)
            )
            await asyncio.sleep(1.5)
            
            # 3. Simulate processing and file artifact generation (60%)
            artifact_data = {
                "output_text": "Empirical script outline generated based on builder specifications.",
                "duration_seconds": 180,
                "references": ["Master_Docs/04_YOUTUBE_CONTENT_ENGINE.md"]
            }
            await self.event_queue.broadcast_event(
                task_id,
                TaskArtifactUpdateEvent(task_id=task_id, artifact_name="script_outline", data=artifact_data)
            )
            
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="working", message="Performing validation testing", progress=0.7)
            )
            await asyncio.sleep(1.0)
            
            # 4. State transition: completed (100%)
            task["state"] = "completed"
            task["progress"] = 1.0
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="completed", message="Execution finalized successfully", progress=1.0)
            )
            
        except Exception as e:
            # Failure fallback transition
            task["state"] = "failed"
            await self.event_queue.broadcast_event(
                task_id,
                TaskStatusUpdateEvent(task_id=task_id, state="failed", message=f"Task failed: {str(e)}", progress=1.0)
            )
