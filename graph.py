from neo4j import GraphDatabase
from neo4j.graph import Path
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

def get_neighbors(entity_name):

    query = """
    MATCH (n:Entity {name:$name})-[r]-(m)

    RETURN
        n,
        r,
        m
    """

    with driver.session(database=database_name) as session:

        result = session.run(
            query,
            name=entity_name
        )

        return [record.data() for record in result]
    

def get_neighbor_paths(entity_name):

    query = """
    MATCH path=(n:Entity {name:$name})-[r]-(m)

    RETURN
        path,
        m AS neighbor,
        m.embedding AS embedding
    """

    with driver.session(database=database_name) as session:

        result = session.run(
            query,
            name=entity_name
        )

        return [
            {
                "path": record["path"],
                "neighbor": record["neighbor"],
                "embedding": record["embedding"]
            }
            for record in result
        ]


def get_last_node(path: Path):
    """
    Return last node of a Neo4j Path.
    """

    return path.nodes[-1]


def get_path_length(path: Path):
    """
    Return number of relationships.
    """

    return len(path.relationships)


def print_path(path: Path):

    output = []

    output.append(path.nodes[0]["name"])

    for i, rel in enumerate(path.relationships):

        output.append(rel.type)

        output.append(path.nodes[i + 1]["name"])

    print(" -> ".join(output))