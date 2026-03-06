---
name: agentos-api-evals
description: |
  Interact with AgentOS Evals API endpoints using the AgentOSClient SDK.
  Use this skill to write ad-hoc Python scripts, tests, and automation
  for running accuracy and performance evaluations, listing eval runs,
  getting eval details, and managing evaluations. Trigger when: importing
  AgentOSClient to work with evals, writing scripts to benchmark agents,
  creating eval tests, or asking things like "run an accuracy eval on
  my agent" or "show me the latest eval results."
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "evals", "evaluations", "api", "client", "agno"]
---

# AgentOS Evals API

Use `agno.client.AgentOSClient` to run, list, and inspect agent evaluations on a remote AgentOS instance. Install with `pip install agno`.

## Prerequisites

Start an AgentOS server with agents:

```bash
pip install "agno[os,anthropic]"
export ANTHROPIC_API_KEY=sk-...
python start_agentos.py  # See agno-agentos skill
```

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

## Run Accuracy Evaluation

```python
import asyncio
from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    agent_id = config.agents[0].id

    eval_result = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.ACCURACY,
        input_text="What is 2 + 2?",
        expected_output="4",
    )

    if eval_result:
        print(f"Eval ID: {eval_result.id}")
        print(f"Type: {eval_result.eval_type}")
        print(f"Data: {eval_result.eval_data}")

asyncio.run(main())
```

## Run Performance Evaluation

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
    agent_id = config.agents[0].id

    eval_result = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.PERFORMANCE,
        input_text="Hello, how are you?",
        num_iterations=3,  # Run multiple times to measure performance
    )

    if eval_result:
        print(f"Eval ID: {eval_result.id}")
        print(f"Performance Data: {eval_result.eval_data}")
```

## List Evaluation Runs

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

The list endpoint supports filtering by:
- `agent_id`: Filter by agent
- `team_id`: Filter by team
- `workflow_id`: Filter by workflow
- `model_id`: Filter by model
- `type`: Filter by component type (`agent`, `team`, `workflow`)
- `eval_types`: Comma-separated eval types (`accuracy`, `performance`, `agent_as_judge`, `reliability`)
- `limit`, `page`: Pagination (default: 20 per page)
- `sort_by`, `sort_order`: Sorting (default: `created_at` desc)

## Get Evaluation Details

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # List first to get an ID
    evals = await client.list_eval_runs()
    if not evals.data:
        print("No evaluations found")
        return

    eval_run = await client.get_eval_run(evals.data[0].id)
    print(f"Eval ID: {eval_run.id}")
    print(f"Name: {eval_run.name}")
    print(f"Type: {eval_run.eval_type}")
    print(f"Agent: {eval_run.agent_id}")
    print(f"Model: {eval_run.model_id}")
    print(f"Data: {eval_run.eval_data}")
```

## Full Evaluation Workflow

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

- **Don't forget `await`** — all client methods are async
- **Don't hardcode agent IDs** — discover them from `aget_config()`
- **Don't skip error handling** — eval endpoints may fail if agents aren't configured properly
- **Don't use too many iterations** — performance evals with high `num_iterations` can be slow and expensive
- **Don't ignore eval data** — `eval_data` contains the actual evaluation results and metrics

## Further Reading

For advanced eval API patterns, read `references/api-patterns.md`.
