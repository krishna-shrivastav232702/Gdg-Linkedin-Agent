"""
Quality of life improvements for config.
"""

from dataclasses import dataclass
from typing import get_type_hints
import toml

@dataclass
class SubConfig:
    pass

@dataclass
class Tavily(SubConfig):
    api_key: str

@dataclass
class Server(SubConfig):
    host: str
    port: int
    cors_allowed_origins: list[str]

@dataclass
class Config:
    tavily: Tavily
    server: Server
    def __init__(self, config: dict[str, dict[str, str]]):
        registered_types = get_type_hints(self)
        for k, v in config.items():
            if k in registered_types:
                setattr(self, k, registered_types[k](**v))

def load_config(config_file: str = "config.toml") -> Config:
    """
    Loads config.toml and instantiates Config object.
    """
    with open(config_file, encoding="utf-8") as f:
        config = toml.load(f)
    return Config(config)