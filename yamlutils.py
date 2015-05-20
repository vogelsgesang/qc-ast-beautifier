import yaml
from collections import OrderedDict

class SafeOrderedDumper(yaml.SafeDumper):
    """ 
    A Yaml dumper which is able to store OrderedDicts

    Usage: `yaml.dump(data, Dumper=SafeOrderedDumper)`
    """
    #: the tag used to represent the OrderedDict in Yaml
    _odict_tag = u'tag:yaml.org,2002:map'

    def __init__(self, *args, **kwargs):
        super(SafeOrderedDumper, self).__init__(*args, **kwargs)
        self.add_representer(OrderedDict, self.represent_odict)

    def represent_odict(self, dump, mapping, flow_style=None):
        "Like BaseRepresenter.represent_mapping, but does not issue the sort()."
        value = []
        node = yaml.MappingNode(self._odict_tag, value, flow_style=flow_style)
        if dump.alias_key is not None:
            dump.represented_objects[dump.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            mapping = mapping.items()
        for item_key, item_value in mapping:
            node_key = dump.represent_data(item_key)
            node_value = dump.represent_data(item_value)
            if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if dump.default_flow_style is not None:
                node.flow_style = dump.default_flow_style
            else:
                node.flow_style = best_style
        return node
