# agentos-serve

Spin up [AgentOS](https://os.agno.com) from any Python file containing [Agno](https://github.com/agno-agi/agno) agents, teams, or workflows.

## Install

```bash
pip install agentos-serve
```

With common tool dependencies (DuckDuckGo, yfinance, exa, newspaper, SQL, DuckDB):

```bash
pip install agentos-serve[common-tools]
```

## Usage

```bash
# Serve a single agent file
agentos-serve my_agent.py

# Serve all agents in a directory
agentos-serve agents/

# Serve multiple paths
agentos-serve agents/ teams/ workflows/my_flow.py

# Custom port and name
agentos-serve my_agent.py --port 8080 --name "My AgentOS"
```

## CLI Options

| Option | Default | Description |
|---|---|---|
| `paths` | *(required)* | Python file(s) or directories to scan |
| `--port`, `-p` | `7777` | Server port |
| `--host` | `localhost` | Server host |
| `--name`, `-n` | auto-generated | AgentOS instance name |

## Extras

| Extra | Included packages |
|---|---|
| `common-tools` | `agno[ddg,yfinance,exa,newspaper,sql,duckdb]` |
| `mcp` | `agno[mcp]` |

For model providers and other agno extras, install them directly:

```bash
pip install agno[openai]
pip install agno[anthropic]
pip install agno[google]
```
