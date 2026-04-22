import json
from pathlib import Path


def main() -> int:
    source_path = Path(__file__).resolve().parent.parent / "data" / "quantum_sources.jsonl"

    if not source_path.exists():
        print(f"Source file not found: {source_path}")
        return 1

    records = []
    concepts: set[str] = set()

    for line_number, raw_line in enumerate(source_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON on line {line_number}: {exc}")
            return 1

        records.append(record)
        for concept in record.get("concepts", []):
            concepts.add(str(concept))

    print(f"Total sources: {len(records)}")
    print("Concepts:")
    for concept in sorted(concepts):
        print(f"- {concept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
