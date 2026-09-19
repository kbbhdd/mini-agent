from datetime import datetime

from app.tools.registry import register


def get_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """返回当前时间。"""
    try:
        return datetime.now().strftime(format)
    except Exception as e:
        return f"错误：{e}"


TIME_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "获取当前日期和时间。当用户询问现在几点、今天几号、当前时间时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "description": "时间格式，默认 '%Y-%m-%d %H:%M:%S'。一般不用传。",
                }
            },
            "required": [],
        },
    },
}


register("get_time", TIME_SCHEMA, get_time)