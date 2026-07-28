from graph.neo4j_client import get_session


def get_methods(type_name):

    with get_session() as session:

        result = session.run("""
            MATCH (t:JavaType {name:$name})-[:HAS_METHOD]->(m:Method)
            RETURN m.name AS method
        """, name=type_name)

        return [r["method"] for r in result]


def get_uses(type_name):

    with get_session() as session:

        result = session.run("""
            MATCH (t:JavaType {name:$name})-[:USES]->(d:JavaType)
            RETURN d.name AS dependency
        """, name=type_name)

        return [r["dependency"] for r in result]


def get_extends(type_name):

    with get_session() as session:

        result = session.run("""
            MATCH (t:JavaType {name:$name})-[:EXTENDS]->(p:JavaType)
            RETURN p.name AS parent
        """, name=type_name)

        return [r["parent"] for r in result]


def get_implements(type_name):

    with get_session() as session:

        result = session.run("""
            MATCH (t:JavaType {name:$name})-[:IMPLEMENTS]->(i:JavaType)
            RETURN i.name AS interface
        """, name=type_name)

        return [r["interface"] for r in result]
    
def get_calls(type_name):

    with get_session() as session:

        result = session.run("""
            MATCH (t:JavaType {name:$name})-[:HAS_METHOD]->(m1:Method)
            MATCH (m1)-[:CALLS]->(m2:Method)
            RETURN m1.name AS caller,
                   m2.name AS callee
        """, name=type_name)

        return [
            (r["caller"], r["callee"])
            for r in result
        ]