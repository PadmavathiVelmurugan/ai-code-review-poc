from graph.graph_queries import get_related_java_types


def retrieve_graph_context(class_name):

    related = get_related_java_types(class_name)

    print("\n========== GRAPH CONTEXT ==========")

    print("Current class:", class_name)

    print("Related classes:")

    for r in related:
        print(" -", r)

    return related