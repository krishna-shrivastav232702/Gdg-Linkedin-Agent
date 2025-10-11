"""
Backend server.
"""

import core.config
import core.database
import schemas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return schemas.SessionListResponse(sessions=sessions)

@app.post("/a/session/create")
def session_create(create_request: schemas.SessionCreateRequest) -> schemas.SessionCreationResponse:
    session = db.sessions.create(create_request.topic_prompt)
    return schemas.SessionCreationResponse(session=session, code=201)

@app.post("/a/session/{session_id}/delete")
def session_delete(session_id: str) -> None:
    db.sessions.delete(session_id)
