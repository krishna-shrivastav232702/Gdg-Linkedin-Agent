"""
Contains schemas for FastAPI request and response bodies.
"""

import core.database
from pydantic import BaseModel
import json

##################### Utilities ####################

class GenericResponse(BaseModel):
    code: int = 200

#################### Application releated schemas ####################

# Requests (inherit from BaseModel)
class SessionCreateRequest(BaseModel):
    topic_prompt: str

# Responses (inherit from GenericResponse) 
class SessionListResponse(GenericResponse):
    sessions: list[core.database.Session]

class SessionCreationResponse(GenericResponse):
    session: core.database.Session
    code: int = 201

class SessionDeletionResponse(GenericResponse):
    code: int = 204

class SessionDetailResponse(GenericResponse):
    session: core.database.Session | None
    messages: list[dict] | None = None
    draft: str | None = None
    def __init__(self, **data):
        super().__init__(**data)
        self.code = 200 if self.session else 404
        if not self.session: return
        self.messages = self.session.get_messages()
        self.draft = self.session.draft
