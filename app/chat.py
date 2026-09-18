from rich.console import Console
from rich.panel import Panel
from openai import OpenAIError

from app.llm import LLMClient
from app.messages import DEFAULT_SYSTEM_PROMPT, build_messages

console = Console()

HELP_TEXT = """
命令：
  /system <内容>   修改系统提示词
  /system          查看当前系统提示词
  /reset           恢复默认系统提示并清空对话
  clear            清空对话历史
  help             查看帮助
  exit / quit      退出
"""


def main():
    console.print(Panel.fit(
        "[bold cyan]Mini-Agent 聊天[/bold cyan]\n"
        "输入内容开始对话。输入 [yellow]help[/yellow] 查看命令。",
        border_style="cyan",
    ))

    llm = LLMClient()
    history = []
    system_prompt = DEFAULT_SYSTEM_PROMPT

    while True:
        try:
            user_input = console.input("\n[bold green]你：[/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]再见。[/dim]")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        if lower in {"exit", "quit"}:
            console.print("[dim]再见。[/dim]")
            break

        if lower == "help":
            console.print(HELP_TEXT)
            continue

        if lower == "clear":
            history.clear()
            console.print("[dim]对话已清空。[/dim]")
            continue

        if lower == "/reset":
            history.clear()
            system_prompt = DEFAULT_SYSTEM_PROMPT
            console.print("[dim]已恢复默认系统提示并清空对话。[/dim]")
            continue

        if lower == "/system":
            console.print(f"[cyan]当前系统提示：[/cyan]{system_prompt}")
            continue

        if lower.startswith("/system "):
            system_prompt = user_input[len("/system "):].strip()
            console.print("[dim]系统提示已更新。[/dim]")
            continue

        history.append({"role": "user", "content": user_input})

        console.print("[bold magenta]AI：[/bold magenta]", end="")
        reply = ""
        try:
            for piece in llm.chat_stream(build_messages(history, system_prompt)):
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