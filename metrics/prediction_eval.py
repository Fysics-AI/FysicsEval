from __future__ import annotations

import json
import re
import string
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

score_key_default = "eval_score"
Number = Union[int, float]


# ---------- IO helpers ----------
def _read_records(path: Union[str, Path]) -> List[Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        raise ValueError("Only list-style JSON is supported")
    raise ValueError(f"Unsupported file type: {path.suffix}")


def _write_jsonl(records: Iterable[Dict[str, Any]], output_path: Union[str, Path]) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for item in records:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def _default_output_path(input_path: Union[str, Path], output_dir: Union[str, Path]) -> Path:
    src = Path(input_path)
    target_dir = Path(output_dir)
    suffix = ".jsonl"
    return target_dir / (src.stem + suffix)


# ---------- numeric parsing ----------
def _clean_numeric_text(value: Any) -> str:
    """
    Light cleanup before numeric parsing:
    - remove <think>...</think> blocks
    - keep the last non-empty paragraph (models often place the final value last)
    - strip commas and extra spaces
    """
    text = str(value or "")
    text = re.sub(r"<\s*THINK\s*>.*?<\s*/\s*THINK\s*>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    parts = [seg.strip() for seg in re.split(r"\n\s*\n", text) if seg.strip()]
    if len(parts) >= 2:
        text = parts[-1]
    return text.replace(",", " ").strip()


def _is_number_or_punct(text: str) -> bool:
    """Allow only digits and punctuation (ASCII + common CJK marks)."""
    allowed_punct = string.punctuation + "，。？！；：、“”‘’（）【】《》％%"
    pattern = rf"^[0-9eE{re.escape(allowed_punct)}\s]+$"
    return bool(re.fullmatch(pattern, text.strip()))


_NUM_PATTERN = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _extract_first_number(value: Any) -> Optional[float]:
    """
    Pull out the first numeric token from free-form text.
    Returns None when no number is present or conversion fails.
    """
    text = _clean_numeric_text(value)
    if not _is_number_or_punct(text):
        return None
    matches = _NUM_PATTERN.findall(text)
    if len(matches) != 1:
        return None
    try:
        return float(matches[0])
    except Exception:
        return None


def _wrap_score(value: Any) -> Dict[str, Any]:
    return {"score": value}


# ---------- Numeric metrics ----------
def evaluate_numeric_mra(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    *,
    prediction_key: str = "prediction",
    answer_key: str = "answer",
    score_key: str = "mra",
    eps: float = 1e-9,
) -> Dict[str, Any]:
    """
    Mean Relative Accuracy (MRA):
        rel_err = |pred - gold| / max(|gold|, eps)
        mra = mean(rel_err < (1 - theta) for theta in C)
    where C = [0.1, 0.2, ..., 0.95].
    Records without numeric pred/gold are scored 0.
    """
    records = _read_records(input_path)
    scored: List[Dict[str, Any]] = []
    scores: List[float] = []

    thresholds: List[float] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

    for rec in records:
        item = deepcopy(rec)
        pred = _extract_first_number(item.get(prediction_key))
        gold = _extract_first_number(item.get(answer_key))

        mra_score: float = 0.0
        if pred is not None and gold is not None:
            rel_err = abs(pred - gold) / max(abs(gold), eps)
            mra_score = sum(rel_err < (1 - t) for t in thresholds) / len(thresholds)
        scores.append(mra_score)

        item[score_key] = _wrap_score(mra_score)
        scored.append(item)

    output_path = _default_output_path(input_path, output_dir)
    _write_jsonl(scored, output_path)
    return {
        "task": "numeric_mra",
        "output": str(output_path),
        "total": len(records),
        "scored": len(scores),
        "mean_mra": (sum(scores) / len(scores)) if scores else None,
    }
__all__ = [
    "evaluate_numeric_mra",
    "score_key_default",
]
