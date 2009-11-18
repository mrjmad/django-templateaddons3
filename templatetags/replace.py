#!/usr/bin/env python
# coding= utf-8
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument


register = template.Library()


class ReplaceNode(template.Node):
    def __init__(self, nodelist, arguments):
        self.nodelist = nodelist
        self.from_str = arguments["from"]
        self.to_str = arguments["to"]
    
    def render(self, context):
        from_str = parse_tag_argument(self.from_str, context)
        to_str = parse_tag_argument(self.to_str, context)
        
        output = self.nodelist.render(context)
        output = output.replace(from_str, to_str)
        return output


def replace_tag(parser, token):
    default_arguments = {}
    default_arguments['from'] = ''
    default_arguments['to'] = ''
    arguments = decode_tag_arguments(token, default_arguments)
    
    nodelist = parser.parse(('endreplace',))
    parser.delete_first_token()
    return ReplaceNode(nodelist, arguments)


register.tag('replace', replace_tag)
