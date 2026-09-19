from datetime import datetime


class Trace:
    def __init__(self):
        self.events: list[dict] = []

    def add(self, kind: str, **data):
        """记录一条事件。kind 例如 'tool_call'、'tool_result'、'final'。"""
        self.events.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "kind": kind,
            **data,
        })

    def dump(self) -> str:
        """返回可读的文本。"""
        if not self.events:
            return "（本次会话暂无工具调用记录）"
        lines = []
        for e in self.events:
            t = e["time"]
            k = e["kind"]
            if k == "tool_call":
                lines.append(f"[{t}] → 调用 {e['name']}({e['args']})")
            elif k == "tool_result":
                lines.append(f"[{t}] ← 返回 {e['result'][:80]}")
            elif k == "final":
                lines.append(f"[{t}] ✓ 最终回答")
            else:
                lines.append(f"[{t}] {k} {e}")
        return "\n".join(lines)

    def clear(self):
        self.events.clear()