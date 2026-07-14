from graph import driver
import os
from dotenv import load_dotenv

load_dotenv()

database_name = os.getenv("NEO4J_DATABASE")


def vector_search(embedding, top_k=5):

    with driver.session(database=database_name) as session:

        result = session.run(
            """
            CALL db.index.vector.queryNodes(
                'node_embeddings',
                $top_k,
                $embedding
            )
            YIELD node, score

            RETURN node.name AS name, score
            """,
            embedding=embedding.tolist(),
            top_k=top_k
        )

        return [
            record.data()
            for record in result
            if record["score"] > 0.75
        ]