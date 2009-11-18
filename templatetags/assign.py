#!/usr/bin/env python
# coding= utf-8
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument


register = template.Library()


class AssignNode(template.Node):
    def __init__(self, nodelist, arguments):
        self.nodelist = nodelist
        self.name = arguments['name']
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        context[name] = self.nodelist.render(context)
        return ''


@register.tag
def assign(parser, token):
    default_arguments = {}
    default_arguments['name'] = '"assign"'
    arguments = decode_tag_arguments(token, default_arguments)
    
    nodelist = parser.parse(('endassign',))
    parser.delete_first_token()
    return AssignNode(nodelist, arguments)
