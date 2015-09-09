#!/usr/bin/python3
import yaml
import inspect
import graphviz as gv
import subprocess

class GraphRenderer:
    """
    this class is capable of rendering arbitrary data structures as a graph using graphviz
    """
    graphattrs = {
        'labelloc': 't',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'margin': '0',
    }
    nodeattrs = {
        'color': 'white',
        'fontcolor': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    }
    edgeattrs = {
        'color': 'white',
        'fontcolor': 'white',
    }

    _graph = None
    _rendered_nodes = None

    @staticmethod
    def _escape_dot_label(str):
        return str.replace("\\", "\\\\").replace("|", "\\|")

    def _render_node(self, node):
        if id(node) in self._rendered_nodes:
            return
        self._rendered_nodes.add(id(node))
        node_id = node_id
        graph = self._graph
        if isinstance(node, dict):
            graph.node(node_id, label=node.get("node_type"))
            for key, value in node.items():
                if key == "node_type": continue
                self._render_node(value)
                graph.edge(node_id, str(id(value)), label=key)
        elif isinstance(node, list):
            graph.node(node_id, label="[list]")
            for idx, value in enumerate(node):
                self._render_node(value)
                graph.edge(node_id, str(id(value)), label=str(idx))
        else:
            graph.node(node_id, label=str(node))

    def render(self, data, *, label=None):
        # create the graph
        graphattrs = self.graphattrs.copy()
        if label is not None:
            graphattrs['label'] = label
        graph = gv.Digraph(graph_attr = graphattrs, node_attr = self.nodeattrs, edge_attr = self.edgeattrs)

        # recursively draw all the nodes and edges
        self._graph = graph
        self._rendered_nodes = set()
        self._render_node(data)
        self._graph = None
        self._rendered_nodes = None

        # display the graph
        graph.format = "pdf"
        graph.render("test")
        subprocess.Popen(['xdg-open', "test.pdf"])

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        data = yaml.load(sys.stdin)
        label = "<graph read from stdin>"
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as instream:
            data = yaml.load(instream)
        label = sys.argv[1]
    else:
        print(inspect.cleandoc("""
        Usage: astvisualizer.py [infile]

        If infile is not given, input will be read from stdin
        """))
        exit(1)

    renderer = GraphRenderer()
    renderer.render(data, label=label)
