"""
Open-ended QA LLM-judge prompt and minimal helper for FysicsEval reasoning.

This file keeps the rubric in one place and exposes:
  - `build_messages(question, reference_answer, model_response)` -> chat messages
  - `llm_judge_openqa(...)`                         -> async one-shot judge call

It returns the six rubric scores as plain integers (1/3/5) so it stays compatible
with the existing evaluators that expect numeric fields per dimension.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

__all__ = [
    "SYSTEM_PROMPT",
    "FYSICS_REASONING_RUBRIC",
    "build_messages",
    "JudgeConfig",
    "llm_judge_openqa",
]


# --------- Prompt content ---------
SYSTEM_PROMPT = (
    "You are an expert physicist evaluator. Follow the rubric exactly and "
    "respond with a single JSON object only."
)

FYSICS_REASONING_RUBRIC = """# Role Definition
You are an expert Physicist and Senior Lead Evaluator. Your task is to evaluate a [Model Response] to a [Physics Question] against a [Reference Answer] based on physics laws.

# Evaluation Objective
Assess the response on 6 dimensions (Score 1, 3, or 5) and provide a JSON output with justifications.

# Evaluation Dimensions & Scoring Criteria

## 1. Semantic Consistency
**Focus:** Internal coherence, logic flow, and responsiveness to the prompt.
- **[5] Perfect:** Coherent, directly answers prompt, no contradictions.
- **[3] Acceptable:** Answers prompt but has minor phrasing ambiguities or slight repetitions.
- **[1] Poor:** Incoherent, self-contradictory (e.g., A>B then B>A), or off-topic.

## 2. Physical Parameter Precision
**Focus:** Accuracy of values, constants ($g, c, h$), units, and orders of magnitude.
- **[5] Precise:** Correct values, units, and significant figures.
- **[3] Minor Errors:** Mostly correct, but minor unit slips or slight constant inaccuracies that don't ruin the conclusion.
- **[1] Failure:** Wrong orders of magnitude, fundamental unit errors (e.g., Force in Joules), or wrong constants.

## 3. Physical Causal Validity
**Focus:** Soundness of cause-and-effect relationships (e.g., Force $\to$ Acceleration).
- **[5] Flawless:** Correct causal direction; clearly distinguishes dependent/independent variables.
- **[3] Simplified:** Correct link, but explanation lacks depth or presents correlation as causation.
- **[1] Invalid:** Reversed causality (effect precedes cause) or invents non-physical relationships.

## 4. Physical Mechanism Identification
**Focus:** Selection of correct physical laws/models (e.g., Conservation Laws, Maxwell's Eq).
- **[5] Exact:** Identifies the specific, correct mechanism/law; rejects irrelevant ones.
- **[3] Generic:** Identifies the correct general field (e.g., "thermodynamics") but cites a generic law instead of the specific one needed.
- **[1] Incorrect:** Applies the wrong law/principle entirely.

## 5. Reasoning Chain Completeness
**Focus:** Logical derivation steps and granularity.
- **[5] Complete:** Granular, step-by-step derivation with all assumptions justified.
- **[3] Implicit:** Logical conclusion, but skips intermediate steps or relies on implicit assumptions.
- **[1] Fragmented:** Massive logical leaps, missing steps, or hallucinated derivation.

## 6. Quantitative-Qualitative Alignment
**Focus:** Consistency between mathematical results and verbal explanations.
- **[5] Aligned:** Verbal explanation perfectly matches mathematical outcome (e.g., Math: $v \downarrow$, Text: "Slows down").
- **[3] Loose:** General alignment, but tone/nuance slightly disconnects from the math.
- **[1] Conflicting:** Direct contradiction (e.g., Math shows increase, Text says decrease).

# Output Format
Output ONLY the raw JSON object below:
{
  "semantic_consistency": <int>,
  "physical_parameter_precision": <int>,
  "physical_causal_validity": <int>,
  "physical_mechanism_identification": <int>,
  "reasoning_chain_completeness": <int>,
  "quantitative_qualitative_alignment": <int>,
  
}"""

def build_messages(question: Any, reference_answer: Any, model_response: Any) -> List[Dict[str, str]]:
    """
    Build chat messages for the judge model.
    """
    user_text = (
        f"{FYSICS_REASONING_RUBRIC}\n\n"
        f"# Input Data\n"
        f"Question: {question or ''}\n"
        f"Reference Answer: {reference_answer or ''}\n"
        f"Model Response: {model_response or ''}\n\n"
        "Output the evaluation following the required format."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]


@dataclass
class JudgeConfig:
    model: str = "gpt-5"
    base_url: Optional[str] = None
    api_key: Optional[str] = None  # falls back to OPENAI_API_KEY if None
    temperature: float = 0.0
    timeout: int = 120


async def llm_judge_openqa(
    question: Any,
    reference_answer: Any,
    model_response: Any,
    *,
    client: Optional[AsyncOpenAI] = None,
    config: Optional[JudgeConfig] = None,
) -> Dict[str, Any]:
    """
    Call the LLM judge once and return the parsed JSON dict.
    """
    cfg = config or JudgeConfig()
    api_key = cfg.api_key or os.getenv("OPENAI_API_KEY")
    if client is None:
        client = AsyncOpenAI(api_key=api_key, base_url=cfg.base_url)

    resp = await client.chat.completions.create(
        model=cfg.model,
        messages=build_messages(question, reference_answer, model_response),
        temperature=cfg.temperature,
        timeout=cfg.timeout,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content or "{}"
    try:
        return json.loads(content)
    except Exception:
        # Keep raw text to aid debugging while staying JSON-compatible for callers.
        return {"judge_raw": content, "judge_parse_error": True}

