"""
Tasks with Dependencies Example

Demonstrates task mode with dependency chains. The team leader creates tasks
where later tasks depend on earlier ones, ensuring correct execution order.

"""

from agno.agent import Agent
from agno.team.mode import TeamMode
from agno.team.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------

data_collector = Agent(
    name="Data Collector",
    role="Gathers raw data and facts on a topic",
    model=model,
    instructions=[
        "You collect raw data and facts on the given topic.",
        "Be thorough -- gather statistics, key facts, and relevant details.",
        "Present findings as structured data points.",
    ],
)

analyst = Agent(
    name="Analyst",
    role="Analyzes data and extracts insights",
    model=model,
    instructions=[
        "You analyze data provided to you and extract insights.",
        "Identify trends, patterns, and notable findings.",
        "Support conclusions with the data you were given.",
    ],
)

report_writer = Agent(
    name="Report Writer",
    role="Writes polished reports from analysis results",
    model=model,
    instructions=[
        "You write clear, professional reports.",
        "Structure the report with an executive summary, key findings, and conclusion.",
        "Make the report accessible to a non-technical audience.",
    ],
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------

team = Team(
    name="Research Pipeline Team",
    mode=TeamMode.tasks,
    model=model,
    members=[data_collector, analyst, report_writer],
    instructions=[
        "You lead a research pipeline team.",
        "Create tasks with dependencies to enforce execution order:",
        "1. Data Collection (no dependencies) -- assign to Data Collector",
        "2. Analysis (depends on Data Collection) -- assign to Analyst",
        "3. Report Writing (depends on Analysis) -- assign to Report Writer",
        "Use the dependency field when creating tasks to ensure correct ordering.",
        "Provide the final report as your response.",
    ],
    show_members_responses=True,
    markdown=True,
    max_iterations=10,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    team.print_response(
        "Research the global renewable energy market: gather key data, "
        "analyze trends, and produce a brief executive report."
    )
