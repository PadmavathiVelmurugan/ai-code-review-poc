from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"   # Use your actual password

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connected Successfully' AS msg")
        print(result.single()["msg"])

if __name__ == "__main__":
    test_connection()