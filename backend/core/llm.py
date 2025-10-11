"""
LLM API wrappers and utilities.
"""

from typing import Iterable
import core.config
import cerebras.cloud.sdk

class LLM:
    def __init__(self, provider_config: core.config.LLMProviderConfig, model_name: str = "qwen-3-32b"):
        self._client = cerebras.cloud.sdk.Cerebras(api_key=provider_config.api_key)
        self.model_name = model_name
    def complete(self, messages: list[dict[str, str]], temperature: float = None, stop: str = None) -> Iterable[str]:
        stream = self._client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=temperature,
            stream=True,
            stop=stop
        )
        try:
            for chunk in stream:
                yield chunk.choices[0].delta.content or ""
        finally:
            stream.close()
