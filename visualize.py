# CSE 4288 - Search Algorithms : drawing helper
# Used by lab_3.py (A*) and lab_3_dfs.py (DFS). Do not run this file directly.

import matplotlib
matplotlib.use("Agg")                    # save images without opening a window
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

R = 0.45  # node radius


def draw_graph(graph, pos, start, goal, path, filename, title,
               h=None, weighted=False, curved=(), visit_order=None):
    """
    graph       : node -> list of neighbors  (or (neighbor, cost) if weighted)
    pos         : node -> (x, y) position on the picture
    path        : final path found (drawn in green)
    h           : heuristic dict (shown inside node) - for A*
    visit_order : list of nodes in the order they were visited - for DFS
    """
    path_edges = set(zip(path, path[1:])) if path else set()

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    width = max(xs) - min(xs) + 2
    height = max(ys) - min(ys) + 2.2
    fig, ax = plt.subplots(figsize=(width * 1.15, height * 1.15))
    ax.set_aspect('equal')
    ax.axis('off')

    # Edges
    for u in graph:
        for item in graph[u]:
            v, c = item if weighted else (item, None)
            on_path = (u, v) in path_edges
            color = '#059669' if on_path else '#888888'
            rad = -0.25 if (u, v) in curved else 0.0
            # Start and end the arrow on the circle edges
            (x1, y1), (x2, y2) = pos[u], pos[v]
            d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            dx, dy = (x2 - x1) / d, (y2 - y1) / d
            p1 = (x1 + dx * R, y1 + dy * R)
            p2 = (x2 - dx * (R + 0.04), y2 - dy * (R + 0.04))
            ax.add_patch(FancyArrowPatch(
                p1, p2, connectionstyle=f"arc3,rad={rad}",
                arrowstyle='-|>', mutation_scale=22,
                lw=3.5 if on_path else 1.8, color=color,
                shrinkA=0, shrinkB=0, zorder=2))
            if weighted:
                mx = (pos[u][0] + pos[v][0]) / 2
                my = (pos[u][1] + pos[v][1]) / 2 + (0.75 if rad else 0.25)
                ax.text(mx, my, str(c), fontsize=14, ha='center', va='center',
                        color=color, fontweight='bold',
                        bbox=dict(facecolor='white', edgecolor='none', pad=1))

    # Nodes
    for n, (x, y) in pos.items():
        if n == start:
            fc, ec = '#d1fae5', '#059669'
        elif n == goal:
            fc, ec = '#fde68a', '#d97706'
        else:
            fc, ec = '#e8f0fe', '#1a56db'
        ax.add_patch(Circle((x, y), R, facecolor=fc, edgecolor=ec, lw=2.5, zorder=3))
        if n == goal:
            ax.add_patch(Circle((x, y), R + 0.08, fill=False, edgecolor=ec, lw=2, zorder=3))
        label = f"{n}\nh={h[n]}" if h else n
        ax.text(x, y, label, ha='center', va='center',
                fontsize=13 if h else 16, fontweight='bold', zorder=4)

        # Visit order number (DFS)
        if visit_order and n in visit_order:
            k = visit_order.index(n) + 1
            ax.text(x + R * 0.95, y + R * 0.95, str(k), ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white', zorder=5,
                    bbox=dict(boxstyle='circle,pad=0.25', facecolor='#dc2626',
                              edgecolor='none'))

    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(min(ys) - 1, max(ys) + 1.2)
    ax.set_title(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close()


def draw_output(text, filename, heading="Program Output"):
    lines = text.rstrip('\n').split('\n')
    step = 0.32                                   # line height in inches
    longest = max(len(l) for l in lines)
    fig_w = max(10, longest * 0.115 + 1)
    fig_h = step * len(lines) + 1.0
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='#1e1e1e')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#1e1e1e')
    ax.axis('off')

    ax.text(0.03, 1 - 0.3 / fig_h, heading,
            color='#cccccc', fontsize=14, family='monospace', va='top')
    y = 1 - 0.8 / fig_h
    for line in lines:
        color, weight = '#d4d4d4', 'normal'
        if line.startswith('Step'):
            color = '#dcdcaa'
        elif line.startswith(' '):
            color = '#9cdcfe'
        elif line.startswith(('Goal', 'Optimal', 'Total', 'Path', 'Visit')):
            color, weight = '#4ec9b0', 'bold'
        elif line.startswith('Enter'):
            color = '#ce9178'
        ax.text(0.03 * 10 / fig_w, y, line, color=color, fontsize=13,
                family='monospace', fontweight=weight, va='top')
        y -= step / fig_h

    plt.savefig(filename, dpi=200, facecolor='#1e1e1e')
    plt.close()
