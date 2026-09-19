from typing import Callable

_TOOLS: dict[str, dict] = {}


def register(name: str, schema: dict, fn: Callable):
    """注册一个工具。"""
    _TOOLS[name] = {"schema": schema, "fn": fn}


def get_fn(name: str) -> Callable | None:
    """按名字取工具函数。"""
    entry = _TOOLS.get(name)
    return entry["fn"] if entry else None


def get_schemas() -> list[dict]:
    """返回所有工具的 schema 列表，给 LLM 看。"""
    return [entry["schema"] for entry in _TOOLS.values()]


def list_tools() -> list[str]:
    """返回所有已注册的工具名。"""
    return list(_TOOLS.keys())