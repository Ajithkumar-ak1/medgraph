RELATION_TEMPLATES = {

    "TREATS":
        "{source} treats {target}.",

    "SPECIALIZES_IN":
        "{source} specializes in {target}.",

    "HAS_SYMPTOM":
        "{source} has the symptom {target}.",

    "AFFECTS":
        "{source} affects {target}."
}

def build_evidence(ranked_paths):

    evidence = []

    for item in ranked_paths:

        path = item["path"]

        nodes = path.nodes
        relationships = path.relationships


        for i, rel in enumerate(relationships):

            start_node = rel.start_node
            end_node = rel.end_node


            source = start_node["name"]
            target = end_node["name"]

            relation = rel.type


            template = RELATION_TEMPLATES.get(
                relation,
                "{source} is related to {target}."
            )


            sentence = template.format(
                source=source,
                target=target
            )


            evidence.append(sentence)


    return list(set(evidence))