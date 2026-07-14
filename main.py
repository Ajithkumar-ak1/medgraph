from embedding.model import model
from retrieval.vector_search import vector_search
from retrieval.graph_expansion import expand_nodes
from retrieval.path_ranker import rank_paths
from retrieval.evidence_builder import build_evidence
from retrieval.context_builder import build_context
from llm import generate_answer


question = """
What medicine treats a disease which has symptom headache
and affects brain?
"""


# Step 1
extracted = extract_entities(
    llm,
    question
)


print(extracted)


# Step 2
linked_entities = linker.link_entities(
    extracted["entities"]
)


print(linked_entities)



# Step 3
all_evidence = []


for entity in linked_entities:

    best_match = entity["matches"][0]

    evidence = evidence_retriever.get_evidence(
        best_match["name"]
    )

    all_evidence.extend(evidence)



print(all_evidence)