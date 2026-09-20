from openai import OpenAI

from app.config import (
    EMBEDDING_API_KEY,
    EMBEDDING_BASE_URL,
    EMBEDDING_MODEL,
)

_client = OpenAI(
    api_key=EMBEDDING_API_KEY,
    base_url=EMBEDDING_BASE_URL,
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """批量把文本转成向量。"""
    if not texts:
        return []

    resp = _client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    # resp.data 顺序和 texts 一致
    return [item.embedding for item in resp.data]


def embed_query(text: str) -> list[float]:
    """把单个查询文本转成向量。"""
    return embed_texts([text])[0]