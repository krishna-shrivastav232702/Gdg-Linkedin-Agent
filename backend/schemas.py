"""
Contains schemas for FastAPI request and response bodies.
"""

from fastapi import Response
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