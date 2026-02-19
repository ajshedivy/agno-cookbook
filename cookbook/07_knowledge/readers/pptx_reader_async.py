import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pptx_reader import PPTXReader
from agno.vectordb.pgvector import PgVector

from cookbook_config import model

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    # Table name: ai.pptx_documents
    vector_db=PgVector(
        table_name="pptx_documents",
        db_url=db_url,
    ),
)

# Create an agent with the knowledge
agent = Agent(
    model=model,
    knowledge=knowledge,
    search_knowledge=True,
)


def main():
    # Load PPTX content from file(s) asynchronously
    # You can load multiple PPTX files by calling ainsert multiple times
    asyncio.run(
        knowledge.ainsert(
            path="path/to/your/presentation.pptx",  # Replace with actual PPTX file path
            reader=PPTXReader(),
        )
    )

    # Create and use the agent
    asyncio.run(
        agent.aprint_response(
            "Search through the presentation content and tell me what key topics, main points, or information are covered in the slides. Be specific about what you find in the knowledge base.",
            markdown=True,
        )
    )


if __name__ == "__main__":
    main()
