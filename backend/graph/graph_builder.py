from graph.neo4j_client import get_session


def create_type(type_name, kind):
    with get_session() as session:
        session.run("""
            MERGE (t:JavaType {name:$name})
            SET t.kind = $kind
        """,
        name=type_name,
        kind=kind)


def create_method(type_name, method_name):

    with get_session() as session:

        session.run("""
            MERGE (t:JavaType {name:$type_name})

            MERGE (m:Method {
                name:$method_name,
                owner:$type_name
            })

            MERGE (t)-[:HAS_METHOD]->(m)
        """,
        type_name=type_name,
        method_name=method_name)


def create_uses(type_name, dependency):
    with get_session() as session:
        session.run("""
            MERGE (t:JavaType {name:$type_name})
            MERGE (d:JavaType {name:$dependency})
            MERGE (t)-[:USES]->(d)
        """,
        type_name=type_name,
        dependency=dependency)


def create_extends(type_name, parent):
    with get_session() as session:
        session.run("""
            MERGE (t:JavaType {name:$type_name})
            MERGE (p:JavaType {name:$parent})
            MERGE (t)-[:EXTENDS]->(p)
        """,
        type_name=type_name,
        parent=parent)


def create_implements(class_name, interface_name):

    with get_session() as session:

        session.run("""
            MERGE (c:JavaType {name:$class_name})
            MERGE (i:JavaType {name:$interface_name})
            MERGE (c)-[:IMPLEMENTS]->(i)
        """,
        class_name=class_name,
        interface_name=interface_name)


def create_calls(type_name, method_name, called_method):

    with get_session() as session:

        session.run("""
            MERGE (m1:Method {
                name:$method_name,
                owner:$type_name
            })

            MERGE (m2:Method {
                name:$called_method
            })

            MERGE (m1)-[:CALLS]->(m2)
        """,
        type_name=type_name,
        method_name=method_name,
        called_method=called_method)