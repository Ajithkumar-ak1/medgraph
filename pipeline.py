from embedding.model import model
from retrieval.vector_search import vector_search
from retrieval.evidence_builder import build_evidence
from retrieval.entity_anchor_traversal import EntityAnchorTraversal
from retrieval.context_builder import build_context
from retrieval.entity_anchor_traversal import EntityAnchorTraversal
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

    # 3. Build entity scores
    entity_scores = {
        r["name"]: r["score"]
        for r in results
    }

    # 4. Entity Anchor Traversal

    traversal = EntityAnchorTraversal(
        query_embedding=embedding,
        entity_scores=entity_scores,
        max_hops=2,
        beam_width=5
    )

    ranked_paths = traversal.traverse(results)

    print("\n========== Entity Anchor Traversal ==========")

    for item in ranked_paths:

        print()

        print("Score :", round(item["score"], 3))

        path = item["path"]

        nodes = path.nodes
        rels = path.relationships

        print(nodes[0]["name"])

        for i in range(len(rels)):

            print("  |")

            print(" ", rels[i].type)

            print("  |")

            print(nodes[i + 1]["name"])

        print("-------------------------")

    


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

    print("========== Context ==========")
    print(context)
    # 7. LLM
    answer = generate_answer(
        question,
        context
    )


    return answer