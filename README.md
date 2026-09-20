# Mini-Agent

一个本地 AI Agent，支持工具调用、知识库检索、Web 界面。

## 特性

- 多轮对话 + 流式输出
- Function Calling：计算器、时间查询、文件读取、文档检索
- RAG 知识库：基于 docs/ 目录的语义检索
- 工具注册机制：加工具只改一个文件
- 工具重试 + 调用日志
- FastAPI 后端 + Streamlit 前端
- 命令行界面

## 架构

```
浏览器 → Streamlit → FastAPI → Agent循环 → LLM
                                    ↓
                              工具注册中心
                                    ↓
                     calculator / get_time / read_file / search_docs
                                    ↓
                          RAG (loader → splitter → embedder → retriever)
```

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env  # 填入你的API Key
```

**终端1：启动后端**

```bash
uvicorn app.server:app --reload --port 8000
```

**终端2：启动前端**

```bash
streamlit run web/streamlit_app.py
```

浏览器打开 http://localhost:8501

**或者只用命令行：**

```bash
python -m app.chat
```

## 环境变量

```
OPENAI_API_KEY=        # 聊天模型（DeepSeek / OpenAI）
OPENAI_BASE_URL=
MODEL=

EMBEDDING_API_KEY=     # 向量模型（硅基流动）
EMBEDDING_BASE_URL=
EMBEDDING_MODEL=BAAI/bge-m3
```

## 项目结构

```
app/
  llm.py           # LLM客户端
  agent.py         # Agent循环
  messages.py      # 消息构建
  trace.py         # 调用日志
  server.py        # FastAPI后端
  chat.py          # 命令行界面
  tools/           # 工具（注册即用）
  rag/             # RAG检索
web/
  streamlit_app.py # 网页前端
docs/              # 知识库文档
```