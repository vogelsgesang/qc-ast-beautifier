#!/usr/bin/python
import sys
import yaml
from yamlutils import SafeOrderedDumper
from collections import OrderedDict

humanReadableOrder = ['node_type', 'test', 'orelse', 'body']

def createCmpFunctionForOrderRelation(incompleteOrder):
    """
    returns a function which can be used by the builtin `sorted` as cmp function

    `incompleteOrder` must be an array listing the values in increasing order.
    The returned cmp functions uses the ordering specified by `incompleteOrder` whenever possible.
    """
    def compareFnct(x,y):
        if x in incompleteOrder and y in incompleteOrder:
            return incompleteOrder.index(x) - incompleteOrder.index(y)
        elif x in incompleteOrder and y not in incompleteOrder:
            return -1
        elif x not in incompleteOrder and y in incompleteOrder:
            return 1
        else:
            return cmp(x,y)
    return compareFnct

def reorderAstForHumans(astTree):
    """
    brings the elements of the AST in a human readable order
    """
    if isinstance(astTree, dict):
        processedItems = map(lambda e: [e[0], reorderAstForHumans(e[1])], astTree.items())
        return OrderedDict(sorted(processedItems, key=lambda e: e[0], cmp=createCmpFunctionForOrderRelation(humanReadableOrder)))
    if isinstance(astTree, list):
        return map(reorderAstForHumans, astTree)
    else:
        return astTree

data = yaml.load(sys.stdin)
print(yaml.dump(reorderAstForHumans(data), Dumper=SafeOrderedDumper))
