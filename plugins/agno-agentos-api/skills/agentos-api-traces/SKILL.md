---
name: agentos-api-traces
description: |
  Interact with AgentOS Traces API endpoints using the AgentOSClient SDK.
  For standard operations (listing traces, getting trace details, viewing
  stats), use the provided CLI script first. Only write custom Python when
  the script cannot handle the use case (e.g., debugging workflows that
  chain agent runs with trace inspection, custom filtering, or integration
  tests). Trigger when: importing AgentOSClient to work with traces,
  writing scripts to debug agent runs, creating trace tests, or asking
  things like "show me the traces from my last agent run" or "how many
  tokens did my agent use?"
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "traces", "tracing", "api", "client", "agno"]
---

# AgentOS Traces API

Use `agno.client.AgentOSClient` to list and inspect execution traces on a remote AgentOS instance. Traces provide observability into agent execution flows, model invocations, token usage, tool calls, and errors.

## Prerequisites

Start an AgentOS server with tracing enabled:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS

db = SqliteDb(db_file="tmp/app.db")
agent = Agent(
    name="Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
)

agent_os = AgentOS(
    agents=[agent],
    tracing=True,  # Enable tracing
)
agent_os.serve()
```

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing traces, getting
trace details, and viewing session statistics — all from the command line
with no custom code needed.

The script is at: `scripts/view_traces.py`

### List recent traces

```bash
uv run scripts/view_traces.py --base-url http://localhost:7777
```

### Limit the number of traces shown

```bash
uv run scripts/view_traces.py --base-url http://localhost:7777 --limit 5
```

### Get detailed info for a specific trace

```bash
uv run scripts/view_traces.py --base-url http://localhost:7777 \
  --trace-id abc-123
```

### View trace statistics grouped by session

```bash
uv run scripts/view_traces.py --base-url http://localhost:7777 --stats
```

### Full CLI reference

```
uv run scripts/view_traces.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Debugging workflows** that chain agent runs with trace inspection
- **Custom filtering** by user_id, pagination, or sorting
- **Programmatic span inspection** (e.g., summing token usage across spans)
- **Integration tests** that assert on trace content
- **Automated monitoring** with custom retry or polling logic

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/traces` | List traces (paginated, filterable) |
| GET | `/traces/{trace_id}` | Get trace or span detail |
| GET | `/traces/stats/sessions` | Get trace statistics by session |

## Custom Python Examples

### Using Traces for Debugging

Chain an agent run with trace inspection to debug execution:

```python
import asyncio
from agno.client import AgentOSClient

async def debug_agent_run():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    agent_id = config.agents[0].id

    # Run an agent
    result = await client.run_agent(
        agent_id=agent_id,
        message="Search for recent AI news",
        session_id="debug-session",
    )

    # List traces to find the execution trace
    traces = await client.list_traces()
    for trace in traces.data[:5]:
        print(f"Trace: {trace.trace_id}")

        # Get detailed trace info
        detail = await client.get_trace(trace.trace_id)
        if hasattr(detail, "spans"):
            for span in detail.spans or []:
                print(f"  {span.name}: {span.duration_ms}ms")

asyncio.run(debug_agent_run())
```

### Custom Filtering and Pagination

Supports filtering by:
- `user_id`: Filter by user
- `limit`, `page`: Pagination
- `sort_by`, `sort_order`: Sorting

### Programmatic Span Inspection

Sum token usage across all spans in a trace:

```python
async def total_tokens(client: AgentOSClient, trace_id: str) -> int:
    trace = await client.get_trace(trace_id)
    spans = getattr(trace, "spans", None) or []
    return sum(getattr(s, "total_tokens", 0) or 0 for s in spans)
```

Traces provide insight into:
- **Agent execution flows** — the sequence of steps an agent takes
- **Model invocations and token usage** — which models were called and how many tokens were used
- **Tool calls and their results** — which tools were invoked and what they returned
- **Errors and performance bottlenecks** — where things went wrong or slowed down

## Anti-Patterns

- **Don't write custom Python for basic operations** — use the CLI script
- **Don't forget `tracing=True`** on AgentOS — tracing must be explicitly enabled
- **Don't poll traces in tight loops** — use reasonable intervals when monitoring
- **Don't ignore token usage** — traces are valuable for cost monitoring
- **Don't forget pagination** — use `limit` and `page` for large trace volumes

## Further Reading

For advanced tracing patterns, read `references/api-patterns.md`.
