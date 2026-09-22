import json
import sys
from pathlib import Path

# 让 python eval/run_eval.py 也能找到 app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agent import run_agent
from app.llm import LLMClient
from app.messages import build_messages
from app.trace import Trace

CASES_FILE = Path(__file__).parent / "cases.jsonl"


def load_cases():
    cases = []
    for line in CASES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            cases.append(json.loads(line))
    return cases


def extract_tool_names(trace: Trace):
    return [e["name"] for e in trace.events if e["kind"] == "tool_call"]


def run_case(llm, case):
    trace = Trace()
    messages = build_messages([], None)
    messages.append({"role": "user", "content": case["input"]})

    reply = run_agent(llm, messages, trace=trace)
    called_tools = extract_tool_names(trace)

    # 检查工具
    tool_ok = set(called_tools) == set(case["expect_tools"])

    # 检查内容
    content_ok = all(s in reply for s in case.get("must_contain", []))

    return {
        "input": case["input"],
        "reply": reply,
        "called_tools": called_tools,
        "expect_tools": case["expect_tools"],
        "tool_ok": tool_ok,
        "content_ok": content_ok,
        "passed": tool_ok and content_ok,
    }


def main():
    llm = LLMClient()
    cases = load_cases()

    passed = 0
    for i, case in enumerate(cases, 1):
        result = run_case(llm, case)
        status = "✅" if result["passed"] else "❌"
        print(f"[{i:2d}/{len(cases)}] {status} {result['input']}")
        if not result["passed"]:
            print(f"     期望工具：{result['expect_tools']}，实际：{result['called_tools']}")
            print(f"     回复：{result['reply'][:80]}")
        if result["passed"]:
            passed += 1

    rate = passed / len(cases) * 100
    print()
    print(f"通过：{passed}/{len(cases)}，通过率 {rate:.1f}%")


if __name__ == "__main__":
    main()