from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    ),
    notifications_min_severity="OFF"
)

database_name = os.getenv("NEO4J_DATABASE")

def get_all_nodes():
    query = """
    MATCH (n)
    RETURN id(n) AS id,
           labels(n)[0] AS label,
           n.name AS name
    """

    with driver.session(database=database_name) as session:
        return [record.data() for record in session.run(query)]


def save_embedding(node_id, embedding):
    query = """
    MATCH (n)
    WHERE id(n)=$id
    SET n.embedding=$embedding
    """

    with driver.session(database=database_name) as session:
        session.run(
            query,
            id=node_id,
            embedding=embedding
        )