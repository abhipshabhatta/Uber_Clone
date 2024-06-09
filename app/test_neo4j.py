from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_location(self, location_id, name):
        with self.driver.session() as session:
            session.run(
                "CREATE (a:Location {id: $location_id, name: $name})",
                location_id=location_id, name=name
            )

    def create_connection(self, start_id, end_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Location {id: $start_id}), (b:Location {id: $end_id})
                CREATE (a)-[:CONNECTED_TO]->(b)
                """,
                start_id=start_id, end_id=end_id
            )

    def find_shortest_path(self, start_id, end_id):
        print(f"Finding path from {start_id} to {end_id}")
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (start:Location {id: $start_id}), (end:Location {id: $end_id}),
                p = shortestPath((start)-[*]-(end))
                RETURN nodes(p) AS nodes, relationships(p) AS relationships
                """, 
                start_id=start_id, end_id=end_id
            )
            path = result.single()
            if path:
                print("Raw path data:", path)
                nodes = [node["name"] for node in path["nodes"]]
                relationships = path["relationships"]
                return {"nodes": nodes, "relationships": relationships}
            print("No path found in result")
            return None

# Test data setup
def test_find_shortest_path():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "123456789"  # Replace with your Neo4j password

    neo4j_client = Neo4jClient(uri, user, password)

    # Create nodes and relationships in Neo4j for the test
    neo4j_client.create_location('antony_id', 'antony')
    neo4j_client.create_location('Troyes_id', 'Troyes')
    neo4j_client.create_location('some_intermediate_location_id', 'some_intermediate_location')

    neo4j_client.create_connection('antony_id', 'some_intermediate_location_id')
    neo4j_client.create_connection('some_intermediate_location_id', 'Troyes_id')

    # Test data for shortest path
    start_id = 'antony_id'
    end_id = 'Troyes_id'

    result = neo4j_client.find_shortest_path(start_id, end_id)
    
    if result:
        print("Shortest path found:")
        print("Nodes:", result["nodes"])
        print("Relationships:", result["relationships"])
    else:
        print("No path found")

    neo4j_client.close()

if __name__ == "__main__":
    test_find_shortest_path()
