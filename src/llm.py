import os
from typing import Any, Dict, Callable
import ollama
from openai import OpenAI
from .settings import get_settings
import pandas as pd
# from .client import get_llm_response
from .prompts import DATASET_SUMMARY_PROMPT,ANSWER_GENERATOR_PROMPT,ANSWER_EXPLANATION_PROMPT

settings = get_settings()

# --- Backend call functions ---
def _call_ollama(prompt: str, model: str):
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,  # 👈 enable streaming
    )
    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            yield chunk["message"]["content"]

def _call_openai(prompt: str, model: str):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content


# --- Dispatcher dictionary ---
DISPATCH: Dict[str, Callable[[str, str], str]] = {
    "mistral:7b-instruct-q4_K_M": _call_ollama,
    "llama3": _call_ollama,
    "gpt-4o-mini": _call_openai,
    "gpt-4o": _call_openai,
}

def get_llm_response(prompt: str, model: str | None = None, stream: bool = False):
    model = model or os.getenv("LLM_MODEL", "mistral:7b-instruct-q4_K_M")
    if model not in DISPATCH:
        raise ValueError(f"Unsupported model: {model}")
    else:
        print(f"Using model: {model}")
    generator = DISPATCH[model](prompt, model)  # always yields

    if stream:
        # hand generator back to caller
        return generator
    else:
        # consume generator fully, return one string
        full_text = ""
        for token in generator:
            full_text += token
        return full_text


def prepare_for_llm(df: pd.DataFrame, max_sample: int = 5) -> dict:
    """
    Summarize a dataframe into schema, summary stats, correlations, and a small sample.

    Args:
        df: Input DataFrame
        max_sample: Number of rows to include as examples
    
    Returns:
        dict with schema, summary, correlations, and sample
    """
    numeric_cols = df.select_dtypes(include="number").columns
    # print(f"Numeric columns: {list(numeric_cols)}")

    # Schema
    schema = list(df.columns)
    # print(f"Schema: {schema}")

    # Summary stats (mean, std, min, max for numeric cols only)
    summary = {}
    for col in numeric_cols:
        summary[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }

    # Correlation matrix (numeric only)
    corr_matrix = df[numeric_cols].corr().round(2).to_dict()

    # Example rows
    sample = df.head(max_sample).to_dict(orient="records")

    # print(f"Prepared summary with {len(schema)} columns, {len(summary)} summaries, and {len(sample)} sample rows.")

    return {
        "schema": schema,
        "summary": summary,
        "correlations": corr_matrix,
        "sample": sample,
    }


def explain_dataset(df: pd.DataFrame, question: str, model: str = "mistral:7b-instruct-q4_K_M",stream: bool = False):
    """
    Pre-compute stats & correlations, then let LLM explain in plain English.
    """
    prepared = prepare_for_llm(df)

    prompt = DATASET_SUMMARY_PROMPT.format(
        question=question,
        schema=prepared["schema"],
        summary=prepared["summary"],
        correlations=prepared["correlations"],
        sample=prepared["sample"]
    )

    if stream:
        # yield chunks
        for token in get_llm_response(prompt, stream=True):
            yield token
    else:
        # return final string
        return get_llm_response(prompt, stream=False)
    
def generate_code(question: str, cols: list, table_name: str) -> str:

    prompt = ANSWER_GENERATOR_PROMPT.format(
        question=question,
        cols=cols,
        table_name=table_name
    )

    resp = get_llm_response(prompt, model=settings.LLM_MODEL, stream=False)
    # Remove triple backticks and "python" language marker if present
    if resp.startswith("```"):
        resp = resp.strip().strip("`")   # remove all backticks
        # Sometimes it comes as ```python\n...\n```
        if resp.lower().startswith("sql"):
            resp = resp[len("sql"):].lstrip("\n")
    return resp.strip()


def execute_code(df: pd.DataFrame, code: str):
    allowed_locals = {"df": df}
    exec(code, {}, allowed_locals)  # sandbox-ish
    return allowed_locals.get("result")

def explain_answer(question: str, result: any):
    prompt = ANSWER_EXPLANATION_PROMPT.format(
        question=question,
        result=result
    )

    return get_llm_response(prompt, stream=False)

    # resp = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role":"user","content":prompt}]
    # )
    # return resp.choices[0].message.content
