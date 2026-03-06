# AgentOS API Reference

## Full AgentOS Constructor

```python
from agno.os import AgentOS

AgentOS(
    id="app-id",
    description="Application description",
    agents=[agent1, agent2],
    teams=[team1],
    workflows=[workflow1],
    knowledge=[knowledge1],
    tracing=True,                  # Enable request tracing
)
```

## Deployment Options

### Local Development
```python
agent_os.serve(app="module:app", reload=True)
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install "agno[os]"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7777"]
```

### Cloud Deployment
- **Serverless**: Cloud Run, App Runner, Azure Container Apps
- **Orchestrated**: ECS, GKE, AKS
- **PaaS**: Railway.app, Render, Heroku
- **Specialized**: Modal

## PostgreSQL Setup for Production

```python
from agno.db.postgres import PostgresDb

# Connection string format
db = PostgresDb(
    id="prod-db",
    db_url="postgresql+psycopg://user:password@host:5432/database"
)
```

### Docker Compose for Local PostgreSQL
```yaml
version: "3.8"
services:
  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: ai
      POSTGRES_PASSWORD: ai
      POSTGRES_DB: ai
    volumes:
      - pgdata:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "7777:7777"
    environment:
      DATABASE_URL: postgresql+psycopg://ai:ai@db:5432/ai
    depends_on:
      - db

volumes:
  pgdata:
```

## Control Plane

Connect to the Agno control plane at `https://app.agno.com/playground` for:
- Real-time agent interaction
- Session monitoring
- Memory and knowledge management
- Debugging and tracing

## API Key Configuration

```bash
# Required model API keys
export ANTHROPIC_API_KEY=sk-...
export OPENAI_API_KEY=sk-...

# Optional database URL
export DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db
```
