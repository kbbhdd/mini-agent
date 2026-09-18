DEFAULT_SYSTEM_PROMPT = "你是一个简洁、友好的 AI 助手。回答尽量控制在三句话以内。"


def build_messages(history, system_prompt=None):
    prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
    return [{"role": "system", "content": prompt}] + list(history)