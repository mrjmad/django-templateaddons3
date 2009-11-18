#!/usr/bin/env python
# coding= utf-8
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument


register = template.Library()


class IfInNode(template.Node):
    def __init__(self, value, list, nodelist_true, nodelist_false):
        self.value = value
        self.list = list
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfIn node>"

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.nodelist_true.get_nodes_by_type(nodetype))
        nodes.extend(self.nodelist_false.get_nodes_by_type(nodetype))
        return nodes

    def render(self, context):
        value = parse_tag_argument(self.value, context)
        list = parse_tag_argument(self.list, context)
        if value in list:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag
def ifin(parser, token):
    """
    Usage:
    Assume that {{ my_list }} is a list.
    {% ifin "a" my_list %}
        Yes
    {% else %}
        No
    {% endif %}
    """
    bits = token.contents.split()
    del bits[0]
    if not bits or len(bits)!=2:
        raise TemplateSyntaxError("'ifin' statement requires exactly two arguments")
    # Bits now looks something like this: ['a', 'b']
    nodelist_true = parser.parse(('else', 'endif'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfInNode(bits[0], bits[1], nodelist_true, nodelist_false)
