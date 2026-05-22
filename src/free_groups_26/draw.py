from graph_tool import VertexPropertyMap
from graph_tool.draw import graph_draw
from .whitehead_graph import WhiteheadGraph

__all__ = ["draw_graph"]


def draw_graph(
    whg: WhiteheadGraph,
    output: str | None = None,
    partition: VertexPropertyMap | None = None,
):
    """
    Draws a Whitehead Graph.

    :param output: The output file for the graph. If left blank in an interactive environment like a Jupyter Notebook, it will use the standard output.
    :param part: The partition to be followed when drawing the graph.

    """
    v_text = whg.new_vertex_property(
        "string", vals=[str(whg.letter_map[v]) for v in whg.iter_vertices()]
    )
    graph_draw(
        whg,
        edge_text=whg.weight_map,
        vertex_text=v_text,
        output=output,
        vertex_fill_color=partition,
    )
