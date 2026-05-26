import networkx as nx
import matplotlib.pyplot as plt

from networkx import Graph
from .letter import Letter
from .word import Word

type WhiteheadGraph = Graph[Letter]


def generate_whg(word: Word) -> WhiteheadGraph:
    """
    Generates a Whitehead Graph for the given word.
    """
    whg: WhiteheadGraph = Graph()
    cyclic = word.word + (word.word[0],)

    for i in range(len(cyclic) - 1):
        curr = cyclic[i].get_base()
        next = cyclic[i + 1].get_base()

        w_add = abs(cyclic[i].exp) - 1
        if w_add != 0:
            change_whg_edge_or_weight(whg, curr, curr.inv(), w_add)
        change_whg_edge_or_weight(whg, curr, next.inv())

    return whg


def change_whg_edge_or_weight(
    whg: WhiteheadGraph, v1: Letter, v2: Letter, weight: int = 1
) -> None:
    """
    Changes the edge weights for an edge if it exists, otherwise adds the given edge to the graph.
    """
    try:
        whg[v1][v2]["weight"] += weight
    except KeyError:
        _ = whg.add_edge(v1, v2, weight=weight)


def draw_graph(G: WhiteheadGraph) -> None:
    """
    Uses matplotlib to draw the given Whitehead Graph.
    """
    pos = nx.spring_layout(G)
    _ = nx.draw_networkx_nodes(G, pos, node_size=700)
    _ = nx.draw_networkx_labels(G, pos, font_size=20)
    _ = nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=1)
    edge_labels: dict[tuple[Letter, Letter], int] = nx.get_edge_attributes(G, "weight")
    _ = nx.draw_networkx_edge_labels(G, pos, edge_labels)
    ax = plt.gca()
    _ = ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
