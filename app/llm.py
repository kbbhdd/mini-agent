import time
from threading import Lock

from openai import OpenAI
from app.config import (
    LLM_RPM,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    MODEL,
)


class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None, rpm=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url if base_url is not None else OPENAI_BASE_URL
        self.model = model or MODEL

        rpm = rpm if rpm is not None else LLM_RPM
        self._min_interval = 60.0 / rpm if rpm and rpm > 0 else 0.0
        self._last_call = 0.0
        self._lock = Lock()

        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        self.client = OpenAI(**kwargs)

    def _throttle(self):
        """距离上次调用不够最小间隔就等待。"""
        if self._min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._min_interval - (now - self._last_call)
            if wait > 0:
                time.sleep(wait)
            self._last_call = time.monotonic()

    def create_completion(self, messages, tools=None, stream=False):
        """统一的 LLM 调用入口，带限速。"""
        self._throttle()
        kwargs = {"model": self.model, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        if stream:
            kwargs["stream"] = True
        return self.client.chat.completions.create(**kwargs)

    def chat(self, messages):
        resp = self.create_completion(messages)
        return resp.choices[0].message.content

    def chat_stream(self, messages):
        stream = self.create_completion(messages, stream=True)
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content