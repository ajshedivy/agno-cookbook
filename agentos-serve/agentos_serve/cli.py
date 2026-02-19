"""Spin up AgentOS from any Python file(s) or directory containing Agno agents.

Dynamically imports the target file(s), discovers Agent / Team / Workflow
instances at module level, and serves them via AgentOS.

Usage:
    agentos-serve path/to/agent.py
    agentos-serve path/to/agents/
    agentos-serve dir1/ dir2/ file.py
    agentos-serve file.py -p 8080
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Package -> install hint mapping
# ---------------------------------------------------------------------------

# Packages covered by `pip install agentos-serve[common-tools]`
_COMMON_TOOLS_PACKAGES: set[str] = {
    "ddgs", "duckduckgo_search",  # agno[ddg]
    "yfinance",                    # agno[yfinance]
    "exa_py",                      # agno[exa]
    "newspaper4k", "lxml_html_clean",  # agno[newspaper]
    "sqlalchemy",                  # agno[sql]
    "duckdb",                      # agno[duckdb]
}

# Package name (from error message) -> agno extra name
_PACKAGE_TO_EXTRA: dict[str, str] = {
    # Model providers
    "openai": "openai",
    "anthropic": "anthropic",
    "google.genai": "google",
    "google_genai": "google",
    "groq": "groq",
    "mistralai": "mistral",
    "cohere": "cohere",
    "ollama": "ollama",
    # Individual tool extras
    "mcp": "mcp",
    "fal_client": "fal",
    "firecrawl": "firecrawl",
    "PyGithub": "github",
    "crawl4ai": "crawl4ai",
}


def _install_hint(exc: Exception) -> str | None:
    """Given an import error, return a helpful install suggestion or ``None``."""
    msg = str(exc)

    # Check if any common-tools package is mentioned
    for pkg in _COMMON_TOOLS_PACKAGES:
        if pkg in msg:
            return "pip install agentos-serve[common-tools]"

    # Check for known individual extras
    for pkg, extra in _PACKAGE_TO_EXTRA.items():
        if pkg in msg:
            return f"pip install agno[{extra}]"

    # Fallback: try to extract the package name from "No module named 'xxx'"
    if "No module named" in msg:
        start = msg.find("'")
        end = msg.find("'", start + 1) if start != -1 else -1
        if start != -1 and end != -1:
            mod = msg[start + 1 : end].split(".")[0]
            return f"pip install {mod}"

    return None


# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------


def resolve_paths(paths: list[str]) -> list[Path]:
    """Expand directories to their contained ``.py`` files (sorted), pass files through."""
    result: list[Path] = []
    for p in paths:
        target = Path(p).resolve()
        if target.is_dir():
            py_files = sorted(target.glob("*.py"))
            if not py_files:
                print(f"Warning: no .py files in directory: {p}", file=sys.stderr)
            result.extend(py_files)
        elif target.is_file():
            result.append(target)
        else:
            print(f"Error: path not found: {p}", file=sys.stderr)
            sys.exit(1)
    return result


def load_module(filepath: Path) -> Any | None:
    """Dynamically import a Python file, skipping its ``__main__`` block.

    Returns ``None`` (with a warning) if the file fails to import, so that
    directories with files that have missing dependencies don't abort the
    entire run.
    """
    if filepath.suffix != ".py":
        return None

    # Ensure the file's own directory is importable (sibling imports)
    parent = str(filepath.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)

    # Ensure CWD is importable (for project-local config modules)
    cwd = str(Path.cwd())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    module_name = f"_agentos_loaded_{filepath.stem}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        print(f"Warning: could not create module spec for {filepath}", file=sys.stderr)
        return None

    module = importlib.util.module_from_spec(spec)
    # Prevent ``if __name__ == "__main__"`` blocks from running
    module.__name__ = module_name
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        hint = _install_hint(exc)
        msg = f"Warning: skipping {filepath.name} ({exc})"
        if hint:
            msg += f"\n    -> {hint}"
        print(msg, file=sys.stderr)
        return None

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
        prog="agentos-serve",
        description="Spin up AgentOS from any Python file(s) containing Agno agents, teams, or workflows.",
        epilog=(
            "examples:\n"
            "  agentos-serve agents/my_agent.py\n"
            "  agentos-serve agents/\n"
            "  agentos-serve agents/ teams/\n"
            "  agentos-serve file1.py file2.py --name 'My AgentOS' -p 8080"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Python file(s) or directories containing Agent, Team, or Workflow definitions",
    )
    parser.add_argument("--port", "-p", type=int, default=7777, help="server port (default: 7777)")
    parser.add_argument("--host", default="localhost", help="server host (default: localhost)")
    parser.add_argument("--name", "-n", default=None, help="AgentOS instance name")

    args = parser.parse_args()

    # -- Resolve paths ----------------------------------------------------
    py_files = resolve_paths(args.paths)
    if not py_files:
        print("Error: no Python files resolved from the provided path(s).", file=sys.stderr)
        sys.exit(1)

    # -- Load and discover ------------------------------------------------
    all_agents: list = []
    all_teams: list = []
    all_workflows: list = []
    loaded_count = 0

    for filepath in py_files:
        module = load_module(filepath)
        if module is None:
            continue
        loaded_count += 1
        agents, teams, workflows = discover_objects(module)
        all_agents.extend(agents)
        all_teams.extend(teams)
        all_workflows.extend(workflows)

    all_agents = deduplicate_agents(all_agents, all_teams)

    total = len(all_agents) + len(all_teams) + len(all_workflows)
    if total == 0:
        print("Error: no Agent, Team, or Workflow instances found in the provided path(s).", file=sys.stderr)
        sys.exit(1)

    # -- Summary ----------------------------------------------------------
    def log(msg: str = "") -> None:
        print(msg, file=sys.stderr, flush=True)

    log(f"\nLoaded {loaded_count} file(s), discovered {total} object(s):\n")
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
        labels: list[str] = []
        for p in args.paths:
            target = Path(p)
            labels.append(target.name if target.is_dir() else target.stem)
        name = "AgentOS: " + ", ".join(labels)

    agent_os = AgentOS(
        name=name,
        agents=all_agents or None,
        teams=all_teams or None,
        workflows=all_workflows or None,
    )
    app = agent_os.get_app()

    log(f"\nServing on http://{args.host}:{args.port}")
    log("Open https://os.agno.com to interact with your agents\n")

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
