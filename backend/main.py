"""
Backend server.
"""

import core.config
import core.database
import schemas
from fastapi import FastAPI, Request, Response
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
def session_list():
    sessions = db.sessions.list()
    return {
        "success": True,
        "code": 200,
        "sessions": [session.dict() for session in sessions]
    }

@app.post("/a/session/create")
def session_create(create_request: schemas.SessionCreateRequest):
    session = db.sessions.create(create_request.topic_prompt)
    return {
        "success": True,
        "code": 200,
        "session": session.dict(),
    }

@app.post("/a/session/{session_id}/delete")
def session_delete(session_id: str):
    db.sessions.delete(session_id)
    return {
        "success": True,
        "code": 200,
    }
