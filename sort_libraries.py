import argparse
import json
import sys


def sort_libraries(input_path, output_path=None):
    """
    Reads a library JSON array, sorts entries alphabetically by name,
    reassigns sequential IDs to reflect the new sort order, and writes
    the result. All other fields are left unchanged.
    """

    # Read
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: Expected a JSON array at the root level.", file=sys.stderr)
        sys.exit(1)

    # Sort alphabetically by name (case-insensitive)
    sorted_data = sorted(data, key=lambda x: (x.get("name") or "").casefold())

    # Reassign IDs sequentially to reflect new sort order
    for index, item in enumerate(sorted_data, start=0):
        item["id"] = index

    # Write (defaults to overwriting the input file)
    destination = output_path or input_path
    with open(destination, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, indent=2, ensure_ascii=False)
        f.write("\n")  # POSIX-compliant trailing newline

    print(
        f"✓ Sorted {len(sorted_data)} entries and wrote to '{destination}'."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sort a library JSON array alphabetically by name and reassign sequential IDs."
    )
    parser.add_argument(
        "input",
        help="Path to the source JSON file."
    )
    parser.add_argument(
        "--output", "-o",
        help="Path for the sorted output file. Defaults to overwriting the input file.",
        default=None
    )

    args = parser.parse_args()
    sort_libraries(args.input, args.output)
