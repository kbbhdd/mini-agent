from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agent import run_agent
from app.llm import LLMClient
from app.messages import DEFAULT_SYSTEM_PROMPT, build_messages
from app.trace import Trace

app = FastAPI(title="Mini-Agent API")

_llm = LLMClient()


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入")
    history: list[dict] = Field(default_factory=list, description="历史消息")
    system_prompt: str = Field(default=DEFAULT_SYSTEM_PROMPT)


class ChatResponse(BaseModel):
    reply: str
    trace: str
    history: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    trace = Trace()
    messages = build_messages(req.history, req.system_prompt)
    messages.append({"role": "user", "content": req.message})

    reply = run_agent(_llm, messages, trace=trace)

    new_history = list(req.history)
    new_history.append({"role": "user", "content": req.message})
    new_history.append({"role": "assistant", "content": reply})

    return ChatResponse(
        reply=reply,
        trace=trace.dump(),
        history=new_history,
    )