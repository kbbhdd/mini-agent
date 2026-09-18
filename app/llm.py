from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL


class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url if base_url is not None else OPENAI_BASE_URL
        self.model = model or MODEL

        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url

        self.client = OpenAI(**kwargs)

    def chat(self, messages):
        """非流式，一次性返回"""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return resp.choices[0].message.content

    def chat_stream(self, messages):
        """流式，逐块返回文字"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content


if __name__ == "__main__":
    llm = LLMClient()
    for piece in llm.chat_stream([
        {"role": "user", "content": "用一句话解释 AI Agent"}
    ]):
        print(piece, end="", flush=True)
    print()