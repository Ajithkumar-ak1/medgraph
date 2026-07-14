from embedding.model import model
from retrieval.vector_search import vector_search
from retrieval.evidence_builder import build_evidence
from retrieval.entity_anchor_traversal import EntityAnchorTraversal
from retrieval.context_builder import build_context
from retrieval.entity_anchor_traversal import EntityAnchorTraversal
from retrieval.reasoning import ReasoningBuilder

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
    # 5. Reasoning Chain

    reasoning_builder = ReasoningBuilder()


    triples = reasoning_builder.extract_triples(
        ranked_paths
    )

    triples = reasoning_builder.remove_duplicates(
        triples
    )


    groups = reasoning_builder.group_triples(
        triples
    )


    context = reasoning_builder.build_chain(
        groups
    )


    print("\n========== Reasoning Context ==========")
    print(context)
    print("======================================")
    # 7. LLM
    answer = generate_answer(
        question,
        context
    )


    return answer