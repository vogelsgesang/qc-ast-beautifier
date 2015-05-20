#!/usr/bin/python3
import yaml
import inspect
from functools import cmp_to_key

class HumanFriendlyAstDumper(yaml.SafeDumper):
    default_order = []
    specialized_orders = {}

    def __init__(self, *args, **kwargs):
        super(HumanFriendlyAstDumper, self).__init__(*args, **kwargs)
        self.add_representer(dict, self.represent_dict)
        #materialize the key functions
        self._default_key_fun = self._createKeyFunc(self.default_order)
        self._specialized_key_funs = {k: self._createKeyFunc(v) for k, v in self.specialized_orders.items()}

    def represent_dict(self, _, data):
        if 'node_type' in data and data['node_type'] in self._specialized_key_funs:
            key_fun = self._specialized_key_funs[data['node_type']]
        else:
            key_fun = self._default_key_fun
        items = sorted(data.items(), key=key_fun)
        return self.represent_mapping(u'tag:yaml.org,2002:map', items);

    def _createKeyFunc(self, order):
        """
        returns a function which can be used by the builtin `sorted` as key function

        `order` must be an array listing the values in increasing order.
        The returned cmp functions uses the ordering specified by `order` whenever possible.
        """
        def compareFunc(x,y):
            x = x[0]
            y = y[0]
            if x in order and y in order:
                return order.index(x) - order.index(y)
            elif x in order and y not in order:
                return -1
            elif x not in order and y in order:
                return 1
            else:
                return  -1 if x < y else 1 if x > y else 0
        return cmp_to_key(compareFunc)

if __name__ == '__main__':
    import sys

    HumanFriendlyAstDumper.specialized_orders = {
            'if': ['node_type', 'test', 'orelse', 'body']
            }
    HumanFriendlyAstDumper.default_order = ['node_type']

    if len(sys.argv) == 1:
        data = yaml.load(sys.stdin)
    elif len(sys.argv) == 2:
        instream = open(sys.argv[1], 'r')
        data = yaml.load(instream)
        instream.close()
    else:
        print(inspect.cleandoc("""
        Usage: astdumper.py [infile]

        If infile is not given, input will be read from stdin
        """))
        exit(1)

    print(yaml.dump(data, Dumper=HumanFriendlyAstDumper))
