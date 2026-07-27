from parser import read_java_files
from java_parser import parse_java_file
from graph.graph_service import store_java


def build_graph(project_path):
    """
    Scan the entire Java project and store
    classes and methods in Neo4j.
    """

    print("\n==============================")
    print("Building Neo4j Knowledge Graph")
    print("==============================")

    java_files = read_java_files(project_path)

    total_files = len(java_files)
    total_classes = 0
    total_methods = 0

    # read_java_files() returns a LIST
    for java_file in java_files:

        file_path = java_file["path"]
        code = java_file["code"]

        print(f"\nProcessing: {file_path}")

        parsed = parse_java_file(code)

        if not parsed:
            continue
        
        print(f"Processing: {file_path}")
        print(parsed)

        store_java(parsed)

        total_classes += 1
        total_methods += len(parsed["methods"])

    print("\n==============================")
    print("Graph Build Completed")
    print("==============================")
    print(f"Java Files : {total_files}")
    print(f"Classes    : {total_classes}")
    print(f"Methods    : {total_methods}")


if __name__ == "__main__":

    PROJECT_PATH = "../backend/src"

    build_graph(PROJECT_PATH)