from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SectionSpec:
    name: str
    start_heading: str
    end_heading: str
    limit: int


SECTIONS = [
    SectionSpec(
        name="summary",
        start_heading="## One sentence summary (255 characters)",
        end_heading="## Dates",
        limit=255,
    ),
    SectionSpec(
        name="description",
        start_heading="# Describe your proposed activities. (7,000 characters maximum)",
        end_heading="## What is your capacity and experience to carry out the activities? (3,500 characters maximum)",
        limit=7000,
    ),
    SectionSpec(
        name="capacity",
        start_heading="## What is your capacity and experience to carry out the activities? (3,500 characters maximum)",
        end_heading="## Provide information about artistic and presenting partners and their involvement in your project. (1,700 characters maximum)",
        limit=3500,
    ),
    SectionSpec(
        name="partners",
        start_heading="## Provide information about artistic and presenting partners and their involvement in your project. (1,700 characters maximum)",
        end_heading="## What is your project timeline? Provide important milestones. (3,500 characters maximum)",
        limit=1700,
    ),
    SectionSpec(
        name="timeline",
        start_heading="## What is your project timeline? Provide important milestones. (3,500 characters maximum)",
        end_heading="## Budget",
        limit=3500,
    ),
    SectionSpec(
        name="other",
        start_heading="## Is there other information that will help us understand your application? (1,700 characters maximum)",
        end_heading="<!--",
        limit=1700,
    ),
]


def strip_leading_guidance(section_text: str) -> str:
    lines = section_text.strip().splitlines()
    if not lines:
        return ""

    filtered: list[str] = []
    skipping = False
    paren_balance = 0

    for line in lines:
        stripped = line.strip()

        if not filtered and stripped.startswith("("):
            skipping = True

        if skipping:
            paren_balance += stripped.count("(")
            paren_balance -= stripped.count(")")
            if paren_balance <= 0:
                skipping = False
                paren_balance = 0
            continue

        filtered.append(line)

    return "\n".join(filtered).strip()


def extract_section(text: str, spec: SectionSpec) -> str:
    start = text.index(spec.start_heading) + len(spec.start_heading)
    end = text.index(spec.end_heading, start)
    return text[start:end].strip()


def build_report(text: str, include_hints: bool) -> list[tuple[str, int, int, int]]:
    report = []
    for spec in SECTIONS:
        section_text = extract_section(text, spec)
        answer_text = section_text if include_hints else strip_leading_guidance(section_text)
        count = len(answer_text)
        remaining = spec.limit - count
        report.append((spec.name, count, spec.limit, remaining))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check character counts for the CCA application sections.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=Path(__file__).with_name("application.md"),
        type=Path,
        help="Path to the application markdown file.",
    )
    parser.add_argument(
        "--include-hints",
        action="store_true",
        help="Count the bracketed Council guidance at the start of sections.",
    )
    args = parser.parse_args()

    text = args.path.read_text()
    report = build_report(text, include_hints=args.include_hints)

    print(f"Character counts for: {args.path}")
    print("Mode: counting full section text" if args.include_hints else "Mode: excluding leading bracketed guidance")
    print()
    print(f"{'section':<12} {'count':>7} {'limit':>7} {'delta':>7} status")
    print("-" * 46)

    has_overages = False
    for name, count, limit, remaining in report:
        status = "OK" if remaining >= 0 else "OVER"
        has_overages = has_overages or remaining < 0
        print(f"{name:<12} {count:>7} {limit:>7} {remaining:>7} {status}")

    return 1 if has_overages else 0


if __name__ == "__main__":
    raise SystemExit(main())