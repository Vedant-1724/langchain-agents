
"""Display observable tool calls and results from agent execution."""

import logging

logger = logging.getLogger(__name__)


def display_trace(result: dict) -> None:
    """Print tool calls, tool results, and the final response."""

    messages = result.get("messages", [])

    print("\n" + "=" * 60)
    print("AGENT EXECUTION TRACE")
    print("=" * 60)

    for message in messages:
        message_type = type(message).__name__

        if message_type == "AIMessage":
            for call in getattr(message, "tool_calls", []):
                print(f"\n[TOOL REQUEST] {call.get('name')}")
                print(f"Arguments: {call.get('args')}")

        elif message_type == "ToolMessage":
            print(f"\n[TOOL RESULT] {message.name}")
            print(message.content)

    print("\n" + "=" * 60)

    if messages:
        final_message = messages[-1]

        if type(final_message).__name__ == "AIMessage":
            print("FINAL ANSWER")

            content = final_message.content

            if isinstance(content, list):
                text_parts = [
                    item["text"]
                    for item in content
                    if isinstance(item, dict)
                    and item.get("type") == "text"
                ]
                print("\n".join(text_parts))
            else:
                print(content)

    print("=" * 60 + "\n")
