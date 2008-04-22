#!/usr/bin/env python
# coding= utf-8
from django import template

register = template.Library()

class CounterNode(template.Node):
    def __init__(self, name, start=0):
        self.name = name
        self.start = start
    
    def render(self, context):
        if not context.has_key(self.name):
            context[self.name] = self.start
        else:
            context[self.name] += 1
        return str(context[self.name])

def counter(parser, token):
    # This version uses a regular expression to parse tag contents.
    # TODO: add "step" argument: the interval to count by
    # TODO: add "direction" argument: ascending or descending
    import re
    args = token.split_contents()
    args.reverse()
    
    tag_name = args.pop()
    
    if not len(args):
        name = ''
    else:
        name = args.pop()
        if not (name[0] == name[-1] and name[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        name = name[1:-1]
    if not name:
        name = 'default'
    
    start = 0
    if not len(args):
        start = 0
    else:
        start = args.pop()
        start = int(start)
    
    return CounterNode(name, start)

register.tag('counter', counter)
