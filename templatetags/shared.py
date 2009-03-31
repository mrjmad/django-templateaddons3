#!/usr/bin/env python
# coding= utf-8
from django import template
from templateutils.utils import decode_tag_arguments, parse_tag_argument


register = template.Library()


class SharedContentProxy():
    """
    Content storage.
    """
    def __init__(self, content=u''):
        self.content = content
    
    def __unicode__(self):
        return self.content


class SharedContentNode(template.Node):
    """
    Make it possible to declare content blocks which output can still be 
    updated after declaration.
    """
    shared_content = {}
    
    def __init__(self, name):
        self.name = name
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        if name not in self.shared_content:
            self.shared_content[name] = SharedContentProxy()
        return self.shared_content[name]


@register.tag
def shared_content(parser, token):
    """
    Template tag to declare a "shared" content block. 
    Usage:
      {% load shared %}
      {% shared_content name="my_content" %}
    """
    default_arguments = {}
    default_arguments['name'] = '"default"'
    arguments = decode_tag_arguments(token, default_arguments)
    return SharedContentNode(arguments['name'])


class SharedAppendNode(template.Node):
    """
    Make it possible to update content of a shared block.
    """
    def __init__(self, nodelist, name):
        self.name = name
        self.nodelist = nodelist
    
    def render(self, context):
        content = self.nodelist.render(context)
        name = parse_tag_argument(self.name, context)
        proxy = SharedContentNode.shared_content.get(name, SharedContentProxy())
        proxy.content += content
        #SharedContentNode.shared_content[name].content += content
        return u''


@register.tag
def shared_append(parser, token):
    """
    Template tag to append content to a shared content block.
    Usage:
      {% load shared %}
      {% shared_append name="my_content" %}
          Some content you want to append to the shared block named 
          'my_content'. Can contain {{ MEDIA_URL }} variables or tags.
      {% endshared %}
    """
    default_arguments = {}
    default_arguments['name'] = '"default"'
    arguments = decode_tag_arguments(token, default_arguments)
    nodelist = parser.parse(('endshared_append',))
    parser.delete_first_token()
    return SharedAppendNode(nodelist, arguments['name'])
