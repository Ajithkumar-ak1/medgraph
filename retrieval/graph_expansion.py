from graph import driver
import os
from dotenv import load_dotenv

load_dotenv()

database_name = os.getenv("NEO4J_DATABASE")


def get_neighbor_paths(entity_name):

    query = """
    MATCH (n:Entity {name:$name})-[r]-(m)

    RETURN
        path=(n)-[r]-(m)
    """

    with driver.session(database=database_name) as session:

        result=session.run(
            query,
            name=entity_name
        )

        return [record["path"] for record in result]