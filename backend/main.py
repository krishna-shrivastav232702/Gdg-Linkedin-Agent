"""
Backend server.
"""

import core.config
import core.database
import schemas
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

config = core.config.load_config()
db = core.database.Database(
    config.mongodb.uri,
    config.mongodb.db_name,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.server.cors_allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/a/session/list")
def session_list() -> schemas.SessionListResponse:
    sessions = db.sessions.list()
    print(sessions)
    return schemas.SessionListResponse(sessions=sessions)

@app.post("/a/session/create")
def session_create(create_request: schemas.SessionCreateRequest) -> schemas.SessionCreationResponse:
    session = db.sessions.create(create_request.topic_prompt)
    return schemas.SessionCreationResponse(session=session)

@app.post("/a/session/{session_id}/delete")
def session_delete(session_id: str) -> None:
    db.sessions.delete(session_id)
    return schemas.SessionDeletionResponse()

@app.get("/a/session/{session_id}")
def session_detail(session_id: str) -> schemas.SessionDetailResponse:
    session = db.sessions.get(session_id)
    return schemas.SessionDetailResponse(session=session)

class WSConnection:
    def __init__(self, websocket: WebSocket, disconnection_callback: callable):
        self.websocket = websocket
        self.disconnection_callback = disconnection_callback
    async def disconnect(self):
        try:
            await self.websocket.close()
        except WebSocketDisconnect:
            pass
        self.disconnection_callback(self.websocket)
    async def send(self, data: dict):
        try:
            await self.websocket.send_json(data)
        except WebSocketDisconnect:
            await self.disconnect()
    async def receive(self):
        try:
            return await self.websocket.receive_json()
        except WebSocketDisconnect:
            await self.disconnect()
    async def handle_message(self, data):
        if not data.get("_"):
            return False
        
    async def run(self):
        while True:
            data = await self.receive()
            resp = await self.handle_message(data)
            if resp == False:
                return

class WSConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        return WSConnection(websocket, self.disconnect)
    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            pass

ws_manager = WSConnectionManager()

@app.websocket("/a/ws")
async def websocket_endpoint(websocket: WebSocket):
    ws = await ws_manager.connect(websocket)
    await ws.run()
    await ws.disconnect()