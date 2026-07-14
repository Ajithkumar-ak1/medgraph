from graph import get_neighbor_paths
from retrieval.path_ranker import rank_paths
import numpy as np
from retrieval.path_ranker import RELATION_WEIGHTS
from retrieval.similarity import cosine_similarity
from retrieval.reasoning import ReasoningBuilder

class EntityAnchorTraversal:

    def __init__(
        self,
        query_embedding,
        entity_scores,
        max_hops=2,
        beam_width=5
    ):

        self.query_embedding = query_embedding
        self.entity_scores = entity_scores
        self.max_hops = max_hops
        self.beam_width = beam_width

    def traverse(self, anchor_entities):

        frontier = anchor_entities

        visited = set()

        final_paths = []

        for hop in range(self.max_hops):

            print(f"\n========== Hop {hop+1} ==========")

            candidate_paths = []

            next_frontier = []

            for entity in frontier:

                entity_name = entity["name"]

                if entity_name in visited:
                    continue

                visited.add(entity_name)

                print(f"\nExpanding : {entity_name}")

                neighbors = get_neighbor_paths(entity_name)

                for candidate in neighbors:

                    path = candidate["path"]

                    neighbor = candidate["neighbor"]

                    neighbor_embedding = np.array(candidate["embedding"])

                    similarity = cosine_similarity(
                        self.query_embedding,
                        neighbor_embedding
                    )

                    relation = path.relationships[0].type

                    relation_weight = RELATION_WEIGHTS.get(
                        relation,
                        0.5
                    )

                    score = (
                        0.7 * similarity
                        +
                        0.3 * relation_weight
                    )

                    candidate_paths.append({

                        "path": path,

                        "score": score,

                        "neighbor": neighbor

                    })

            if not candidate_paths:
                break

            candidate_paths.sort(
                key=lambda x: x["score"],
                reverse=True
            )

            candidate_paths = candidate_paths[:self.beam_width]

            final_paths.extend(candidate_paths)

            for item in candidate_paths:

                path = item["path"]

                next_frontier.append({
                    "name": item["neighbor"]["name"],
                    "score": item["score"]
                })

            frontier = next_frontier

        final_paths.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return final_paths[:self.beam_width]