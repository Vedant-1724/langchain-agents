
"""Command-line entry point for the LangChain agent."""

import logging

from app.agent import get_agent
from app.config import validate_google_api_key
from app.utils.tracing import display_trace

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def main() -> None:
    """Run an interactive agent session."""

    try:
        validate_google_api_key()
        agent = get_agent()
    except Exception as exc:
        print(f"Configuration error: {exc}")
        return

    print("\nLangChain Tool-Using AI Agent")
    print("Tools: calculator, web_search")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\n[INFO] Sending request to Gemini...")
            result = agent.invoke(
                {"messages": [{"role": "user", "content": question}]}
            )
            print("[INFO] Agent execution completed.")
            display_trace(result)
        except Exception:
            logging.exception("Agent execution failed")
            print(
                "The agent encountered an error. "
                "Check the terminal logs and try again."
            )


if __name__ == "__main__":
    main()
