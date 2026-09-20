from pathlib import Path

from app.config import DOCS_DIR


def load_docs() -> list[dict]:
    """读取 docs/ 目录下所有 .md 和 .txt，返回 [{"path": ..., "text": ...}, ...]。"""
    docs_dir = Path(DOCS_DIR)
    if not docs_dir.exists():
        return []

    results = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[loader] 跳过 {path}: {e}")
            continue
        results.append({
            "path": str(path),
            "text": text,
        })
    return results