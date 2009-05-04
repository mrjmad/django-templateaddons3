#!/usr/bin/env python
# coding= utf-8
from django import template
from templateutils.utils import decode_tag_arguments, parse_tag_argument
from django.utils.encoding import force_unicode


register = template.Library()


class JavascriptContainer(object):
    """
    Content storage.
    """
    def __init__(self):
        self.nodes = []
        self.separator = u'\n'
        self.unique = True
    
    def __unicode__(self):
        if self.unique:
            self.remove_duplicates()
        return u'%s' % self.separator.join(self.nodes)
    
    def remove_duplicates(self):
        seen = set()
        self.nodes = [x for x in self.nodes if x not in seen and not seen.add(x)]
    
    def append(self, content):
        self.nodes.append(content)


javascript_container = JavascriptContainer()


class JavascriptRenderNode(template.Node):
    def render(self, context):
        return u'%s' % javascript_container


@register.tag
def javascript_render(parser, token):
    return JavascriptRenderNode()


class JavascriptAssignNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        content = self.nodelist.render(context)
        javascript_container.append(content)
        return u''


@register.tag
def javascript_assign(parser, token):
    default_arguments = {}
    arguments = decode_tag_arguments(token, default_arguments)
    nodelist = parser.parse(('endjavascript_assign',))
    parser.delete_first_token()
    return JavascriptAssignNode(nodelist)


@register.simple_tag
def javascript_reset():
    global javascript_container
    javascript_container = JavascriptContainer()
    return u''
