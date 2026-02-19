import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.csv_reader import CSVReader
from agno.vectordb.pgvector import PgVector

from cookbook_config import model

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="csv_documents",
        db_url=db_url,
    ),
    max_results=5,  # Number of results to return on search
)

# Initialize the Agent with the knowledge
agent = Agent(
    model=model,
    knowledge=knowledge,
    search_knowledge=True,
)


if __name__ == "__main__":
    # Comment out after first run
    asyncio.run(
        knowledge.ainsert(
            url="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
            reader=CSVReader(encoding="gb2312"),
        )
    )

    # Create and use the agent
    asyncio.run(agent.aprint_response("What is the csv file about", markdown=True))
