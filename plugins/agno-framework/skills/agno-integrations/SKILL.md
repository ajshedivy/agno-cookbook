---
name: agno-integrations
description: |
  Integrate Agno agents with observability platforms, A2A protocol, and
  external services. Covers OpenTelemetry, Langfuse, Arize Phoenix,
  Agent-to-Agent protocol, and Discord bots. Trigger this skill when:
  adding observability to agents, setting up tracing, integrating with
  Langfuse or similar platforms, or asking "how do I monitor my agents?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["observability", "tracing", "integrations", "langfuse", "a2a", "agno"]
---

# Integrate Agno Agents

Connect agents to observability platforms, external services, and other agent systems. Install with `pip install agno`.

## Observability with OpenTelemetry

### Langfuse via OpenInference

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.instrumentation.agno import AgnoInstrumentor

# Configure Langfuse OTLP endpoint
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://cloud.langfuse.com/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = (
    f"Authorization=Basic {os.environ['LANGFUSE_AUTH']}"
)

# Set up tracing
provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter())
)
trace.set_tracer_provider(provider)

# Instrument Agno
AgnoInstrumentor().instrument()

# Now all agent runs are automatically traced
from agno.agent import Agent

agent = Agent(
    model="openai:gpt-4o",
    markdown=True,
)

agent.print_response("Hello!", stream=True)
```

### Arize Phoenix (Local)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.instrumentation.agno import AgnoInstrumentor

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
    )
)
trace.set_tracer_provider(provider)

AgnoInstrumentor().instrument()
```

### Required Dependencies

```bash
pip install "agno[opentelemetry]"
pip install openinference-instrumentation-agno
pip install opentelemetry-exporter-otlp
```

## Agent-to-Agent (A2A) Protocol

Agno supports the A2A protocol for inter-agent communication across systems:

```python
from agno.agent import Agent
from agno.tools.a2a import A2ATools

# Connect to a remote A2A-compatible agent
agent = Agent(
    model="openai:gpt-4o",
    tools=[A2ATools(url="http://remote-agent:8000/a2a")],
    instructions=["Use the remote agent for specialized tasks."],
)

agent.print_response("Ask the remote agent to analyze this data.", stream=True)
```

## MCP (Model Context Protocol)

Connect to MCP servers for external tool access:

```python
from agno.agent import Agent
from agno.tools.mcp import MCPTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[MCPTools(url="http://localhost:3000/mcp")],
)

agent.print_response("Use the MCP tools to help me.", stream=True)
```

## Slack Integration

```python
from agno.agent import Agent
from agno.tools.slack import SlackTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[SlackTools()],
    instructions=["Help manage Slack messages and channels."],
)
```

## GitHub Integration

```python
from agno.agent import Agent
from agno.tools.github import GithubTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[GithubTools()],
    instructions=["Help manage GitHub issues and PRs."],
)
```

## Email Integration

```python
from agno.agent import Agent
from agno.tools.gmail import GmailTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[GmailTools()],
    instructions=["Help manage emails."],
)
```

## Custom Observability Hook

Log agent events programmatically:

```python
from agno.agent import Agent

def on_run_complete(run_response):
    print(f"Run {run_response.run_id} completed")
    if run_response.metrics:
        print(f"  Tokens: {run_response.metrics.total_tokens}")
        print(f"  Duration: {run_response.metrics.time_to_first_token}s")

agent = Agent(
    model="openai:gpt-4o",
    markdown=True,
)

response = agent.run("Hello!")
on_run_complete(response)
```

## Anti-Patterns

- **Don't instrument in production without sampling** — tracing every request adds overhead
- **Don't hardcode auth tokens** — use environment variables for Langfuse/Arize keys
- **Don't skip `AgnoInstrumentor().instrument()`** — it must be called before agent runs
- **Don't mix tracing backends** — pick one observability platform per deployment
- **Don't forget to install extras** — `agno[opentelemetry]` is required for tracing

## Further Reading

For advanced observability patterns and integration guides, read `references/api-patterns.md`.
