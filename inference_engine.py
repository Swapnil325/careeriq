# ============================================================
# inference_engine.py
# Forward Chaining Inference Engine
#
# How it works:
#   1. Normalise user input into a "working memory" dict.
#   2. Iterate every rule in the knowledge base.
#   3. For each rule, count how many conditions are satisfied.
#   4. A rule FIRES when ALL required condition categories match
#      at least one item (partial match within a category is OK).
#   5. Confidence score = base_score × (matched_conditions / total_conditions)
#   6. Return fired rules sorted by confidence (highest first).
# ============================================================

from knowledge_base import RULES


def _normalise(value):
    """Lowercase + strip a string or list of strings."""
    if isinstance(value, list):
        return [v.lower().strip() for v in value]
    return value.lower().strip()


def _build_working_memory(user_input: dict) -> dict:
    """Convert raw user input into a clean working-memory dict."""
    return {
        "interests":  _normalise(user_input.get("interests", [])),
        "marks": {
            k: _normalise(v)
            for k, v in user_input.get("marks", {}).items()
        },
        "skills":     _normalise(user_input.get("skills", [])),
        "personality": _normalise(user_input.get("personality", [])),
    }


def _check_rule(rule: dict, wm: dict) -> tuple[bool, float, list[str]]:
    """
    Evaluate a single rule against working memory.

    Returns:
        fired        – True if ALL condition groups are satisfied
        confidence   – score between 0-100
        matched_keys – human-readable list of what matched (for explanation)
    """
    conditions   = rule["conditions"]
    total_groups = len(conditions)
    matched      = 0
    matched_keys = []

    # ── interests ───────────────────────────────────────────
    if "interests" in conditions:
        required = conditions["interests"]
        hits = [i for i in required if i in wm["interests"]]
        if hits:
            matched += 1
            matched_keys.append(f"interests: {', '.join(hits)}")
        else:
            return False, 0.0, []          # hard fail

    # ── marks ───────────────────────────────────────────────
    if "marks" in conditions:
        required_marks = conditions["marks"]
        mark_hits = []
        for subject, level in required_marks.items():
            if wm["marks"].get(subject) == level:
                mark_hits.append(f"{subject}={level}")
        if len(mark_hits) == len(required_marks):   # ALL marks must match
            matched += 1
            matched_keys.append(f"marks: {', '.join(mark_hits)}")
        else:
            return False, 0.0, []          # hard fail

    # ── skills ──────────────────────────────────────────────
    if "skills" in conditions:
        required = conditions["skills"]
        hits = [s for s in required if s in wm["skills"]]
        if hits:
            matched += 1
            matched_keys.append(f"skills: {', '.join(hits)}")
        else:
            return False, 0.0, []          # hard fail

    # ── personality ─────────────────────────────────────────
    if "personality" in conditions:
        required = conditions["personality"]
        hits = [p for p in required if p in wm["personality"]]
        if hits:
            matched += 1
            matched_keys.append(f"personality: {', '.join(hits)}")
        else:
            return False, 0.0, []          # hard fail

    # ── confidence = base_score × (matched / total) ─────────
    confidence = round(rule["base_score"] * (matched / total_groups), 1)
    return True, confidence, matched_keys


def run_inference(user_input: dict) -> list[dict]:
    """
    Main entry point.  Returns a sorted list of career suggestions.
    Each item: { career, confidence, explanation, rule_id, matched_on }
    """
    wm      = _build_working_memory(user_input)
    results = []

    for rule in RULES:
        fired, confidence, matched_keys = _check_rule(rule, wm)
        if fired:
            results.append({
                "career":      rule["career"],
                "confidence":  confidence,
                "explanation": rule["explanation"],
                "rule_id":     rule["id"],
                "matched_on":  matched_keys,
            })

    # Sort by confidence descending
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results
