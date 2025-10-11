"""
Contains the agentic logic and implementation.
"""

import core.llm

class Supervisor:
    def __init__(self, llm: core.llm.LLM):
        self.llm = llm
