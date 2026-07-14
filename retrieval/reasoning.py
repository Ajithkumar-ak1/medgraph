class ReasoningBuilder:

    def __init__(self):
        pass

    def extract_triples(self, paths):

        triples = []

        for item in paths:

            path = item["path"]

            relationship = path.relationships[0]

            triples.append({

                "head": relationship.start_node["name"],
                "relation": relationship.type,
                "tail": relationship.end_node["name"]

            })

        return triples
    
    def group_triples(self, triples):

        groups = []

        visited = set()

        for i, triple in enumerate(triples):

            if i in visited:
                continue

            group = []

            queue = [i]

            visited.add(i)


            while queue:

                current_index = queue.pop()

                current = triples[current_index]

                group.append(current)


                current_entities = {
                    current["head"],
                    current["tail"]
                }


                for j, other in enumerate(triples):

                    if j in visited:
                        continue


                    other_entities = {
                        other["head"],
                        other["tail"]
                    }


                    # Check shared entity

                    if current_entities.intersection(other_entities):

                        queue.append(j)

                        visited.add(j)


            groups.append(group)


        return groups
    

    def build_chain(self, groups):

        chains = []

        for group in groups:

            lines = []

            entities = set()

            for triple in group:

                head = triple["head"]
                relation = triple["relation"].replace("_", " ").lower()
                tail = triple["tail"]

                entities.add(head)
                entities.add(tail)

                lines.append(
                    f"- {head} {relation} {tail}."
                )


            chain = []

            chain.append(
                "Connected reasoning chain:"
            )

            chain.extend(lines)

            chain.append(
                f"\nShared entities: {', '.join(entities)}"
            )


            chains.append(
                "\n".join(chain)
            )


        return "\n\n".join(chains)
    
    def remove_duplicates(self, triples):

        unique = []

        seen = set()

        for triple in triples:

            key = (
                triple["head"],
                triple["relation"],
                triple["tail"]
            )

            if key not in seen:

                seen.add(key)
                unique.append(triple)

        return unique