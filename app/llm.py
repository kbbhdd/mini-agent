from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL

kwargs = {"api_key": OPENAI_API_KEY}
if OPENAI_BASE_URL:
    kwargs["base_url"] = OPENAI_BASE_URL

client = OpenAI(**kwargs)

def chat(messages):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    answer = chat([
        {"role": "user", "content": "用一句话解释什么是 AI Agent"}
    ])
    print(answer)