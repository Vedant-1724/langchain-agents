
"""Create the LangChain agent and register its tools."""

from functools import lru_cache

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import get_google_api_key
from app.tools.calculator import calculate
from app.tools.web_search import web_search
from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression accurately.

    Use this tool for arithmetic, percentages, large-number calculations,
    and expressions requiring exact computation. Supports +, -, *, /,
    //, %, **, parentheses and unary signs.
    """
    try:
        return str(calculate(expression))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return f"Calculator error: {exc}"


SYSTEM_PROMPT = """
You are a helpful AI assistant equipped with two tools: calculator and
web_search.

Guidelines:
1. Answer ordinary conceptual questions directly when no tool is needed.
2. Use calculator for arithmetic and calculations requiring accuracy.
3. Use web_search for current information and external factual evidence.
4. For multi-step tasks, use the appropriate tools in sequence and use
   their actual results in your final answer.
5. Never invent tool results, sources, or calculations.
6. If a tool returns an error, explain the limitation clearly and do not
   pretend the operation succeeded.
7. Distinguish retrieved facts from estimates and hypothetical scenarios.
8. Give concise, clear final answers.
9. If search results are irrelevant or inconclusive, say that the
   search did not find relevant evidence. Do not claim that something
   does not exist based on a single search.
10. Clearly distinguish tool output from conclusions or inferences.
"""


@lru_cache(maxsize=1)
def get_agent():
    """Build and cache the configured LangChain agent."""


    model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=get_google_api_key(),
        max_retries=3,
        timeout=30,
    )

    tools = [calculator, web_search]

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
