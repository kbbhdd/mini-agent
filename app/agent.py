import json

from rich.console import Console

from app.tools.calculator import calculator, CALCULATOR_SCHEMA, TOOL_MAP

console = Console()

TOOLS = [CALCULATOR_SCHEMA]

MAX_ITERATIONS = 5


def run_agent(llm, messages):
    """执行 Agent 循环，返回最终回答字符串。"""
    for _ in range(MAX_ITERATIONS):
        response = llm.client.chat.completions.create(
            model=llm.model,
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                result = "错误：参数不是合法 JSON"
            else:
                fn = TOOL_MAP.get(name)
                if fn is None:
                    result = f"错误：未知工具 {name}"
                else:
                    try:
                        result = fn(**args)
                    except Exception as e:
                        result = f"错误：{e}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "错误：超过最大迭代次数"