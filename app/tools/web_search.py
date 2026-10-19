
"""Tavily-powered web search tool for the LangChain agent."""

import logging
import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch

logger = logging.getLogger(__name__)

load_dotenv()


@tool
def web_search(query: str) -> str:
    """Search the live web for current facts, recent developments, and reliable sources.

    Use this tool when a question requires up-to-date information or external
    evidence unavailable from the model's built-in knowledge.
    Provide a specific, descriptive search query.
    """
    if not query or not query.strip():
        return "Search error: query cannot be empty."

    if not os.getenv("TAVILY_API_KEY"):
        return "Search error: TAVILY_API_KEY is not configured."

    try:
        search = TavilySearch(max_results=5)
        results = search.invoke({"query": query.strip()})

        if not results:
            return "No search results found."

        if isinstance(results, dict):
            results = results.get("results", results)

        if isinstance(results, list):
            formatted = []
            for item in results:
                if isinstance(item, dict):
                    title = item.get("title", "Untitled")
                    url = item.get("url", "URL unavailable")
                    content = item.get("content", "No summary available")
                    formatted.append(
                        f"Title: {title}\nURL: {url}\nSummary: {content}"
                    )
                else:
                    formatted.append(str(item))

            return "\n\n".join(formatted) or "No search results found."

        return str(results)

    except Exception:
        logger.exception("Web search failed")
        return "Search error: the web search service failed. Please try again."
