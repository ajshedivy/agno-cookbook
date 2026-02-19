"""
Team Instantiation Performance Evaluation
=========================================

Demonstrates measuring team instantiation performance.
"""

from agno.agent import Agent
from agno.eval.performance import PerformanceEval
from agno.team.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Team Member
# ---------------------------------------------------------------------------
team_member = Agent(model=model)


# ---------------------------------------------------------------------------
# Create Benchmark Function
# ---------------------------------------------------------------------------
def instantiate_team():
    return Team(members=[team_member])


# ---------------------------------------------------------------------------
# Create Evaluation
# ---------------------------------------------------------------------------
instantiation_perf = PerformanceEval(name="Instantiation Performance Team", func=instantiate_team, num_iterations=1000)

# ---------------------------------------------------------------------------
# Run Evaluation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instantiation_perf.run(print_results=True, print_summary=True)
