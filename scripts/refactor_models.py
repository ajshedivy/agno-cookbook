#!/usr/bin/env python3
"""Refactor cookbook examples to use cookbook_config for model selection.

Changes per file:
1. Removes `from agno.models.<provider> import <ModelClass>` lines
2. Adds `from cookbook_config import model` at the same position
3. Replaces `<ModelClass>(id="...")` with `model` in model= assignments

Skips:
- cookbook/90_models/** (provider-specific demos)
- cookbook/10_reasoning/models/** (same reason)
- cookbook/scripts/** (utility scripts)
- Imports of types (Message, Model, ModelResponse, etc.)
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COOKBOOK_DIR = REPO_ROOT / "cookbook"

# Directories to skip entirely
SKIP_DIRS = {
    COOKBOOK_DIR / "90_models",
    COOKBOOK_DIR / "10_reasoning" / "models",
    COOKBOOK_DIR / "scripts",
}

# Model classes we know how to replace
MODEL_CLASSES = {
    "OpenAIChat", "OpenAIResponses", "Gemini", "Claude", "Groq", "DeepSeek",
    "Ollama", "MistralChat", "Cohere", "Together", "Fireworks", "xAI",
    "HuggingFace", "Nvidia", "Cerebras", "CerebrasOpenAI", "Sambanova",
    "Perplexity", "OpenRouter", "OpenRouterResponses", "DeepInfra", "LiteLLM",
    "AwsBedrock", "AzureOpenAI", "AzureAIFoundry", "WatsonX", "AIMLAPI",
    "DashScope", "V0", "Llama",
}

# Modules that contain model classes (provider modules)
MODEL_PROVIDER_MODULES = {
    "agno.models.openai", "agno.models.openai.chat", "agno.models.openai.responses",
    "agno.models.google", "agno.models.google.gemini",
    "agno.models.anthropic", "agno.models.anthropic.claude",
    "agno.models.groq", "agno.models.groq.groq",
    "agno.models.deepseek", "agno.models.deepseek.deepseek",
    "agno.models.ollama", "agno.models.ollama.chat",
    "agno.models.mistral", "agno.models.mistral.mistral",
    "agno.models.cohere", "agno.models.cohere.chat",
    "agno.models.together", "agno.models.together.together",
    "agno.models.fireworks", "agno.models.fireworks.fireworks",
    "agno.models.xai", "agno.models.xai.xai",
    "agno.models.huggingface", "agno.models.huggingface.huggingface",
    "agno.models.nvidia", "agno.models.nvidia.nvidia",
    "agno.models.cerebras", "agno.models.cerebras.cerebras",
    "agno.models.sambanova", "agno.models.sambanova.sambanova",
    "agno.models.perplexity", "agno.models.perplexity.perplexity",
    "agno.models.openrouter", "agno.models.openrouter.openrouter",
    "agno.models.deepinfra", "agno.models.deepinfra.deepinfra",
    "agno.models.litellm", "agno.models.litellm.litellm",
    "agno.models.aws", "agno.models.aws.bedrock",
    "agno.models.azure", "agno.models.azure.openai_chat", "agno.models.azure.ai_foundry",
    "agno.models.ibm", "agno.models.ibm.watsonx",
    "agno.models.aimlapi", "agno.models.aimlapi.aimlapi",
    "agno.models.dashscope", "agno.models.dashscope.dashscope",
    "agno.models.vercel", "agno.models.vercel.v0",
    "agno.models.vertexai", "agno.models.vertexai.gemini", "agno.models.vertexai.claude",
    "agno.models.meta",
}

# Pattern to match model import lines
MODEL_IMPORT_RE = re.compile(
    r"^from\s+(agno\.models\.\S+)\s+import\s+(.+)$"
)

# Pattern to match model instantiation in model= assignments
# Handles: model=ModelClass(id="..."), model=ModelClass(id="...", param=val), etc.
MODEL_INSTANTIATION_RE = re.compile(
    r"(model\s*=\s*)" + r"(" + "|".join(re.escape(c) for c in MODEL_CLASSES) + r")" + r"\([^)]*\)"
)


def should_skip(filepath: Path) -> bool:
    for skip_dir in SKIP_DIRS:
        try:
            filepath.relative_to(skip_dir)
            return True
        except ValueError:
            pass
    return False


def process_file(filepath: Path) -> dict:
    stats = {"model_imports_removed": 0, "model_replaced": 0, "skipped_reason": None}

    content = filepath.read_text()
    lines = content.split("\n")

    # First pass: check if file has any model provider imports
    has_model_import = False
    for line in lines:
        stripped = line.strip()
        m = MODEL_IMPORT_RE.match(stripped)
        if m:
            module = m.group(1)
            imported = m.group(2).strip().split("#")[0].strip().split(" as ")[0].strip()
            if module in MODEL_PROVIDER_MODULES and imported in MODEL_CLASSES:
                has_model_import = True
                break

    if not has_model_import:
        stats["skipped_reason"] = "no_model_imports"
        return stats

    # Second pass: remove model imports, track position
    new_lines = []
    first_removed_idx = None

    for line in lines:
        stripped = line.strip()

        m = MODEL_IMPORT_RE.match(stripped)
        if m:
            module = m.group(1)
            imported = m.group(2).strip().split("#")[0].strip().split(" as ")[0].strip()
            if module in MODEL_PROVIDER_MODULES and imported in MODEL_CLASSES:
                stats["model_imports_removed"] += 1
                if first_removed_idx is None:
                    first_removed_idx = len(new_lines)
                continue

        new_lines.append(line)

    # Replace model instantiations
    content_new = "\n".join(new_lines)

    def replace_model(match):
        stats["model_replaced"] += 1
        return match.group(1) + "model"

    content_new = MODEL_INSTANTIATION_RE.sub(replace_model, content_new)

    # Insert cookbook_config import at the position of the first removed import
    import_line = "from cookbook_config import model"
    if import_line not in content_new:
        result_lines = content_new.split("\n")
        insert_idx = first_removed_idx if first_removed_idx is not None else 0
        result_lines.insert(insert_idx, import_line)
        content_new = "\n".join(result_lines)

    if content_new != content:
        filepath.write_text(content_new)

    return stats


def main():
    py_files = sorted(COOKBOOK_DIR.rglob("*.py"))

    total_files = 0
    total_modified = 0
    total_skipped = 0
    total_stats = {"model_imports_removed": 0, "model_replaced": 0}

    for filepath in py_files:
        if should_skip(filepath):
            total_skipped += 1
            continue

        total_files += 1
        stats = process_file(filepath)

        if stats["skipped_reason"]:
            continue

        total_modified += 1
        for key in total_stats:
            total_stats[key] += stats[key]

        if "--verbose" in sys.argv:
            print(f"  Modified: {filepath.relative_to(REPO_ROOT)}")

    print(f"\nRefactoring complete!")
    print(f"  Files scanned: {total_files}")
    print(f"  Files modified: {total_modified}")
    print(f"  Files skipped (excluded dirs): {total_skipped}")
    print(f"  Model imports removed: {total_stats['model_imports_removed']}")
    print(f"  Model instantiations replaced: {total_stats['model_replaced']}")


if __name__ == "__main__":
    main()
