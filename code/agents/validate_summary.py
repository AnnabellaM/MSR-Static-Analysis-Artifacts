#!/usr/bin/env python3
"""
Validate the summarizer's annotation for one item and write it, with the raw
item's identifying fields, to data/summarized/<tool>_<n>.json. The full raw
item (comments, commits, patches) stays in data/issues/; join on tool + number.
The annotation goes under a "summary" key since the raw item has its own "type".

Checks:
  - schema: type, problem, cause, references
  - every evidence claim appears verbatim (whitespace-normalized) in the cited field

Exits non-zero and prints every error if validation fails; nothing is written.

Usage: python agents/validate_summary.py data/issues/soot_1206.json annotation.json
"""

import json
import os
import re
import sys

OUTPUT_DIR = "data/summarized"
ID_FIELDS = ("tool", "number", "type", "html_url", "state", "created_at", "closed_at",
             "significant_pr")  # significant_pr is null for issues
TYPES = {"BUG", "ENHANCEMENT", "QUESTION", "MAINTENANCE", "OTHER"}
RELATIONS = {"FIXES", "FIXED_BY", "DUPLICATE_OF", "DEPENDS_ON", "RELATED"}
TARGET = re.compile(r'^([a-z]+-\d+|[\w.-]+/[\w.-]+#\d+)$')


def fields(item: dict) -> list[tuple[str, str]]:
    """Return (label, text) pairs using the labels evidence must cite."""
    out = [("TITLE", item.get("title") or ""), ("BODY", item.get("body") or "")]
    for i, c in enumerate(item.get("comments") or [], start=1):
        out.append((f"COMMENT_{i:02d}", c.get("body") or ""))
    return out


def norm(text: str) -> str:
    return re.sub(r'\s+', ' ', text or "").strip()


def check_evidence(evidence, sources: dict, where: str, errors: list) -> None:
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{where}.evidence must be a non-empty list")
        return
    for i, ev in enumerate(evidence):
        loc = f"{where}.evidence[{i}]"
        if not isinstance(ev, dict) or set(ev) != {"field", "claim"}:
            errors.append(f"{loc} must be exactly {{field, claim}}")
            continue
        if ev["field"] not in sources:
            errors.append(f"{loc}.field {ev['field']!r} does not exist in this item")
        elif not norm(ev["claim"]) or norm(ev["claim"]) not in norm(sources[ev["field"]]):
            errors.append(f"{loc}.claim is not a verbatim quote from {ev['field']}: {ev['claim'][:80]!r}")


def validate(ann: dict, sources: dict) -> list[str]:
    errors = []
    expected = {"type", "problem", "cause", "references"}
    if set(ann) != expected:
        errors.append(f"top-level keys must be {sorted(expected)}, got {sorted(ann)}")
    if ann.get("type") not in TYPES:
        errors.append(f"type must be one of {sorted(TYPES)}")

    problem = ann.get("problem")
    if not isinstance(problem, dict) or not norm(problem.get("description")):
        errors.append("problem.description is required")
    else:
        check_evidence(problem.get("evidence"), sources, "problem", errors)

    cause = ann.get("cause")
    if cause is not None:
        if not isinstance(cause, dict) or set(cause) != {"description", "evidence"}:
            errors.append("cause must be null or exactly {description, evidence}")
        else:
            if not norm(cause["description"]):
                errors.append("cause.description is required")
            check_evidence(cause["evidence"], sources, "cause", errors)

    refs = ann.get("references")
    if not isinstance(refs, list):
        errors.append("references must be a list (empty if none)")
        refs = []
    for i, ref in enumerate(refs):
        loc = f"references[{i}]"
        if not isinstance(ref, dict) or set(ref) != {"target", "relation", "evidence"}:
            errors.append(f"{loc} must be exactly {{target, relation, evidence}}")
            continue
        if not TARGET.match(str(ref["target"])):
            errors.append(f"{loc}.target {ref['target']!r} must look like 'soot-123' or 'org/repo#123'")
        if ref["relation"] not in RELATIONS:
            errors.append(f"{loc}.relation must be one of {sorted(RELATIONS)}")
        check_evidence(ref["evidence"], sources, loc, errors)
    return errors


def main(raw_path: str, ann_path: str) -> None:
    with open(raw_path, encoding="utf-8") as f:
        item = json.load(f)
    with open(ann_path, encoding="utf-8") as f:
        ann = json.load(f)

    errors = validate(ann, dict(fields(item)))
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    out = {k: item.get(k) for k in ID_FIELDS}
    out["summary"] = ann
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, os.path.basename(raw_path))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)
    print(f"OK: wrote {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
