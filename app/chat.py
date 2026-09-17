from rich.console import Console
from rich.panel import Panel
from openai import OpenAIError

from app.llm import chat_stream

console = Console()

SYSTEM_PROMPT = "你是一个简洁、友好的 AI 助手。回答尽量控制在三句话以内。"


def build_messages(history):
    return [{"role": "system", "content": SYSTEM_PROMPT}] + history


def main():
    console.print(Panel.fit(
        "[bold cyan]Mini-Agent 聊天[/bold cyan]\n"
        "输入内容开始对话，输入 [yellow]exit[/yellow] 或 [yellow]quit[/yellow] 退出。",
        border_style="cyan",
    ))

    history = []

    while True:
        try:
            user_input = console.input("\n[bold green]你：[/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]再见。[/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            console.print("[dim]再见。[/dim]")
            break

        history.append({"role": "user", "content": user_input})

        console.print("[bold magenta]AI：[/bold magenta]", end="")
        reply = ""
        try:
            for piece in chat_stream(build_messages(history)):
                console.print(piece, end="", soft_wrap=True)
                reply += piece
        except OpenAIError as e:
            console.print(f"\n[red]调用模型出错：{e}[/red]")
            history.pop()
            continue

        console.print()
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()