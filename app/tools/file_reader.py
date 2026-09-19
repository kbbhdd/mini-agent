from pathlib import Path

from app.tools.registry import register

# 允许读取的目录（后面做 RAG 时会用到 docs/）
ALLOWED_DIR = Path("docs").resolve()

MAX_CHARS = 3000


def read_file(path: str) -> str:
    """读取指定文件内容（限制在 docs 目录下，最多 3000 字符）。"""
    try:
        target = Path(path).resolve()
    except Exception as e:
        return f"错误：路径无效 {e}"

    if not str(target).startswith(str(ALLOWED_DIR)):
        return f"错误：只允许读取 {ALLOWED_DIR} 下的文件"

    if not target.exists():
        return f"错误：文件不存在 {path}"

    if not target.is_file():
        return f"错误：不是文件 {path}"

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return f"错误：读取失败 {e}"

    if len(content) > MAX_CHARS:
        return content[:MAX_CHARS] + f"\n\n...（已截断，原文件 {len(content)} 字符）"

    return content


FILE_READER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取 docs 目录下的文本文件。当用户想让你看某个文件内容时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径，例如 'docs/notes.txt'",
                }
            },
            "required": ["path"],
        },
    },
}


register("read_file", FILE_READER_SCHEMA, read_file)