# AgentOS Traces API Reference

## Complete Trace Endpoints

### GET /traces
List execution traces with pagination and filtering.

**Query Parameters:**
- `agent_id` (string): Filter by agent
- `session_id` (string): Filter by session
- `user_id` (string): Filter by user
- `limit` (integer, default: 20): Items per page
- `page` (integer, default: 1): Page number
- `sort_by` (string, default: `created_at`): Sort field
- `sort_order` (string, default: `desc`): Sort direction

**Response:** Paginated list of trace objects.

### GET /traces/{trace_id}
Get detailed trace or span information including the full hierarchy.

**Path Parameters:**
- `trace_id` (string, required): Trace identifier

**Response:** Trace detail with spans showing:
- Model invocations and token usage
- Tool calls and their results
- Execution duration per span
- Error information

### GET /traces/stats/sessions
Get aggregated trace statistics grouped by session ID.

**Query Parameters:**
- `user_id` (string): Filter by user
- `limit` (integer): Items per page
- `page` (integer): Page number
- `sort_by`, `sort_order`: Sorting

**Response:** Aggregated stats per session:
- `session_id`: Session identifier
- `total_traces`: Number of traces
- `first_trace_at`: Timestamp of first trace
- `last_trace_at`: Timestamp of last trace
- Associated user and agent information

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# List traces
traces = await client.list_traces()
# traces.data — list of trace objects

# Get trace detail
trace = await client.get_trace("trace-id")
# trace.trace_id, trace.spans, trace.duration_ms

# Get stats by session
stats = await client.get_trace_stats_by_session()
# stats.data — aggregated statistics
```

## What Traces Capture

| Category | Details |
|----------|---------|
| Agent execution flows | Sequence of steps, decision points |
| Model invocations | Which models called, parameters used |
| Token usage | Input/output tokens per model call |
| Tool calls | Tools invoked, arguments, return values |
| Errors | Exceptions, timeouts, failures |
| Performance | Duration per span, total execution time |

## Enabling Tracing

Tracing must be explicitly enabled on the AgentOS instance:

```python
agent_os = AgentOS(
    agents=[agent],
    tracing=True,  # Required
)
```
