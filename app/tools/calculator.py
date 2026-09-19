import re

from app.tools.registry import register

ALLOWED = re.compile(r"^[\d+\-*/().\s]+$")


def calculator(expression: str) -> str:
    """计算数学表达式，返回结果字符串。"""
    expression = expression.strip()
    if not expression:
        return "错误：表达式为空"
    if not ALLOWED.match(expression):
        return "错误：表达式包含非法字符"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        return f"错误：{e}"
    return str(result)


CALCULATOR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "计算数学表达式。当用户需要做数学计算、算术运算时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "要计算的数学表达式，例如 '2+3*4'",
                }
            },
            "required": ["expression"],
        },
    },
}


register("calculator", CALCULATOR_SCHEMA, calculator)