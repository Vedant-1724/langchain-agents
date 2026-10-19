
"""Tests for LangChain agent tool orchestration."""

from unittest.mock import patch

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.agent import SYSTEM_PROMPT, calculator
from app.tools.web_search import web_search


class FakeToolCallingModel(BaseChatModel):
    """Return predefined responses and support LangChain tool binding."""

    responses: list
    response_index: int = 0

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        """Accept the tools registered by the agent."""
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        """Return the next predefined AI message."""

        if self.response_index >= len(self.responses):
            raise AssertionError("The fake model ran out of responses.")

        response = self.responses[self.response_index]
        self.response_index += 1

        if isinstance(response, str):
            response = AIMessage(content=response)

        return ChatResult(
            generations=[ChatGeneration(message=response)]
        )

    @property
    def _llm_type(self) -> str:
        return "fake-tool-calling-model"


def make_test_agent(responses):
    """Build an agent using predefined fake model responses."""

    fake_model = FakeToolCallingModel(responses=responses)

    return create_agent(
        model=fake_model,
        tools=[calculator, web_search],
        system_prompt=SYSTEM_PROMPT,
    )


def test_agent_answers_without_using_tools():
    agent = make_test_agent(
        ["A variable stores a value in a program."]
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is a variable?"}]}
    )

    assert result["messages"][-1].content == (
        "A variable stores a value in a program."
    )
    assert not any(
        isinstance(message, ToolMessage)
        for message in result["messages"]
    )


def test_agent_executes_calculator_tool():
    agent = make_test_agent(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "calculator",
                        "args": {"expression": "18 * 7"},
                        "id": "calculator_call_1",
                        "type": "tool_call",
                    }
                ],
            ),
            "18 multiplied by 7 is 126.",
        ]
    )

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "Calculate 18 multiplied by 7."}
            ]
        }
    )

    tool_results = [
        message
        for message in result["messages"]
        if isinstance(message, ToolMessage)
    ]

    assert len(tool_results) == 1
    assert tool_results[0].name == "calculator"
    assert tool_results[0].content == "126"
    assert "126" in result["messages"][-1].content


def test_agent_executes_web_search_tool():
    fake_results = {
        "results": [
            {
                "title": "Example AI Update",
                "url": "https://example.com/ai-update",
                "content": "A sample summary about an AI update.",
            }
        ]
    }

    with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
        with patch("app.tools.web_search.TavilySearch") as mock_search:
            mock_search.return_value.invoke.return_value = fake_results

            agent = make_test_agent(
                [
                    AIMessage(
                        content="",
                        tool_calls=[
                            {
                                "name": "web_search",
                                "args": {"query": "latest AI developments"},
                                "id": "web_search_call_1",
                                "type": "tool_call",
                            }
                        ],
                    ),
                    "The search returned an example AI update.",
                ]
            )

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "Find the latest AI developments.",
                        }
                    ]
                }
            )

    tool_results = [
        message
        for message in result["messages"]
        if isinstance(message, ToolMessage)
    ]

    assert len(tool_results) == 1
    assert tool_results[0].name == "web_search"
    assert "Example AI Update" in tool_results[0].content
    mock_search.return_value.invoke.assert_called_once()


def test_agent_handles_web_search_configuration_error():
    agent = make_test_agent(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "web_search",
                        "args": {"query": "latest AI developments"},
                        "id": "web_search_call_2",
                        "type": "tool_call",
                    }
                ],
            ),
            "I couldn't search the web because the search API key is missing.",
        ]
    )

    with patch.dict("os.environ", {}, clear=True):
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Search for the latest AI developments.",
                    }
                ]
            }
        )

    tool_results = [
        message
        for message in result["messages"]
        if isinstance(message, ToolMessage)
    ]

    assert len(tool_results) == 1
    assert tool_results[0].name == "web_search"
    assert "TAVILY_API_KEY is not configured" in tool_results[0].content
    assert "couldn't search the web" in result["messages"][-1].content.lower()
