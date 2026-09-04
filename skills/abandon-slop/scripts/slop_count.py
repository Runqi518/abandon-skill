#!/usr/bin/env python3
"""Deterministic, dependency-free anti-slop counter and vocabulary manager."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REF = SKILL_ROOT / "references"
LEGACY_USER_DIR = Path.home() / ".claude" / "config" / "abandon-slop"
USER_DIR = Path(os.environ.get("ABANDON_SLOP_CONFIG_DIR", Path.home() / ".config" / "abandon-slop")).expanduser()
TEACH = USER_DIR / "teach-vocabulary.md"
ALLOW = USER_DIR / "teach-allow-list.md"
SEVERITY = {"low": 1, "medium": 2, "high": 3}
CATEGORIES = {"cliche", "inflation", "vagueness", "meta", "structure", "rhetoric", "jargon", "translation", "punctuation"}
PROVENANCE = {"prior", "prompt-induced", "translation"}


def norm(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def block_lines(path: Path, block: str) -> list[str]:
    if not path.exists():
        return []
    start, end = f"<!-- abandon:{block} -->", f"<!-- /abandon:{block} -->"
    active, result = False, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line == start:
            active = True
        elif line == end:
            active = False
        elif active and line and not line.startswith("#"):
            result.append(line)
    return result


def parse_rules(path: Path, block: str) -> list[dict]:
    rules = []
    for line in block_lines(path, block):
        parts = [part.strip() for part in line.split("|", 4)]
        if len(parts) != 5 or parts[1] not in CATEGORIES or parts[2] not in SEVERITY:
            raise ValueError(f"invalid {block} rule in {path}: {line}")
        prov = [p.strip() for p in parts[3].split(",")]
        if not prov or any(p not in PROVENANCE for p in prov):
            raise ValueError(f"invalid provenance in {path}: {line}")
        rules.append({"id": parts[0], "category": parts[1], "severity": parts[2],
                      "provenance": prov, "pattern": parts[4], "regex": block == "regex",
                      "source": str(path.relative_to(SKILL_ROOT)) if path.is_relative_to(SKILL_ROOT) else str(path)})
    return rules


def language(text: str) -> str:
    cjk = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))
    meaningful = len(re.findall(r"[\w\u3400-\u4dbf\u4e00-\u9fff]", text, re.UNICODE))
    ratio = cjk / meaningful if meaningful else 0.0
    return "zh" if ratio > 0.30 else ("mixed" if ratio >= 0.10 else "en")


def sources(lang: str, genre: str | None) -> list[Path]:
    paths = []
    if lang in {"zh", "mixed"}:
        paths.append(REF / "tells-zh.md")
    if lang in {"en", "mixed"}:
        paths.append(REF / "tells-en.md")
    if genre:
        if not re.fullmatch(r"[a-z0-9-]+", genre):
            raise ValueError(f"invalid genre name: {genre}")
        candidate = REF / "genres" / f"{genre}.md"
        if not candidate.exists():
            raise ValueError(f"unknown genre: {genre}")
        paths.append(candidate)
    legacy_teach = LEGACY_USER_DIR / "teach-vocabulary.md"
    if legacy_teach != TEACH:
        paths.append(legacy_teach)
    paths.append(TEACH)
    return paths


def merged_rules(paths: list[Path]) -> tuple[list[dict], list[str]]:
    merged = {}
    allows = []
    for path in paths:
        for rule in parse_rules(path, "terms") + parse_rules(path, "regex"):
            key = ("regex" if rule["regex"] else "literal", norm(rule["pattern"]))
            merged[key] = rule
        allows.extend(block_lines(path, "allow"))
    legacy_allow = LEGACY_USER_DIR / "teach-allow-list.md"
    if legacy_allow != ALLOW:
        allows.extend(block_lines(legacy_allow, "allow"))
    allows.extend(block_lines(ALLOW, "allow"))
    return list(merged.values()), list(dict.fromkeys(norm(a) for a in allows if norm(a)))


def paragraphs(text: str) -> list[tuple[int, int, str]]:
    result = []
    for number, match in enumerate(re.finditer(r"(?:^|\n\s*\n)(.*?)(?=\n\s*\n|\Z)", text, re.S), 1):
        body = match.group(1)
        start = match.start(1)
        if body.strip():
            result.append((number, start, body))
    return result


def covered_by_allow(text: str, start: int, end: int, allows: list[str]) -> bool:
    matched = norm(text[start:end])
    return any(matched and (matched == allow or matched in allow) for allow in allows)


def prompt_induces(prompt: str, category: str) -> bool:
    hints = {
        "inflation": ["有感染力", "震撼", "compelling", "powerful", "elevate"],
        "structure": ["结构完整", "面面俱到", "comprehensive", "structured", "three"],
        "jargon": ["专业", "高级", "professional", "thought leadership"],
        "rhetoric": ["生动", "文采", "engaging", "eloquent"],
    }
    p = norm(prompt)
    return any(norm(item) in p for item in hints.get(category, []))


def analyze(text: str, genre: str | None, forced_lang: str | None, prompt: str) -> dict:
    lang = forced_lang or language(text)
    rules, allows = merged_rules(sources(lang, genre))
    findings = []
    for para_no, para_start, para in paragraphs(text):
        para_rules = set()
        for rule in rules:
            flags = re.I | re.M
            pattern = rule["pattern"] if rule["regex"] else re.escape(rule["pattern"])
            for match in re.finditer(pattern, para, flags):
                start, end = para_start + match.start(), para_start + match.end()
                if covered_by_allow(text, start, end, allows):
                    continue
                provenance = list(rule["provenance"])
                if prompt and prompt_induces(prompt, rule["category"]) and "prompt-induced" not in provenance:
                    provenance.insert(0, "prompt-induced")
                finding = {
                    "rule_id": rule["id"], "category": rule["category"],
                    "severity": rule["severity"], "paragraph": para_no,
                    "line": text.count("\n", 0, start) + 1, "quote": match.group(0),
                    "start": start, "end": end, "provenance": provenance,
                    "source": rule["source"],
                }
                findings.append(finding)
                para_rules.add(rule["id"])
        if len(para_rules) >= 3:
            stripped = para.strip()
            start = para_start + (len(para) - len(para.lstrip()))
            findings.append({
                "rule_id": "paragraph-cooccurrence", "category": "structure", "severity": "high",
                "paragraph": para_no, "line": text.count("\n", 0, start) + 1,
                "quote": stripped[:120], "start": start, "end": start + min(120, len(stripped)),
                "provenance": ["prior"], "source": "references/spec.md",
            })
    unique = {(f["rule_id"], f["paragraph"], f["start"], f["end"]): f for f in findings}
    findings = sorted(unique.values(), key=lambda f: (f["start"], f["end"], f["rule_id"]))
    summary = dict(sorted(Counter(f["category"] for f in findings).items()))
    points = sum(SEVERITY[f["severity"]] for f in findings)
    readiness = "clean" if points <= 2 else ("light" if points <= 8 else "heavy")
    return {"schema_version": "1.0", "language": lang, "genre": genre,
            "summary": summary, "readiness": readiness, "findings": findings}


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def mutate(value: str, target: Path, block: str, remove: bool, metadata: tuple[str, str, str]) -> dict:
    if not value.strip() or "\n" in value or "|" in value:
        raise ValueError("teach values must be non-empty single lines without '|'")
    current = block_lines(target, block)
    key = norm(value)
    if block == "terms":
        kept = [line for line in current if len(line.split("|", 4)) == 5 and norm(line.split("|", 4)[4]) != key]
        if not remove:
            index = max([int(m.group(1)) for line in kept if (m := re.match(r"personal-(\d+)\|", line))] or [0]) + 1
            category, severity, provenance = metadata
            kept.append(f"personal-{index:04d}|{category}|{severity}|{provenance}|{value.strip()}")
    else:
        kept = [line for line in current if norm(line) != key]
        if not remove:
            kept.append(value.strip())
    title = "# Personal Anti-Slop Vocabulary" if block == "terms" else "# Personal Anti-Slop Allow List"
    content = f"{title}\n\n<!-- abandon:{block} -->\n" + "\n".join(kept) + f"\n<!-- /abandon:{block} -->\n"
    atomic_write(target, content)
    return {"action": "remove" if remove else "add", "kind": block, "value": value.strip(), "normalized": key, "path": str(target)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--file", type=Path)
    source.add_argument("--text")
    parser.add_argument("--genre", help="profile filename under references/genres, without .md")
    parser.add_argument("--lang", choices=["zh", "en", "mixed"])
    parser.add_argument("--prompt-file", type=Path)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--teach-add")
    actions.add_argument("--allow-add")
    actions.add_argument("--teach-remove")
    actions.add_argument("--allow-remove")
    parser.add_argument("--category", choices=sorted(CATEGORIES), default="vagueness")
    parser.add_argument("--severity", choices=sorted(SEVERITY), default="medium")
    parser.add_argument("--provenance", choices=sorted(PROVENANCE), default="prior")
    args = parser.parse_args()
    try:
        result = None
        if args.teach_add or args.teach_remove:
            result = mutate(args.teach_add or args.teach_remove, TEACH, "terms", bool(args.teach_remove), (args.category, args.severity, args.provenance))
            other = block_lines(ALLOW, "allow")
            if not args.teach_remove and any(norm(x) == norm(args.teach_add) for x in other):
                mutate(args.teach_add, ALLOW, "allow", True, ("", "", ""))
        elif args.allow_add or args.allow_remove:
            result = mutate(args.allow_add or args.allow_remove, ALLOW, "allow", bool(args.allow_remove), ("", "", ""))
            if not args.allow_remove:
                mutate(args.allow_add, TEACH, "terms", True, ("", "", ""))
        else:
            text = args.text if args.text is not None else (args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read())
            prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else ""
            result = analyze(text, args.genre, args.lang, prompt)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, re.error) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
