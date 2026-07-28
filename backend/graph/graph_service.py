from graph.graph_builder import (
    create_type,
    create_method,
    create_uses,
    create_extends,
    create_implements,
    create_calls
)

from graph.graph_queries import (
    get_methods,
    get_uses,
    get_calls,
    get_extends,
    get_implements
)


def store_java(parsed):
    """
    Store parsed Java information in Neo4j.
    """

    # Create Java Type
    create_type(
        parsed["name"],
        parsed["type"]
    )

    # Create Methods
    for method in parsed["methods"]:
        create_method(
            parsed["name"],
            method
        )

    # Store USES relationships
    for dependency in parsed["uses"]:
        create_uses(
            parsed["name"],
            dependency
        )

    # Store EXTENDS relationships
    for parent in parsed["extends"]:
        create_extends(
            parsed["name"],
            parent
        )

    # Store IMPLEMENTS relationships
    for interface in parsed["implements"]:
        create_implements(
            parsed["name"],
            interface
        )

    # Store CALLS relationships
    for method_name, called_methods in parsed["calls"].items():

        for called_method in called_methods:

            create_calls(
                parsed["name"],
                method_name,
                called_method
            )


def get_business_context(type_name):
    """
    Retrieve business context from Neo4j.
    """

    methods = get_methods(type_name)
    uses = get_uses(type_name)
    calls = get_calls(type_name)
    extends = get_extends(type_name)
    implements = get_implements(type_name)

    context = f"Java Type: {type_name}\n\n"

    if uses:
        context += "USES:\n"
        for dependency in uses:
            context += f"- {dependency}\n"

    if extends:
        context += "\nEXTENDS:\n"
        for parent in extends:
            context += f"- {parent}\n"

    if implements:
        context += "\nIMPLEMENTS:\n"
        for interface in implements:
            context += f"- {interface}\n"

    if methods:
        context += "\nMETHODS:\n"
        for method in methods:
            context += f"- {method}\n"

    if calls:
        context += "\nCALLS:\n"
        for caller, callee in calls:
            context += f"- {caller} -> {callee}\n"

    return context