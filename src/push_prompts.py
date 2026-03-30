"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_FILE = os.getenv("PROMPT_V2_PATH", "prompts/bug_to_user_story_v2.yml")
USERNAME_LANGSMITH_HUB = os.getenv("USERNAME_LANGSMITH_HUB")


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    system_prompt = prompt_data.get("system_prompt", "")
    user_prompt = prompt_data.get("user_prompt", "")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt),
    ])

    client = Client()
    url = client.push_prompt(
        f"{USERNAME_LANGSMITH_HUB}/{prompt_name}",
        object=prompt_template,
        tags=prompt_data.get("tags", []),
        description=prompt_data.get("description", ""),
        is_public=True,
    )
    print(f"✓ Prompt publicado: {url}")
    return True


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors = []
    if not prompt_data.get("system_prompt"):
        errors.append("system_prompt ausente ou vazio")
    if not prompt_data.get("user_prompt"):
        errors.append("user_prompt ausente ou vazio")
    return len(errors) == 0, errors


def main():
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    data = load_yaml(PROMPT_FILE)
    if not data:
        return 1

    print_section_header("Push de Prompts para o LangSmith Hub")

    for prompt_name, prompt_data in data.items():
        print(f"Enviando prompt: {prompt_name}")

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print(f"Prompt inválido: {errors}")
            return 1

        try:
            push_prompt_to_langsmith(prompt_name, prompt_data)
        except Exception as e:
            print(f"Erro ao enviar {prompt_name}: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
