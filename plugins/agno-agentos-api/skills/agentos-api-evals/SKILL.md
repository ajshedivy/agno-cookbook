---
name: agentos-api-evals
description: |
  Interact with AgentOS Evals API endpoints. For standard operations
  (listing evals, running accuracy/performance evals, getting eval
  details), use the provided CLI script first. Only write custom Python
  when the script cannot handle the use case (e.g., advanced filtering,
  update/delete operations, chaining evals, agent-as-judge). Trigger
  when: running evaluations, listing eval runs, benchmarking agents,
  or asking things like "run an accuracy eval on my agent" or "show me
  the latest eval results."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "evals", "evaluations", "api", "client", "agno"]
---

# AgentOS Evals API

## Prerequisites

Start an AgentOS server with agents:

```bash
export ANTHROPIC_API_KEY=sk-...
uv run start_agentos.py  # See agno-agentos skill
```

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing evals, running
accuracy and performance evaluations, filtering by agent, and getting eval
details — all from the command line with no custom code needed.

The script is at: `scripts/run_evals.py`

### List all evaluation runs

```bash
uv run scripts/run_evals.py
```

### Run an accuracy evaluation

```bash
uv run scripts/run_evals.py \
  --agent-id my-agent \
  --accuracy --input "What is 2+2?" --expected "4"
```

### Run a performance evaluation

```bash
uv run scripts/run_evals.py \
  --agent-id my-agent \
  --performance --input "Hello" --iterations 3
```

### Get details for a specific eval

```bash
uv run scripts/run_evals.py --eval-id abc-123
```

### Filter evals by agent

```bash
uv run scripts/run_evals.py --agent-id my-agent
```

### Use a different server

```bash
uv run scripts/run_evals.py --base-url http://my-server:8000
```

### Full CLI reference

```
uv run scripts/run_evals.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Advanced filtering** (by team, workflow, model, eval type, pagination, sorting)
- **Update or delete** evaluation runs
- **Agent-as-judge or reliability** eval types (not supported by the CLI)
- **Chaining multiple evals** in a single script
- **Custom error handling** or retry logic
- **Integration tests** that assert on eval results programmatically

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/eval-runs` | List evaluation runs (paginated, filterable) |
| GET | `/eval-runs/{eval_id}` | Get evaluation run details |
| POST | `/eval-runs` | Execute evaluation |
| PATCH | `/eval-runs/{eval_id}` | Update evaluation run |
| DELETE | `/eval-runs` | Delete evaluation runs |

## Evaluation Types

| Type | Description |
|------|-------------|
| `accuracy` | Compare agent output against expected output |
| `performance` | Measure response time and throughput |
| `agent_as_judge` | Use another agent to evaluate quality |
| `reliability` | Test consistency across multiple runs |

## Custom Python Examples

### List with Advanced Filtering

The list endpoint supports filtering beyond what the CLI provides:

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    evals = await client.list_eval_runs()
    print(f"Found {len(evals.data)} evaluation runs")

    for eval_run in evals.data:
        print(f"  ID: {eval_run.id}")
        print(f"  Name: {eval_run.name}")
        print(f"  Type: {eval_run.eval_type}")
        print(f"  Agent: {eval_run.agent_id}")
```

Supported filter parameters:
- `agent_id`: Filter by agent
- `team_id`: Filter by team
- `workflow_id`: Filter by workflow
- `model_id`: Filter by model
- `type`: Filter by component type (`agent`, `team`, `workflow`)
- `eval_types`: Comma-separated eval types (`accuracy`, `performance`, `agent_as_judge`, `reliability`)
- `limit`, `page`: Pagination (default: 20 per page)
- `sort_by`, `sort_order`: Sorting (default: `created_at` desc)

### Chained Evaluation Workflow

Run multiple eval types and aggregate results in a single script:

```python
import asyncio
from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
    agent_id = config.agents[0].id

    # Run accuracy eval
    accuracy = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.ACCURACY,
        input_text="What is the capital of France?",
        expected_output="Paris",
    )
    print(f"Accuracy eval: {accuracy.id if accuracy else 'failed'}")

    # Run performance eval
    perf = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.PERFORMANCE,
        input_text="Hello",
        num_iterations=2,
    )
    print(f"Performance eval: {perf.id if perf else 'failed'}")

    # List all evaluations
    evals = await client.list_eval_runs()
    print(f"\nTotal evaluations: {len(evals.data)}")
    for e in evals.data:
        print(f"  {e.id}: {e.eval_type} — {e.name}")

asyncio.run(main())
```

## Anti-Patterns

- **Don't write custom Python for basic operations** — use the CLI script for listing, running accuracy/performance evals, and getting details
- **Don't forget `await`** — all client methods are async
- **Don't hardcode agent IDs** — discover them from `aget_config()` or the CLI script
- **Don't skip error handling** — eval endpoints may fail if agents aren't configured properly
- **Don't use too many iterations** — performance evals with high `num_iterations` can be slow and expensive
- **Don't ignore eval data** — `eval_data` contains the actual evaluation results and metrics

## Further Reading

For advanced eval API patterns, read `references/api-patterns.md`.
