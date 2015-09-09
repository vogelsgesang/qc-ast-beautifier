#!/usr/bin/python3
import yaml
import inspect
import graphviz as gv
import subprocess

def escape_dot_label(str):
    return str.replace("\\", "\\\\").replace("|", "\\|")

def draw_graph(data, *, label=None):
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
    if label is not None:
        graphattrs['label'] = label

    graph = gv.Digraph(graph_attr = graphattrs, node_attr = nodeattrs, edge_attr = edgeattrs)

    rendered_nodes = set()

    def render_node(node):
        if id(node) in rendered_nodes:
            return
        rendered_nodes.add(id(node))
        if isinstance(node, dict):
            graph.node(str(id(node)), label=node.get("node_type"))
            for key, value in node.items():
                if key == "node_type": continue
                render_node(value)
                graph.edge(str(id(node)), str(id(value)), label=key)
        elif isinstance(node, list):
            graph.node(str(id(node)), label="[list]")
            for idx, value in enumerate(node):
                render_node(value)
                graph.edge(str(id(node)), str(id(value)), label=str(idx))
        elif isinstance(node, str):
            graph.node(str(id(node)), label=node)
        else:
            graph.node(str(id(node)), label=str(node))

    render_node(data)
    print(graph.source)
    graph.format = "pdf"
    graph.render("test")
    subprocess.Popen(['xdg-open', "test.pdf"])

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        data = yaml.load(sys.stdin)
        label = None
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

    draw_graph(data, label=label)
