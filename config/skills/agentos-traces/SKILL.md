---
name: agentos-traces
description: |
  Interact with AgentOS Traces API endpoints using the AgentOSClient SDK.
  Covers listing traces, getting trace details, and retrieving trace
  statistics by session. Trigger this skill when: monitoring agent
  execution, debugging traces, viewing token usage, or asking "how do I
  view traces through the API?"
license: Apache-2.0
metadata:
  version: "1.0.0"
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

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/traces` | List traces (paginated, filterable) |
| GET | `/traces/{trace_id}` | Get trace or span detail |
| GET | `/traces/stats/sessions` | Get trace statistics by session |

## List Traces

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    traces = await client.list_traces()
    print(f"Found {len(traces.data)} traces")

    for trace in traces.data:
        print(f"  Trace ID: {trace.trace_id}")
        print(f"  Agent: {trace.agent_id}")
        print(f"  Session: {trace.session_id}")
        print(f"  Created: {trace.created_at}")

asyncio.run(main())
```

Traces provide insight into:
- **Agent execution flows** — the sequence of steps an agent takes
- **Model invocations and token usage** — which models were called and how many tokens were used
- **Tool calls and their results** — which tools were invoked and what they returned
- **Errors and performance bottlenecks** — where things went wrong or slowed down

## Get Trace Detail

Retrieve the full hierarchy of a specific trace including all spans:

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    trace = await client.get_trace("trace-id-here")
    print(f"Trace ID: {trace.trace_id}")
    print(f"Agent: {trace.agent_id}")
    print(f"Duration: {trace.duration_ms}ms")

    # Inspect spans within the trace
    if hasattr(trace, "spans") and trace.spans:
        for span in trace.spans:
            print(f"  Span: {span.name}")
            print(f"    Duration: {span.duration_ms}ms")
            print(f"    Tokens: {span.total_tokens}")
```

## Get Trace Statistics by Session

Retrieve aggregated trace statistics grouped by session ID:

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    stats = await client.get_trace_stats_by_session()
    print(f"Found stats for {len(stats.data)} sessions")

    for entry in stats.data:
        print(f"  Session: {entry.session_id}")
        print(f"    Total traces: {entry.total_traces}")
        print(f"    First trace: {entry.first_trace_at}")
        print(f"    Last trace: {entry.last_trace_at}")
```

Supports filtering by:
- `user_id`: Filter by user
- `limit`, `page`: Pagination
- `sort_by`, `sort_order`: Sorting

## Using Traces for Debugging

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

## Anti-Patterns

- **Don't forget `tracing=True`** on AgentOS — tracing must be explicitly enabled
- **Don't poll traces in tight loops** — use reasonable intervals when monitoring
- **Don't ignore token usage** — traces are valuable for cost monitoring
- **Don't forget pagination** — use `limit` and `page` for large trace volumes

## Further Reading

For advanced tracing patterns, read `references/api-patterns.md`.
