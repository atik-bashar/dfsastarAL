# CSE 4288 - A* Search Algorithm (Python)
# Run this file:  python lab_3.py
# It asks for start and goal, runs A*, and saves two PNG files.

import heapq
import io
from contextlib import redirect_stdout

from visualize import draw_graph, draw_output    # drawing helper file

# Graph: node -> list of (neighbor, cost)
graph = {
    'S': [('A', 1), ('B', 4)],
    'A': [('B', 2), ('C', 5), ('G', 12)],
    'B': [('C', 2)],
    'C': [('G', 3)],
    'G': []
}

# Heuristic h(n): estimated cost from n to goal G
h = {'S': 7, 'A': 6, 'B': 2, 'C': 1, 'G': 0}

# Position of each node on the picture
pos = {'S': (0, 0), 'A': (2, 1.2), 'B': (4, -0.8), 'C': (6, 0.6), 'G': (8, 1.0)}


def a_star(start, goal):
    # Open list (priority queue) items: (f, g, node, path)
    open_list = [(h[start], 0, start, [start])]
    best_g = {start: 0}     # lowest g found so far for each node
    step = 1

    while open_list:
        f, g, node, path = heapq.heappop(open_list)   # node with lowest f

        if node == goal:
            print("\nGoal reached!")
            print("Optimal Path :", " -> ".join(path))
            print("Total Cost   :", g)
            return path, g

        if g > best_g[node]:      # a cheaper path to this node exists
            continue

        print(f"Step {step}: Expanding {node}  (g={g}, h={h[node]}, f={f})")
        step += 1

        for neighbor, cost in graph[node]:
            g_new = g + cost
            if g_new < best_g.get(neighbor, float('inf')):
                best_g[neighbor] = g_new
                f_new = g_new + h[neighbor]
                heapq.heappush(open_list,
                               (f_new, g_new, neighbor, path + [neighbor]))
                print(f"     add {neighbor}: g={g_new}, h={h[neighbor]}, f={f_new}")

    print("\nNo path found")
    return None, None


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

    # Run A* and capture everything it prints
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        path, cost = a_star(start, goal)
    result = buffer.getvalue()
    print(result)

    # File names come from the input, e.g. astar_graph_S_to_G.png
    graph_file = f"astar_graph_{start}_to_{goal}.png"
    output_file = f"astar_output_{start}_to_{goal}.png"

    output_text = f"Enter start node: {start}\nEnter goal node: {goal}\n\n" + result
    if path:
        title = (f"A* Search Graph  (Start = {start}, Goal = {goal})\n"
                 f"Optimal path: {' -> '.join(path)}   (Cost = {cost})")
    else:
        title = f"A* Search Graph  (Start = {start}, Goal = {goal})\nNo path found"

    draw_graph(graph, pos, start, goal, path, graph_file, title,
               h=h, weighted=True, curved={('A', 'G')})
    draw_output(output_text, output_file, heading="A* Search Output")

    print("Saved", graph_file)
    print("Saved", output_file)
