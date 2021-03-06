import networkx as nx
from typing import Optional

from bokeh.io import output_file, show
from bokeh.models import (
    BoxSelectTool,
    Circle,
    NodesOnly,
    EdgesAndLinkedNodes,
    HoverTool,
    MultiLine,
    NodesAndLinkedEdges,
    Plot,
    Range1d,
    TapTool,
    BoxZoomTool,
    ResetTool,
    WheelZoomTool,
)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx


def build_plot(term: str, g: nx.Graph, fpath: Optional[str] = None):
    plot = Plot(
        plot_width=1200,
        plot_height=800,
        x_range=Range1d(-1.1, 1.1),
        y_range=Range1d(-1.1, 1.1),
    )
    plot.title.text = f""""{term}" google vs. graph"""

    plot.add_tools(TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(g, nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(
        size="total_weight",
        fill_color=Spectral4[0]
    )
    graph_renderer.node_renderer.selection_glyph = Circle(
        size=15, fill_color=Spectral4[2]
    )
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="#CCCCCC", line_alpha=0.8, line_width="weight"
    )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color=Spectral4[2], line_width=5
    )
    graph_renderer.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral4[1], line_width=5
    )

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)
    node_hover_tool = HoverTool(tooltips=[("name", "@name")])
    plot.add_tools(
        node_hover_tool, BoxZoomTool(), ResetTool(), TapTool(), WheelZoomTool()
    )

    if not fpath:
        fpath = f"vs_graph_{term.replace(' ', '_').replace('/', '-')}.html"
    output_file(fpath)
    show(plot)
