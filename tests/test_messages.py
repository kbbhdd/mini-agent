from app.messages import DEFAULT_SYSTEM_PROMPT, build_messages


def test_build_messages_uses_default_system_prompt():
    history = [{"role": "user", "content": "你好"}]
    messages = build_messages(history)

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == DEFAULT_SYSTEM_PROMPT
    assert messages[1] == {"role": "user", "content": "你好"}
    assert len(messages) == 2


def test_build_messages_uses_custom_system_prompt():
    history = [{"role": "user", "content": "你好"}]
    messages = build_messages(history, "你是数学老师")

    assert messages[0]["content"] == "你是数学老师"
    assert messages[1]["content"] == "你好"


def test_build_messages_does_not_modify_history():
    history = [{"role": "user", "content": "你好"}]
    build_messages(history)

    assert history == [{"role": "user", "content": "你好"}]