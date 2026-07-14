from graph import driver
import os
from dotenv import load_dotenv

load_dotenv()
database_name = os.getenv("NEO4J_DATABASE")

def expand_nodes(node_names, hops=2):
    """
    Expand retrieved nodes by traversing their neighbors.
    """

    query = f"""
    MATCH (n:Entity)
    WHERE n.name IN $names

    MATCH path=(n)-[*1..5]-(neighbor)

    RETURN path
    """

    with driver.session(database=database_name) as session:
        result = session.run(query, names=node_names)

        return [record["path"] for record in result]