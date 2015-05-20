#!/usr/bin/python3
import yaml
from functools import cmp_to_key

class HumanFriendlyAstDumper(yaml.SafeDumper):
    human_readable_order = []

    def __init__(self, *args, **kwargs):
        super(HumanFriendlyAstDumper, self).__init__(*args, **kwargs)
        self.add_representer(dict, self.represent_dict)
        self._sort_key = self._createKeyFunc(self.human_readable_order)

    def represent_dict(self, _, data):
        items = sorted(data.items(), key=self._sort_key)
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

    HumanFriendlyAstDumper.human_readable_order = ['node_type', 'test', 'orelse', 'body']
    data = yaml.load(sys.stdin)
    print(yaml.dump(data, Dumper=HumanFriendlyAstDumper))
