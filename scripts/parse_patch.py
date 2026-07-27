import re
import json
import sys

patch_file = sys.argv[1]

changed = {}

current_file = None

with open(patch_file, encoding="utf-8") as f:

    for line in f:

        if line.startswith("+++ b/"):
            current_file = line[6:].strip()

            if current_file not in changed:
                changed[current_file] = []

        elif line.startswith("@@"):

            m = re.search(r"\+(\d+)(?:,(\d+))?", line)

            if not m or current_file is None:
                continue

            start = int(m.group(1))
            count = int(m.group(2) or 1)

            changed[current_file].extend(
                range(start, start + count)
            )

print(json.dumps(changed, indent=4))