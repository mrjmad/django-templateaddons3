#!/usr/bin/env python
# coding= utf-8
from django import template

register = template.Library()

class ForRangeNode(template.Node):
    def __init__(self, nodelist, start='0', stop='0', step='1'):
        self.nodelist = nodelist
        self.start = start
        self.stop = stop
        self.step = step
        self.separator = ''
    
    def render(self, context):
        # TODO: assign values to the context (like "for")
        output = []
        
        start = self.start
        if start:
            if not (start[0] == start[-1] and start[0] in ('"', "'")):
                start = template.resolve_variable(start, context)
            else:
                start = start[1:-1]
        else:
            start = '0'
        start = int(start)
        
        stop = self.stop
        if(stop):
            if not (stop[0] == stop[-1] and stop[0] in ('"', "'")):
                stop = template.resolve_variable(stop, context)
            else:
                stop = stop[1:-1]
        else:
            stop = '0'
        stop = int(stop)
        
        step = self.step
        if(step):
            if not (step[0] == step[-1] and step[0] in ('"', "'")):
                step = template.resolve_variable(step, context)
            else:
                step = step[1:-1]
        else:
            step = '1'
        step = int(step)
        
        for i in range(start, stop, step):
            output.append(self.nodelist.render(context))
        output = self.separator.join(output)
        return output

def forrange(parser, token):
    # TODO: add separator parameter
    import re
    args = token.split_contents()
    args.reverse()
    
    tag_name = args.pop()
    
    start = '0'
    stop = '0'
    step = '1'
    
    if len(args):
        stop = args.pop()
        
        if len(args):
            start = stop
            stop = args.pop()
    
            if len(args):
                step = args.pop()
    
    nodelist = parser.parse(('endforrange',))
    parser.delete_first_token()
    return ForRangeNode(nodelist, start, stop, step)

register.tag('forrange', forrange)
