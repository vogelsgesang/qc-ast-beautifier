#!/usr/bin/python3
import yaml
import inspect
from functools import cmp_to_key

class HumanFriendlyAstDumper(yaml.SafeDumper):
    default_order = ['node_type'] #by default, 'node_type' should be always the first element
    specialized_orders = {k: ['node_type'] + v for k,v in {
            'assign': ['targets', 'value'],
            'name': ['id', 'ctx'],
            'attribute': ['value', 'attr', 'ctx'],
            'tuple': ['elts', 'ctx'],
            'list': ['elts', 'ctx'],
            'dict': ['keys', 'values'],
            'listcomp': ['elt', 'generators'],
            'dictcomp': ['key', 'value', 'generators'],
            'comprehension': ['target', 'iter', 'ifs'],
            'boolop': ['op', 'values'],
            'binop': ['left', 'op', 'right'],
            'compare': ['left', 'opes', 'comparators'],
            'call': ['func', 'args', 'starargs', 'keywords', 'kwargs'],
            'if': ['test', 'body', 'orelse'],
            'for': ['target', 'iter', 'body', 'orelse'],
            'while': ['test', 'body', 'orelse'],
            'lambda': ['args', 'body'],
            'functiondef': ['name', 'args', 'decorator_list', 'docstring', 'body'],
            'classdef': ['name', 'bases', 'decorator_list', 'docstring', 'body'],
            'import': ['names'],
            'importfrom': ['module', 'level', 'names'],
            'alias': ['name', 'asname']
        }.items()}

    def __init__(self, *args, **kwargs):
        super(HumanFriendlyAstDumper, self).__init__(*args, **kwargs)
        self.add_representer(dict, self.represent_dict)
        #materialize the key functions
        self._default_key_fun = self._create_key_func(self.default_order)
        self._specialized_key_funs = {k: self._create_key_func(v) for k, v in self.specialized_orders.items()}

    def represent_dict(self, _, data):
        if 'node_type' in data and data['node_type'] in self._specialized_key_funs:
            key_fun = self._specialized_key_funs[data['node_type']]
        else:
            key_fun = self._default_key_fun
        items = sorted(data.items(), key=key_fun)
        return self.represent_mapping(u'tag:yaml.org,2002:map', items);

    @staticmethod
    def _create_key_func(order):
        """
        returns a function which can be used by the builtin `sorted` as key function

        `order` must be an array listing the values in increasing order.
        The returned cmp functions uses the ordering specified by `order` whenever possible.
        """
        def compare_func(x,y):
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
        return cmp_to_key(compare_func)

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        data = yaml.load(sys.stdin)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as instream:
            data = yaml.load(instream)
    else:
        print(inspect.cleandoc("""
        Usage: astdumper.py [infile]

        If infile is not given, input will be read from stdin
        """))
        exit(1)

    print(yaml.dump(data, Dumper=HumanFriendlyAstDumper))
