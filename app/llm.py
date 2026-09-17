from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL

kwargs = {"api_key": OPENAI_API_KEY}
if OPENAI_BASE_URL:
    kwargs["base_url"] = OPENAI_BASE_URL

client = OpenAI(**kwargs)


def chat(messages):
    """非流式，一次性返回"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return resp.choices[0].message.content


def chat_stream(messages):
    """流式，逐块返回文字"""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content