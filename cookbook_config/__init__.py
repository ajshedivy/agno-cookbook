from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

# Load ALL vars from .env into the process environment
# so agno can pick up API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
load_dotenv(_ENV_FILE)


class CookbookSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AGNO_", extra="ignore")

    model: str = "openai:gpt-4o"


settings = CookbookSettings(_env_file=_ENV_FILE)

# Model string — pass directly to Agent(model=model)
model: str = settings.model
