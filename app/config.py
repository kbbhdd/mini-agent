import os
from dotenv import load_dotenv

load_dotenv()

# 聊天模型配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL","kimi-k2.6")

# Embedding 配置
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

# RAG 参数
CHUNK_SIZE = 500       # 每段文字最多字符数
CHUNK_OVERLAP = 100    # 相邻段之间重叠的字符数
TOP_K = 3              # 检索返回最相关的前 K 段
DOCS_DIR = "docs"      # 文档目录

LLM_RPM = int(os.getenv("LLM_RPM", "0"))  # 0 表示不限速