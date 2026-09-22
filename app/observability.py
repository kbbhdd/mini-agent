import os

from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL

_enabled = False
_client = None


def init():
    """初始化 Langfuse，如果没配 key 就跳过。"""
    global _enabled, _client

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    if not public_key or not secret_key:
        return

    try:
        from langfuse import Langfuse
        _client = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        _enabled = True
        print("[observability] Langfuse 已启用")
    except Exception as e:
        print(f"[observability] Langfuse 初始化失败：{e}")


def is_enabled() -> bool:
    return _enabled

def log_agent_run(messages, reply, trace):
    """记录一次完整的 Agent 调用。"""
    if not _enabled or _client is None:
        return

    try:
        _client.trace(
            name="agent_run",
            input=messages,
            output=reply,
            metadata={"trace_dump": trace.dump()},
        )
        _client.flush()
    except Exception as e:
        print(f"[observability] 上报失败: {e}")