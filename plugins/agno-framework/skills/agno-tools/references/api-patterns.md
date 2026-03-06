# Agno Tools API Reference

## Built-in Toolkits (Partial List)

| Category | Toolkit | Import |
|----------|---------|--------|
| Finance | YFinanceTools | `agno.tools.yfinance` |
| Search | WebSearchTools | `agno.tools.websearch` |
| Search | DuckDuckGoTools | `agno.tools.duckduckgo` |
| Math | CalculatorTools | `agno.tools.calculator` |
| Reasoning | ReasoningTools | `agno.tools.reasoning` |
| Files | FileTools | `agno.tools.file` |
| Shell | ShellTools | `agno.tools.shell` |
| Python | PythonTools | `agno.tools.python` |
| MCP | MCPTools | `agno.tools.mcp` |
| Email | EmailTools | `agno.tools.email_tools` |
| SQL | SQLTools | `agno.tools.sql` |
| CSV | CSVTools | `agno.tools.csv_tools` |
| JSON | JSONTools | `agno.tools.json_tools` |
| HTTP | APITools | `agno.tools.api` |
| Git | GitTools | `agno.tools.git` |

## @tool Decorator Options

```python
from agno.tools import tool

@tool(
    description="Override the docstring description",
    requires_confirmation=True,   # Require user approval before execution
)
def my_tool(arg: str) -> str:
    """This docstring is used if description is not set."""
    return "result"
```

## RunContext Properties

```python
from agno.run import RunContext

def my_tool(run_context: RunContext, arg: str) -> str:
    # Access session state
    state = run_context.session_state

    # Read state
    value = state.get("key", "default")

    # Write state
    state["key"] = "new_value"

    return "result"
```

## MCP Tool Integration

```python
from agno.tools.mcp import MCPTools

# Connect via URL (SSE)
mcp = MCPTools(url="http://localhost:3000/mcp")

# Use with agent
agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[mcp],
)
```

## Human-in-the-Loop Pattern

```python
from agno.tools import tool

@tool(requires_confirmation=True)
def dangerous_action(target: str) -> str:
    """Perform a dangerous action. User must confirm."""
    return f"Action performed on {target}"

agent = Agent(tools=[dangerous_action])
response = agent.run("Do the dangerous thing on X")

if response.active_requirements:
    for req in response.active_requirements:
        if req.needs_confirmation:
            # Show user what's about to happen
            print(f"Tool: {req.tool_execution.tool_name}")
            print(f"Args: {req.tool_execution.tool_args}")
            req.confirm()  # or req.reject()

    response = agent.continue_run(
        run_id=response.run_id,
        requirements=response.requirements,
    )
```
