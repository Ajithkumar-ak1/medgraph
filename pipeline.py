from embedding.model import model
from retrieval.vector_search import vector_search
from retrieval.graph_expansion import expand_nodes
from retrieval.path_ranker import rank_paths
from retrieval.evidence_builder import build_evidence
from retrieval.context_builder import build_context
from llm import generate_answer


def graphrag(question):

    # 1. Embed question
    embedding = model.encode(question)


    # 2. Vector search
    results = vector_search(
        embedding,
        top_k=10
    )
    print("\n========== Vector Search Results ==========")
    print(results)

    print("\n====================")
    node_names = [
        r["name"]
        for r in results
    ]


    # 3. Graph expansion
    paths = expand_nodes(
        node_names
    )


    # 4. Ranking
    scores = {
        r["name"]: r["score"]
        for r in results
    }


    ranked_paths = rank_paths(
        paths,
        scores
    )
    print("\n========== Ranked Paths ==========")

    for item in ranked_paths:

        path = item["path"]

        print("Score:", item["score"])

        for node in path.nodes:
            print(node["name"])

        for rel in path.relationships:
            print(rel.type)

        print("----------------")


    # 5. Evidence
    evidence = build_evidence(
        ranked_paths
    )

    print("\n========== Evidence ==========")

    for e in evidence:
        print(e)

    print("==============================")


    # 6. Context
    context = build_context(
        evidence
    )


    # 7. LLM
    answer = generate_answer(
        question,
        context
    )


    return answer