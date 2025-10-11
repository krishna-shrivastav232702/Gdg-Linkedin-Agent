"""
Contains AI agent related functions.
"""

import core.config
import core.agent

class Agent:
    def __init__(self, config: core.config.Config, session_id: str):
        self.config = config
        self.session_id = session_id
        self.llm = core.llm.LLM(provider_config=self.config.llm_provider)
        self.supervisor = core.agent.supervisor.Supervisor(llm=self.llm)
        self.summarizer = core.agent.summarizer.Summarizer(llm=self.llm)
    def user_input(self, prompt: str):
        pass
