import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Mini-Agent", page_icon="🤖")
st.title("🤖 Mini-Agent")
st.caption("本地文档检索 · 工具调用 · 多轮对话")

# 初始化会话状态
if "history" not in st.session_state:
    st.session_state.history = []
if "last_trace" not in st.session_state:
    st.session_state.last_trace = ""

# 侧边栏
with st.sidebar:
    st.header("设置")
    system_prompt = st.text_area(
        "系统提示词",
        value="你是一个简洁、友好的 AI 助手。回答尽量控制在三句话以内。",
        height=100,
    )
    if st.button("清空对话"):
        st.session_state.history = []
        st.session_state.last_trace = ""
        st.rerun()

    st.divider()
    st.subheader("最近调用记录")
    st.text(st.session_state.last_trace or "（暂无）")

# 显示历史对话
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 输入框
user_input = st.chat_input("说点什么...")
if user_input:
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)

    # 调后端
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                resp = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": user_input,
                        "history": st.session_state.history[:-1]
                        if st.session_state.history
                        and st.session_state.history[-1]["role"] == "user"
                        else st.session_state.history,
                        "system_prompt": system_prompt,
                    },
                    timeout=60,
                )
                data = resp.json()
                st.write(data["reply"])

                st.session_state.history = data["history"]
                st.session_state.last_trace = data["trace"]

            except requests.RequestException as e:
                st.error(f"请求失败：{e}")