"""Spin up AgentOS from any cookbook example file(s).

Dynamically imports the target file(s), discovers Agent / Team / Workflow
instances at module level, and serves them via AgentOS.

Usage:
    uv run agentos cookbook/03_teams/02_modes/broadcast/01_basic.py
    uv run agentos cookbook/02_agents/01_quickstart/basic_agent.py -p 8080
    uv run agentos cookbook/02_agents/basic.py cookbook/03_teams/.../01_basic.py
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------


def load_module(filepath: str) -> Any:
    """Dynamically import a Python file, skipping its ``__main__`` block."""
    path = Path(filepath).resolve()
    if not path.exists():
        print(f"Error: file not found: {filepath}")
        sys.exit(1)
    if path.suffix != ".py":
        print(f"Error: not a Python file: {filepath}")
        sys.exit(1)

    # Ensure project root is importable (for cookbook_config)
    root = str(REPO_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)

    # Ensure the file's own directory is importable (sibling imports)
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)

    module_name = f"_agentos_loaded_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        print(f"Error: could not load module from {filepath}")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    # Prevent ``if __name__ == "__main__"`` blocks from running
    module.__name__ = module_name
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        print(f"Error loading {filepath}: {exc}")
        sys.exit(1)

    return module


# ---------------------------------------------------------------------------
# Object discovery
# ---------------------------------------------------------------------------


def discover_objects(module: Any) -> tuple[list, list, list]:
    """Return (agents, teams, workflows) found at module level."""
    from agno.agent.agent import Agent
    from agno.team.team import Team
    from agno.workflow.workflow import Workflow

    agents: list[Agent] = []
    teams: list[Team] = []
    workflows: list[Workflow] = []

    for attr_name in dir(module):
        if attr_name.startswith("_"):
            continue
        obj = getattr(module, attr_name)
        # Check most-specific first (Team/Workflow before Agent)
        if isinstance(obj, Team):
            teams.append(obj)
        elif isinstance(obj, Workflow):
            workflows.append(obj)
        elif isinstance(obj, Agent):
            agents.append(obj)

    return agents, teams, workflows


def deduplicate_agents(agents: list, teams: list) -> list:
    """Remove agents that are already members of a discovered team."""
    member_ids: set[int] = set()
    for team in teams:
        for member in team.members or []:
            member_ids.add(id(member))
    return [a for a in agents if id(a) not in member_ids]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agentos",
        description="Spin up AgentOS from any cookbook example file(s).",
        epilog=(
            "examples:\n"
            "  uv run agentos cookbook/03_teams/02_modes/broadcast/01_basic.py\n"
            "  uv run agentos cookbook/02_agents/01_quickstart/basic_agent.py -p 8080\n"
            "  uv run agentos file1.py file2.py --name 'My AgentOS'"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Python file(s) containing Agent, Team, or Workflow definitions",
    )
    parser.add_argument("--port", "-p", type=int, default=7777, help="server port (default: 7777)")
    parser.add_argument("--host", default="localhost", help="server host (default: localhost)")
    parser.add_argument("--name", "-n", default=None, help="AgentOS instance name")

    args = parser.parse_args()

    # -- Load and discover ------------------------------------------------
    all_agents: list = []
    all_teams: list = []
    all_workflows: list = []

    for filepath in args.files:
        module = load_module(filepath)
        agents, teams, workflows = discover_objects(module)
        all_agents.extend(agents)
        all_teams.extend(teams)
        all_workflows.extend(workflows)

    all_agents = deduplicate_agents(all_agents, all_teams)

    total = len(all_agents) + len(all_teams) + len(all_workflows)
    if total == 0:
        print("Error: no Agent, Team, or Workflow instances found in the provided file(s).", file=sys.stderr)
        sys.exit(1)

    # -- Summary ----------------------------------------------------------
    def log(msg: str = "") -> None:
        print(msg, file=sys.stderr, flush=True)

    log(f"\nDiscovered {total} object(s) from {len(args.files)} file(s):\n")
    for a in all_agents:
        log(f"  Agent:    {a.name or '(unnamed)'}")
    for t in all_teams:
        log(f"  Team:     {t.name or '(unnamed)'}")
        for m in t.members or []:
            log(f"            - {m.name or '(unnamed)'}")
    for w in all_workflows:
        log(f"  Workflow: {w.name or '(unnamed)'}")

    # -- Build and serve --------------------------------------------------
    from agno.os import AgentOS

    name = args.name
    if not name:
        stems = [Path(f).stem for f in args.files]
        name = "Cookbook: " + ", ".join(stems)

    agent_os = AgentOS(
        name=name,
        agents=all_agents or None,
        teams=all_teams or None,
        workflows=all_workflows or None,
    )
    app = agent_os.get_app()

    log(f"\nServing on http://{args.host}:{args.port}")
    log(f"Open https://os.agno.com to interact with your agents\n")

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
