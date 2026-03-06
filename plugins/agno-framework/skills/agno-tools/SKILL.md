---
name: agno-tools
description: |
  Create custom tools for Agno agents. Covers function tools, the @tool
  decorator, toolkit classes, RunContext for state access, and MCP tool
  integration. Trigger this skill when: writing custom agent tools,
  importing agno.tools, using @tool decorator, creating toolkit classes,
  or asking "how do I create tools for Agno agents?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["tools", "agno", "custom-tools", "mcp"]
---

# Create Agno Tools

Agno agents use tools to interact with external systems. You can use built-in toolkits, write plain functions, or use the `@tool` decorator.

## Function Tools (Simplest)

Any Python function can be a tool. Add type hints and a docstring for the agent to understand it:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude

def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72F, sunny"

agent = Agent(
    name="Weather Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[get_weather],
)

agent.print_response("What's the weather in NYC?", stream=True)
```

## Function Tools with RunContext

Access session state and agent context by accepting `run_context: RunContext` as the first parameter:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.run import RunContext

def add_to_list(run_context: RunContext, item: str) -> str:
    """Add an item to the shared list."""
    items = run_context.session_state.get("items", [])
    items.append(item)
    run_context.session_state["items"] = items
    return f"Added {item}. Total: {len(items)}"

def get_list(run_context: RunContext) -> str:
    """Get all items in the list."""
    items = run_context.session_state.get("items", [])
    return f"Items: {', '.join(items)}" if items else "List is empty"

agent = Agent(
    name="List Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[add_to_list, get_list],
    session_state={"items": []},
    add_session_state_to_context=True,
)
```

The `RunContext` parameter is automatically injected — the agent does not see it as a tool argument.

## @tool Decorator

Use `@tool` for additional control like requiring user confirmation:

```python
from agno.tools import tool

@tool(requires_confirmation=True)
def delete_file(path: str) -> str:
    """Delete a file. Requires user confirmation before executing."""
    import os
    os.remove(path)
    return f"Deleted {path}"

@tool(description="Send an email to a recipient")
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}: {subject}"
```

## Built-in Toolkits

Agno ships with 90+ built-in toolkits. Common ones:

```python
# Finance
from agno.tools.yfinance import YFinanceTools
agent = Agent(tools=[YFinanceTools()])

# Web search
from agno.tools.websearch import WebSearchTools
agent = Agent(tools=[WebSearchTools()])

# Calculator
from agno.tools.calculator import CalculatorTools
agent = Agent(tools=[CalculatorTools()])

# Reasoning (chain-of-thought)
from agno.tools.reasoning import ReasoningTools
agent = Agent(tools=[ReasoningTools(add_instructions=True)])

# File operations
from agno.tools.file import FileTools
agent = Agent(tools=[FileTools(base_dir="./data")])

# Shell commands
from agno.tools.shell import ShellTools
agent = Agent(tools=[ShellTools()])

# Python code execution
from agno.tools.python import PythonTools
agent = Agent(tools=[PythonTools()])

# DuckDuckGo search
from agno.tools.duckduckgo import DuckDuckGoTools
agent = Agent(tools=[DuckDuckGoTools()])
```

## MCP Tool Integration

Connect to MCP servers to use external tools:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

agent = Agent(
    name="MCP Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[MCPTools(url="http://localhost:3000/mcp")],
)
```

## Combining Multiple Tool Sources

Agents accept a list of tools — mix toolkits, functions, and decorators:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools

def custom_lookup(ticker: str) -> str:
    """Look up custom data for a ticker."""
    return f"Custom data for {ticker}"

agent = Agent(
    name="Multi-Tool Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[
        YFinanceTools(),       # Toolkit instance
        CalculatorTools(),     # Another toolkit
        custom_lookup,         # Plain function
    ],
)
```

## Tool Docstrings Matter

The agent reads docstrings and type hints to understand tools. Write clear, specific descriptions:

```python
# Good
def search_orders(customer_id: str, status: str = "all") -> str:
    """Search orders for a customer. Returns order IDs, dates, and totals.

    Args:
        customer_id: The customer's unique ID
        status: Filter by status: "all", "pending", "shipped", "delivered"
    """

# Bad
def search(id: str) -> str:
    """Search stuff."""
```

## Anti-Patterns

- **Don't forget type hints** — the agent uses them to generate tool schemas
- **Don't skip docstrings** — the agent needs descriptions to know when to use tools
- **Don't use `run_context` as a regular parameter** — it must be the first parameter and is auto-injected
- **Don't return complex objects** — return strings; the agent processes text
- **Don't put `RunContext` in the docstring Args** — it's invisible to the agent

## Further Reading

For the full built-in tools listing and MCP patterns, read `references/api-patterns.md`.
