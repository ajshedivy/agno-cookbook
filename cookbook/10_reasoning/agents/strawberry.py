"""
Strawberry Letter Counting
==========================

Demonstrates regular, built-in, and DeepSeek-backed reasoning for counting tasks.
"""

import asyncio

from agno.agent import Agent
from rich.console import Console

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agents
# ---------------------------------------------------------------------------
console = Console()

task = "How many 'r' are in the word 'strawberry'?"

regular_agent = Agent(model=model, markdown=True)

cot_agent = Agent(
    model=model,
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=model,
    reasoning_model=model,
    markdown=True,
)


async def run_agents() -> None:
    console.rule("[bold blue]Counting 'r' In 'strawberry'[/bold blue]")

    console.rule("[bold green]Regular Agent[/bold green]")
    await regular_agent.aprint_response(task, stream=True)

    console.rule("[bold yellow]Built-in Reasoning Agent[/bold yellow]")
    await cot_agent.aprint_response(task, stream=True, show_full_reasoning=True)

    console.rule("[bold cyan]DeepSeek Reasoning Agent[/bold cyan]")
    await deepseek_agent.aprint_response(task, stream=True)


# ---------------------------------------------------------------------------
# Run Agents
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(run_agents())
