from graph import get_neighbor_paths, print_path

paths = get_neighbor_paths("Diabetes")

for p in paths:
    print_path(p)