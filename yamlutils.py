import yaml
from collections import OrderedDict

class SafeOrderedDumper(yaml.SafeDumper):
    """
    A Yaml dumper which is able to serialize OrderedDicts

    Usage: `yaml.dump(data, Dumper=SafeOrderedDumper)`
    """
    #: the tag used to represent the OrderedDict in Yaml
    _odict_tag = u'tag:yaml.org,2002:map'

    def __init__(self, *args, **kwargs):
        super(SafeOrderedDumper, self).__init__(*args, **kwargs)
        self.add_representer(OrderedDict, self.represent_odict)

    def represent_odict(self, _, mapping):
        "Like BaseRepresenter.represent_mapping, but does not issue the sort()."
        return self.represent_mapping(self._odict_tag, mapping.items());
