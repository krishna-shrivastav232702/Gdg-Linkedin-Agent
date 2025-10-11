"""
Contains database connection logic.
"""

from dataclasses import dataclass
import pymongo
import uuid
import time

def factory(uri: str, db_name: str) -> pymongo.database.Database:
    """
    Creates a MongoDB database client.
    """
    return pymongo.MongoClient(uri)[db_name]

@dataclass
class Session:
    topic_prompt: str
    session_id: str
    created_at: float
    def __init__(self, db: pymongo.database.Database, session_id: str):
        self.db = db
        _data = self.db.sessions.find_one({"id": session_id}, {"_id": 0})
        if not _data:
            raise ValueError("Session not found")
        self.session_id = session_id
        self.topic_prompt = _data["topic_prompt"]
        self.created_at = _data["created_at"]
        self.deleted = _data.get("deleted", False)
    @property
    def title(self) -> str:
        return self.db.sessions.find_one({"id": self.session_id}, {"_id": 0, "title": 1})["title"]
    @title.setter
    def title(self, value: str) -> None:
        self.db.sessions.update_one(
            {"id": self.session_id},
            {"$set": {"title": value}}
        )
    @property
    def draft(self) -> str:
        return self.db.sessions.find_one({"id": self.session_id}, {"_id": 0, "draft": 1})["draft"]
    @draft.setter
    def draft(self, value: str) -> None:
        self.db.sessions.update_one(
            {"id": self.session_id},
            {"$set": {"draft": value}}
        )
    def get_messages(self) -> list[dict]:
        return self.db.sessions.find_one({"id": self.session_id}, {"_id": 0, "messages": 1})["messages"]
    def add_message(self, role: str, content: str) -> None:
        self.db.sessions.update_one(
            {"id": self.session_id},
            {"$push": {"messages": {"role": role, "content": content}}}
        )
    def add_summary(self, summary: str) -> None:
        self.db.sessions.update_one(
            {"id": self.session_id},
            {"$push": {"messages": {"role": "summary", "content": summary}}}
        )

class SessionManager:
    def __init__(self, db: pymongo.database.Database):
        self.db = db
    def create(self, topic_prompt: str) -> Session:
        session_id = str(uuid.uuid4())
        self.db.sessions.insert_one({
            "id": session_id,
            "topic_prompt": topic_prompt,
            "title": topic_prompt.title()[:64],
            "messages": [], # full message history (no compression or truncation)
            "draft": "",
            "researched_texts": [],
            "created_at": time.time()
        })
        return Session(self.db, session_id)
    def list(self) -> list[Session]:
        return [Session(self.db, s["id"]) for s in self.db.sessions.find({}, {"_id": 0, "id": 1, "deleted": 1}) if not s.get("deleted", False)]
    def get(self, session_id: str) -> Session | None:
        try:
            return Session(self.db, session_id)
        except ValueError:
            return None
    def delete(self, session_id: str) -> None:
        # soft delete
        self.db.sessions.update_one(
            {"id": session_id},
            {"$set": {"deleted": True}}
        )

class Database:
    def __init__(self, uri: str, db_name: str):
        self.db = factory(uri, db_name)
        self.sessions = SessionManager(self.db)
    