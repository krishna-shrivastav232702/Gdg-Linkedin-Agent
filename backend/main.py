"""
Backend server.
"""

import core.config
import core.database
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

config = core.config.load_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.server.cors_allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = core.database.Database(
    config.mongodb.uri,
    config.mongodb.db_name,
)
