from app.config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K
from app.rag.embedder import embed_query, embed_texts
from app.rag.loader import load_docs
from app.rag.retriever import Retriever
from app.rag.splitter import split_text


class RagIndex:
    def __init__(self):
        self.retriever = Retriever()
        self.ready = False

    def build(self) -> int:
        """构建索引，返回片段总数。"""
        docs = load_docs()
        all_items = []

        for doc in docs:
            chunks = split_text(doc["text"], CHUNK_SIZE, CHUNK_OVERLAP)
            for i, chunk in enumerate(chunks):
                all_items.append({
                    "path": doc["path"],
                    "chunk_index": i,
                    "text": chunk,
                })

        if not all_items:
            self.ready = False
            return 0

        vectors = embed_texts([item["text"] for item in all_items])
        self.retriever.add(vectors, all_items)
        self.ready = True
        return len(all_items)

    def search(self, query: str, top_k: int = TOP_K) -> list[dict]:
        if not self.ready:
            return []
        qv = embed_query(query)
        return self.retriever.search(qv, top_k)