import json
import time

from openai import OpenAIError

from app.trace import Trace
from app.tools.registry import get_fn, get_schemas

# 触发工具注册（import 即注册）
import app.tools.calculator  # noqa: F401
import app.tools.time_tool   # noqa: F401
import app.tools.file_reader # noqa: F401

MAX_ITERATIONS = 5
TOOL_RETRIES = 2
TOOL_TIMEOUT = 10


def _call_tool(name, args, trace):
    """执行一个工具，带重试。"""
    fn = get_fn(name)
    if fn is None:
        return f"错误：未知工具 {name}"

    last_err = None
    for attempt in range(TOOL_RETRIES + 1):
        try:
            return fn(**args)
        except Exception as e:
            last_err = e
            time.sleep(0.5 * (attempt + 1))
    return f"错误：工具 {name} 失败（重试 {TOOL_RETRIES} 次）：{last_err}"


def run_agent(llm, messages, trace=None):
    """执行 Agent 循环。trace 可选，用于记录调用过程。"""
    trace = trace or Trace()
    tools = get_schemas()

    for _ in range(MAX_ITERATIONS):
        response = llm.client.chat.completions.create(
            model=llm.model,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            trace.add("final")
            return msg.content

        messages.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            raw_args = tool_call.function.arguments

            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                result = "错误：参数不是合法 JSON"
                args = {}
            else:
                trace.add("tool_call", name=name, args=raw_args)
                result = _call_tool(name, args, trace)

            trace.add("tool_result", name=name, result=str(result))

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    return "错误：超过最大迭代次数"