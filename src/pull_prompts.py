"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = os.getenv("LANGSMITH_PULL_PROMPT", "leonanluppi/bug_to_user_story_v1")
OUTPUT_FILE = os.getenv("PROMPT_OUTPUT_PATH", "prompts/bug_to_user_story_v1.yml")


def pull_prompts_from_langsmith():
    print_section_header("Pull de Prompts do LangSmith Hub")

    print(f"Puxando prompt: {PROMPT_NAME}")
    prompt = hub.pull(PROMPT_NAME)
    print("✓ Prompt carregado com sucesso")

    messages = prompt.messages
    system_content = messages[0].prompt.template if len(messages) > 0 else ""
    user_content = messages[1].prompt.template if len(messages) > 1 else ""

    data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_content,
            "user_prompt": user_content,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    if save_yaml(data, OUTPUT_FILE):
        print(f"✓ Prompt salvo em {OUTPUT_FILE}")
    else:
        print(f"Falha ao salvar {OUTPUT_FILE}")
        return 1

    return 0


def main():
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    try:
        return pull_prompts_from_langsmith()
    except Exception as e:
        print(f"Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
