# Storage API Patterns

## Storage Backend Comparison

| Backend | Import | Extras | Best For |
|---------|--------|--------|----------|
| SQLite | `agno.db.sqlite.SqliteDb` | (base) | Development |
| PostgreSQL | `agno.db.postgres.PostgresDb` | `agno[postgres]` | Production |
| Redis | `agno.db.redis.RedisDb` | `agno[redis]` | High-throughput |
| MongoDB | `agno.db.mongo.MongoDb` | `agno[mongodb]` | Document-oriented |
| MySQL | `agno.db.mysql.MySQLDb` | `agno[mysql]` | MySQL environments |
| DynamoDB | `agno.db.dynamodb.DynamoDb` | `agno[dynamodb]` | AWS serverless |
| Firestore | `agno.db.firestore.FirestoreDb` | `agno[firestore]` | GCP serverless |
| ClickHouse | `agno.db.clickhouse.ClickHouseDb` | `agno[clickhouse]` | Analytics |

## SQLite Configuration

```python
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/agents.db")
```

## PostgreSQL Configuration

```python
from agno.db.postgres import PostgresDb

db = PostgresDb(
    db_url="postgresql+psycopg://user:pass@localhost:5432/mydb",
    table_name="agent_sessions",
)
```

## Full Agent Storage Parameters

```python
Agent(
    db=db,                               # Storage backend
    add_history_to_context=True,         # Include chat history in context
    num_history_runs=5,                  # Number of prior runs to include
    enable_session_summaries=True,       # Summarize old messages
    session_summary_num_runs=10,         # Summarize after N runs
    add_session_state_to_context=True,   # Include session state in context
)
```

## Session State Pattern

```python
from agno.run import RunContext

def my_tool(run_context: RunContext, arg: str) -> str:
    """Tool that reads/writes session state."""
    # Read
    value = run_context.session_state.get("key", "default")
    # Write
    run_context.session_state["key"] = "new_value"
    return f"Updated key to new_value"

agent = Agent(
    model="openai:gpt-4o",
    tools=[my_tool],
    session_state={"key": "initial"},
    add_session_state_to_context=True,
    db=db,
)

# Access state after run
response = agent.run("do something", session_id="s1")
state = agent.get_session_state()
```

## Session Summary Configuration

```python
agent = Agent(
    model="openai:gpt-4o",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    enable_session_summaries=True,      # Enable summarization
    session_summary_num_runs=5,         # Summarize after 5 runs
)
```

## Team Shared Storage

```python
db = SqliteDb(db_file="team.db")

# All members and team share one DB
team = Team(
    model="openai:gpt-4o",
    members=[
        Agent(name="A1", model="openai:gpt-4o", db=db),
        Agent(name="A2", model="openai:gpt-4o", db=db),
    ],
    db=db,
    add_history_to_context=True,
)
```
