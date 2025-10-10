"""
Contains schemas for FastAPI request and response bodies.
"""

import core.database
from pydantic import BaseModel

class SessionCreateRequest(BaseModel):
    topic_prompt: str
