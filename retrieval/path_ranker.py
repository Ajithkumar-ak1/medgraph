# retrieval/path_ranker.py


RELATION_WEIGHTS = {
    "TREATS": 1.0,
    "HAS_SYMPTOM": 0.9,
    "CAUSES": 0.9,
    "AFFECTS": 0.8,
    "HAS_SIDE_EFFECT": 0.8,
    "RELATED_TO": 0.3
}


def calculate_path_score(path, entity_scores=None):
    """
    Rank graph paths based on:
    1. Relationship importance
    2. Vector similarity
    3. Path length
    """

    score = 0


    # Relationship score
    for rel in path.relationships:

        score += RELATION_WEIGHTS.get(
            rel.type,
            0.5
        )


    # Prefer shorter paths
    length_penalty = len(path.relationships) * 0.1

    score -= length_penalty


    # Entity similarity bonus
    if entity_scores:

        for node in path.nodes:

            name = node["name"]

            if name in entity_scores:
                score += entity_scores[name]


    return score



def rank_paths(paths, entity_scores=None, top_k=5):

    ranked = []

    for path in paths:

        score = calculate_path_score(
            path,
            entity_scores
        )

        ranked.append(
            {
                "path": path,
                "score": score
            }
        )


    ranked.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return ranked[:top_k]