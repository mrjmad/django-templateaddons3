#!/usr/bin/env python
# coding= utf-8
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument

register = template.Library()

class CounterNode(template.Node):
    def __init__(self, arguments):
        self.name = arguments['name']
        self.start = arguments['start']
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        start = parse_tag_argument(self.start, context)
        if not context.has_key(name):
            context[name] = start
        else:
            context[name] += 1
        return str(context[name])

def counter(parser, token):
    # TODO: add "step" argument: the interval to count by
    # TODO: add "direction" argument: ascending or descending
    
    default_arguments = {}
    default_arguments['name'] = 'default'
    default_arguments['start'] = 0
    arguments = decode_tag_arguments(token, default_arguments)
    
    return CounterNode(arguments)

register.tag('counter', counter)
