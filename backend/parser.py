import os

SKIP_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__MACOSX",
    "node_modules",
    "target",
    "build",
    "dist",
    "__pycache__"
}


def read_java_files(folder):

    java_files = {}

    print("\n========== PARSER ==========")

    for root, dirs, files in os.walk(folder):

        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:

            if file.startswith("._"):
                continue

            if not file.endswith(".java"):
                continue

            path = os.path.join(root, file)

            print("Reading:", path)

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    java_files[path] = f.read()

            except Exception as e:

                print("Skipped:", path)
                print(e)

    return java_files