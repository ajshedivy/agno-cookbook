# Integrations API Patterns

## OpenTelemetry Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.instrumentation.agno import AgnoInstrumentor

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
AgnoInstrumentor().instrument()
```

## Observability Platforms

| Platform | Endpoint | Auth |
|----------|----------|------|
| Langfuse | `https://cloud.langfuse.com/api/public/otel` | `Authorization=Basic <key>` |
| Arize Phoenix | `http://localhost:6006/v1/traces` | None (local) |
| Jaeger | `http://localhost:4318/v1/traces` | None (local) |

## Dependencies

```bash
pip install "agno[opentelemetry]"
pip install openinference-instrumentation-agno
pip install opentelemetry-exporter-otlp-proto-http   # HTTP
pip install opentelemetry-exporter-otlp-proto-grpc   # gRPC
```

## Built-in Tool Integrations

| Integration | Import | Extras |
|-------------|--------|--------|
| Slack | `agno.tools.slack.SlackTools` | `agno[slack]` |
| GitHub | `agno.tools.github.GithubTools` | `agno[github]` |
| Gmail | `agno.tools.gmail.GmailTools` | `agno[gmail]` |
| Notion | `agno.tools.notion.NotionTools` | `agno[notion]` |
| Todoist | `agno.tools.todoist.TodoistTools` | `agno[todoist]` |
| YouTube | `agno.tools.youtube.YouTubeTools` | `agno[youtube]` |
| Google Maps | `agno.tools.googlemaps.GoogleMapsTools` | `agno[googlemaps]` |

## MCP Integration

```python
from agno.tools.mcp import MCPTools

# SSE transport
agent = Agent(
    model="openai:gpt-4o",
    tools=[MCPTools(url="http://localhost:3000/mcp")],
)

# Stdio transport
agent = Agent(
    model="openai:gpt-4o",
    tools=[MCPTools(command="npx", args=["-y", "@modelcontextprotocol/server-sqlite"])],
)
```

## A2A Protocol

```python
from agno.tools.a2a import A2ATools

agent = Agent(
    model="openai:gpt-4o",
    tools=[A2ATools(url="http://remote-agent:8000/a2a")],
)
```

## Accessing Run Metrics

```python
response = agent.run("Hello")
if response.metrics:
    print(f"Total tokens: {response.metrics.total_tokens}")
    print(f"Input tokens: {response.metrics.input_tokens}")
    print(f"Output tokens: {response.metrics.output_tokens}")
    print(f"Time to first token: {response.metrics.time_to_first_token}")
```
