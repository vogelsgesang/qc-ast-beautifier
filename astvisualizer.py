#!/usr/bin/python3
import yaml
import inspect
import graphviz as gv
import subprocess
import numbers
from uuid import uuid4 as uuid

class GraphRenderer:
    """
    this class is capable of rendering data structures consisting mostly of
    dicts and lists as a graph using graphviz
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
        if isinstance(node, (str, numbers.Number)) or node is None:
            node_id = uuid()
        else:
            node_id = id(node)
        node_id = str(node_id)

        if node_id not in self._rendered_nodes:
            self._rendered_nodes.add(node_id)
            if isinstance(node, dict):
                self._render_dict(node, node_id)
            elif isinstance(node, list):
                self._render_list(node, node_id)
            else:
                self._graph.node(node_id, label=str(node))

        return node_id


    def _render_dict(self, node, node_id):
        self._graph.node(node_id, label=node.get("node_type", "[dict]"))
        for key, value in node.items():
            if key == "node_type":
                continue
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, label=key)


    def _render_list(self, node, node_id):
        self._graph.node(node_id, label="[list]")
        for idx, value in enumerate(node):
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, label=str(idx))


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
