"""
Summarizer agent that condenses supervisor chat history into a concise summary.
"""

import core.llm

class Summarizer:
    def __init__(self, llm: core.llm.LLM):
        self.llm = llm
    def summarize(self, messages: list[dict[str, str]]) -> str:
        pass