# LangChain Agents — AI-5 Internship Project

A tool-using AI agent built with **LangChain, LangGraph, and Google Gemini**. The agent can answer questions directly, perform arithmetic using a calculator tool, search the web using Tavily, and combine multiple tools to complete multi-step tasks.

## Features

- **Calculator tool:** Safely evaluates supported arithmetic expressions without using Python's `eval()`.
- **Web search tool:** Retrieves web search results through Tavily.
- **Tool selection:** Uses tools when needed and answers directly when a tool is unnecessary.
- **Multi-step execution:** Supports tasks requiring more than one tool call.
- **Execution tracing:** Displays tool requests, arguments, tool results, and the final answer.
- **Error handling:** Provides readable errors for missing credentials and failed search requests.
- **Automated tests:** Tests the calculator, search tool, and agent behavior.

## Tech Stack

- Python 3.11
- LangChain
- LangGraph
- Google Gemini API
- Tavily Search API
- pytest
- python-dotenv
- Python logging

## Project Structure

```text
AI-5 - LangChain Agents/
├── app/
│   ├── tools/
│   │   ├── calculator.py
│   │   └── web_search.py
│   ├── utils/
│   │   └── tracing.py
│   ├── agent.py
│   └── config.py
├── tests/
│   ├── test_calculator.py
│   ├── test_web_search.py
│   ├── test_agent.py
│   └── test_error_handling.py
├── examples/
│   └── sample_runs.md
├── logs/
├── .env.example
├── .gitignore
├── LICENSE
├── main.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "AI-5 - LangChain Agents"
```

Replace the placeholder with the actual repository URL after creating your GitHub repository.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root, using `.env.example` as a reference:

```dotenv
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Obtain credentials from the official Google AI Studio and Tavily websites. Never commit your actual API keys or `.env` file to GitHub.

## Run the Agent

```bash
python main.py
```

Enter a question when prompted. The agent will display its tool execution trace when tools are used.

Example prompts:

```text
Calculate 18475 * 3629 - 47281. Use the calculator tool.

Search the web for the official LangChain documentation
explaining create_agent.

Explain what an AI agent is in exactly two sentences.
Do not use any tools.

Search for the official LangChain create_agent documentation.
Then calculate how many minutes are in 3.5 days.
Use both tools and show the formula and result.
```

## Example Execution Trace

The following illustrates the observed calculator execution:

```text
[TOOL REQUEST] calculator
Expression: 18475 * 3629 - 47281

[TOOL RESULT] calculator
66998494

Final answer: 66,998,494
```

A multi-step test also demonstrated the agent using the web search tool and calculator tool in the same task. The calculation was:

```text
3.5 × 24 × 60 = 5040 minutes
```

See [`examples/sample_runs.md`](examples/sample_runs.md) for the documented live demonstrations and test results.

## Run Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

The latest recorded test run passed **26 tests**. The tests include calculator validation, mocked web-search behavior, and agent behavior.

The web-search failure tests use mocks; they do not imply that a live API outage was deliberately reproduced.

## Error Handling and Limitations

- Missing API credentials produce actionable error messages.
- Web-search failures are handled gracefully.
- Search results may be irrelevant or inconclusive; the agent should communicate uncertainty instead of treating a lack of evidence as proof that something does not exist.
- Gemini and external search services depend on network connectivity, API availability, rate limits, and account quotas.
- Model responses and tool selection are not guaranteed to be perfect.

## AI Declaration

AI assistance was used during development for guidance, implementation support, debugging, and documentation. The code was tested, and the project author is responsible for understanding the implementation, validating its behavior, and explaining its design decisions.

## Learning Outcomes

- Building tool-enabled AI agents with LangChain.
- Connecting LLMs to external tools.
- Implementing calculator and web-search tools.
- Supporting multi-step tool execution.
- Logging visible tool activity.
- Testing tool behavior and handling failures.
- Documenting reproducible examples and project setup.

## License

See the [`LICENSE`](LICENSE) file for licensing details.
