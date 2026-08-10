import json
import argparse
import sys
from collections import defaultdict


def validate_libraries(input_path):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON — {e}", file=sys.stderr)
        return False

    if not isinstance(data, list):
        print("Error: Expected a JSON array at the root level.", file=sys.stderr)
        return False

    groups = defaultdict(list)
    for item in data:
        groups[item.get("libid")].append(item)

    errors = []
    for libid, items in groups.items():
        primaries = [item for item in items if item.get("is_primary") is True]
        if len(primaries) == 0:
            names = ", ".join(item.get("name", "?") for item in items)
            errors.append(f"libid {libid!r} has no entry marked is_primary: true ({names})")
        elif len(primaries) > 1:
            names = ", ".join(item.get("name", "?") for item in primaries)
            errors.append(f"libid {libid!r} has {len(primaries)} entries marked is_primary: true ({names})")

    if errors:
        print("Error: is_primary validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return False

    print(f"✓ Validated {len(data)} entries across {len(groups)} libid group(s) — exactly one is_primary per group.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate that each libid in a library JSON array has exactly one entry marked is_primary: true."
    )
    parser.add_argument("input", help="Path to the source JSON file.")

    args = parser.parse_args()
    sys.exit(0 if validate_libraries(args.input) else 1)
