# CSE 4288 - Experiment I : Depth First Search (DFS)
# Run this file:  python lab_3_dfs.py
# It asks for start and goal, runs DFS, and saves two PNG files.

import io
from contextlib import redirect_stdout

from visualize import draw_graph, draw_output    # drawing helper file

# Graph (adjacency list): node -> list of children, left to right
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': ['H'],
    'F': [],
    'G': [],
    'H': []
}

# Position of each node on the picture (tree shape)
pos = {'A': (4, 4.5),
       'B': (2, 3), 'C': (6, 3),
       'D': (1, 1.5), 'E': (3, 1.5), 'F': (5, 1.5), 'G': (7, 1.5),
       'H': (3, 0)}


def dfs(start, goal):
    stack = [start]          # LIFO: last pushed node is explored first
    visited = []             # nodes in the order they were visited
    parent = {start: None}   # to rebuild the path at the end
    step = 1

    while stack:
        node = stack.pop()                       # take the top of the stack
        if node in visited:
            continue
        visited.append(node)

        print(f"Step {step}: Visit {node}")
        step += 1

        if node == goal:
            # Rebuild path by following parents back to start
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            print("\nGoal reached!")
            print("Visit Order  :", " -> ".join(visited))
            print("Path         :", " -> ".join(path))
            print("Nodes visited:", len(visited))
            return path, visited

        # Push children in reverse so the LEFT child is on top (explored first)
        for child in reversed(graph[node]):
            if child not in visited:
                parent.setdefault(child, node)
                stack.append(child)

        print(f"     Stack (top first): {list(reversed(stack))}")

    print("\nGoal not found")
    print("Visit Order  :", " -> ".join(visited))
    return None, visited


def ask_node(message):
    # Keep asking until the user types a valid node name
    while True:
        node = input(message).strip().upper()
        if node in graph:
            return node
        print("Invalid node! Choose from:", ", ".join(graph))


if __name__ == "__main__":
    nodes = "/".join(graph)
    start = ask_node(f"Enter start node ({nodes}): ")
    goal = ask_node(f"Enter goal node ({nodes}): ")

    # Run DFS and capture everything it prints
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        path, visited = dfs(start, goal)
    result = buffer.getvalue()
    print(result)

    # File names come from the input, e.g. dfs_graph_A_to_G.png
    graph_file = f"dfs_graph_{start}_to_{goal}.png"
    output_file = f"dfs_output_{start}_to_{goal}.png"

    if path:
        title = (f"DFS  (Start = {start}, Goal = {goal})\n"
                 f"Path: {' -> '.join(path)}   (red number = visit order)")
    else:
        title = f"DFS  (Start = {start}, Goal = {goal})\nGoal not found"

    output_text = f"Enter start node: {start}\nEnter goal node: {goal}\n\n" + result
    draw_graph(graph, pos, start, goal, path, graph_file, title,
               visit_order=visited)
    draw_output(output_text, output_file, heading="DFS Output")

    print("Saved", graph_file)
    print("Saved", output_file)
