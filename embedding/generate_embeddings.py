from embedding.model import get_embedding
from graph import get_all_nodes, save_embedding

nodes = get_all_nodes()

print(f"Found {len(nodes)} nodes")

for node in nodes:

    text = f"{node['label']} {node['name']}"

    embedding = get_embedding(text)

    save_embedding(node["id"], embedding)

    print(f"Embedded {node['name']}")

print("Finished")