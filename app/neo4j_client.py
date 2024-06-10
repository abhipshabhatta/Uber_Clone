from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_shortest_path(self, start_name, end_name):
        print(f"Finding path from {start_name} to {end_name}")
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (start:Location {name: $start_name}), (end:Location {name: $end_name}),
                p = shortestPath((start)-[*]-(end))
                RETURN nodes(p) AS nodes, relationships(p) AS relationships
                """,
                start_name=start_name, end_name=end_name
            )
            path = result.single()
            if path:
                nodes = [node["name"] for node in path["nodes"]]
                return {"nodes": nodes, "relationships": path["relationships"]}
            print("No path found in result")
            return None
