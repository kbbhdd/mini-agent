def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """把一段长文本切成多个片段，相邻片段有 overlap 字符重叠。"""
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = end - overlap

    return chunks