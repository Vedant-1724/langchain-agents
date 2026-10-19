
"""Tests for the Tavily web search tool."""

from unittest.mock import patch

from app.tools.web_search import web_search


def test_empty_query_returns_error():
    result = web_search.invoke({"query": "   "})
    assert "cannot be empty" in result


def test_missing_api_key_returns_error():
    with patch.dict("os.environ", {}, clear=True):
        result = web_search.invoke({"query": "latest AI news"})
    assert "TAVILY_API_KEY is not configured" in result


def test_successful_search_formats_results():
    fake_results = {
        "results": [
            {
                "title": "Example Article",
                "url": "https://example.com/article",
                "content": "An example search result.",
            }
        ]
    }

    with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
        with patch(
            "app.tools.web_search.TavilySearch"
        ) as mock_search:
            mock_search.return_value.invoke.return_value = fake_results

            result = web_search.invoke({"query": "example topic"})

    assert "Example Article" in result
    assert "https://example.com/article" in result
    assert "An example search result." in result


def test_search_failure_is_handled_gracefully():
    with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
        with patch(
            "app.tools.web_search.TavilySearch"
        ) as mock_search:
            mock_search.return_value.invoke.side_effect = RuntimeError(
                "Simulated search failure"
            )

            result = web_search.invoke({"query": "example topic"})

    assert "Search error" in result
    assert "try again" in result
