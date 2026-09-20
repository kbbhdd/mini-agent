import numpy as np


class Retriever:
    def __init__(self):
        self.vectors: np.ndarray | None = None
        self.items: list[dict] = []

    def add(self, vectors: list[list[float]], items: list[dict]):
        """把向量和对应的元数据存进来。"""
        self.vectors = np.array(vectors, dtype=np.float32)
        self.items = items

    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        """返回最相似的 top_k 条记录，每条附带 score。"""
        if self.vectors is None or len(self.items) == 0:
            return []

        q = np.array(query_vector, dtype=np.float32)

        # 余弦相似度 = 点积 / (模长乘积)
        dots = self.vectors @ q
        norms = np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(q)
        scores = dots / (norms + 1e-8)

        top_idx = np.argsort(-scores)[:top_k]

        results = []
        for i in top_idx:
            item = dict(self.items[i])
            item["score"] = float(scores[i])
            results.append(item)
        return results