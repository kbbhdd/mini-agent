from app.rag.index import RagIndex
from app.tools.registry import register

_index: RagIndex | None = None


def _ensure_index() -> RagIndex:
    """懒加载：第一次调用时才建索引。"""
    global _index
    if _index is None:
        _index = RagIndex()
        n = _index.build()
        print(f"[search_docs] 索引构建完成，共 {n} 个片段")
    return _index


def search_docs(query: str) -> str:
    """在 docs/ 目录里检索和 query 最相关的片段。"""
    idx = _ensure_index()
    if not idx.ready:
        return "错误：docs/ 目录下没有可用文档"

    results = idx.search(query)
    if not results:
        return "没有找到相关内容"

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(
            f"[{i}] 来源：{r['path']}（相似度 {r['score']:.3f}）\n{r['text']}"
        )
    return "\n\n".join(lines)


SEARCH_DOCS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": (
            "在本地文档库中检索信息。当用户询问关于公司制度、产品文档、"
            "内部知识等需要查阅资料的问题时使用。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "用户的问题或关键词，用于检索文档",
                }
            },
            "required": ["query"],
        },
    },
}


register("search_docs", SEARCH_DOCS_SCHEMA, search_docs)