import os
from typing import Any, Dict, Callable

import ollama
from openai import OpenAI
from src.settings import get_settings

settings = get_settings()


# --- Backend call functions ---
def _call_ollama(prompt: str, model: str) -> str:
    response: Dict[str, Any] = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def _call_openai(prompt: str, model: str) -> str:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# --- Dispatcher dictionary ---
DISPATCH: Dict[str, Callable[[str, str], str]] = {
    "mistral:7b-instruct-q4_K_M": _call_ollama,
    "llama3": _call_ollama,
    "gpt-4o-mini": _call_openai,
    "gpt-4o": _call_openai,
}


def get_llm_response(prompt: str, model: str | None = None) -> str:
    model = model or os.getenv("LLM_MODEL", "mistral:7b-instruct-q4_K_M")
    if model not in DISPATCH:
        raise ValueError(f"Unsupported model: {model}")
    return DISPATCH[model](prompt, model)
