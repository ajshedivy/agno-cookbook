# AgentOS Evals API Reference

## Complete Eval Endpoints

### GET /eval-runs
List evaluation runs with pagination, filtering, and sorting.

**Query Parameters:**
- `agent_id` (string): Filter by agent
- `team_id` (string): Filter by team
- `workflow_id` (string): Filter by workflow
- `model_id` (string): Filter by model
- `type` (enum): Filter by component type — `agent`, `team`, `workflow`
- `eval_types` (string): Comma-separated eval types — `accuracy`, `agent_as_judge`, `performance`, `reliability`
- `limit` (integer, default: 20): Items per page
- `page` (integer, default: 1): Page number
- `sort_by` (string, default: `created_at`): Sort field
- `sort_order` (enum, default: `desc`): Sort direction
- `db_id` (string): Database identifier
- `table` (string): Table name

**Response:** Paginated list of eval run objects:
- `id`, `agent_id`, `model_id`, `model_provider`
- `name`, `eval_type`, `eval_data`, `eval_input`
- `created_at`, `updated_at`

### GET /eval-runs/{eval_id}
Get detailed evaluation run.

### POST /eval-runs
Execute a new evaluation.

**Body Parameters:**
- `agent_id` (string): Agent to evaluate
- `eval_type` (EvalType): Type of evaluation
- `input_text` (string): Input prompt
- `expected_output` (string): Expected output (for accuracy evals)
- `num_iterations` (integer): Number of runs (for performance evals)

### PATCH /eval-runs/{eval_id}
Update an evaluation run.

### DELETE /eval-runs
Delete evaluation runs.

## Evaluation Types

| Type | Import | Description |
|------|--------|-------------|
| `ACCURACY` | `EvalType.ACCURACY` | Compare output against expected |
| `PERFORMANCE` | `EvalType.PERFORMANCE` | Measure response time |
| `AGENT_AS_JUDGE` | `EvalType.AGENT_AS_JUDGE` | Use another agent to evaluate |
| `RELIABILITY` | `EvalType.RELIABILITY` | Test consistency across runs |

```python
from agno.db.schemas.evals import EvalType
```

## AgentOSClient Methods

```python
from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType

client = AgentOSClient(base_url="http://localhost:7777")

# Run eval
result = await client.run_eval(
    agent_id="agent-id",
    eval_type=EvalType.ACCURACY,
    input_text="What is 2 + 2?",
    expected_output="4",
)
# result.id, result.eval_type, result.eval_data

# Run performance eval
perf = await client.run_eval(
    agent_id="agent-id",
    eval_type=EvalType.PERFORMANCE,
    input_text="Hello",
    num_iterations=3,
)

# List
evals = await client.list_eval_runs()
# evals.data — list of eval run objects

# Get details
eval_run = await client.get_eval_run("eval-id")
# eval_run.id, eval_run.name, eval_run.eval_type, eval_run.eval_data
```

## Eval Data Schema

The `eval_data` field contains evaluation-specific results:

**Accuracy eval:**
- `status`: Pass/fail
- `expected_output`: What was expected
- `actual_output`: What the agent produced
- `tool_call_results`: Results from any tool calls

**Performance eval:**
- `iterations`: Number of runs
- `avg_duration_ms`: Average response time
- `min_duration_ms`: Fastest response
- `max_duration_ms`: Slowest response
- `avg_tokens`: Average token usage
