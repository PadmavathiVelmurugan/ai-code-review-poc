from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"   # replace if you changed it

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

try:
    with driver.session() as session:
        result = session.run("RETURN 'Neo4j Connected Successfully' AS message")
        print(result.single()["message"])
finally:
    driver.close()