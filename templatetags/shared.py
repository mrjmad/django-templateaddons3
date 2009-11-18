#!/usr/bin/env python
# coding= utf-8
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument
from django.utils.encoding import force_unicode


register = template.Library()


class SharedContentProxy(object):
    """
    Content storage.
    """
    def __init__(self, content=u'', nodes=[], separator=u'', unique=False):
        self.nodes = nodes
        self.separator = separator
        self.unique = unique
        if content:
            self.append(content)
        self.content = content
    
    def __unicode__(self):
        return self.content
        if self.unique:
            pass #self.remove_duplicates()
        return u'%s' % self.separator.join(self.nodes)
    
    def remove_duplicates(self):
        seen = set()
        self.nodes = [x for x in self.nodes if x not in seen and not seen.add(x)]
    
    def append(self, content):
        self.content += content
        self.nodes.append(content)


shared_content = {}


class SharedRenderNode(template.Node):
    """
    Make it possible to declare content blocks which output can still be 
    updated after declaration.
    """
    def __init__(self, name, separator=u'', unique=False):
        self.name = name
        self.separator = separator
        self.unique = unique
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        separator = parse_tag_argument(self.separator, context)
        unique = parse_tag_argument(self.unique, context)
        if name not in shared_content:
            shared_content[name] = SharedContentProxy(unique=unique, separator=separator)
        else:
            shared_content[name].separator = separator
            shared_content[name].unique = unique
        return shared_content[name]


@register.tag
def shared_render(parser, token):
    """
    Template tag to display a "shared content".
    "Shared content" is content that can be populated via multiple calls to the 
    "shared_assign" template tag.
    Usage:
      {% load shared %}
      {% shared_render name="my_content" %}
    
    Usage of optional parameters:
      {% shared_render name="my_content" separator="<br />" unique=1 %}
    """
    default_arguments = {}
    default_arguments['name'] = u'"default"'
    default_arguments['separator'] = u'""'
    default_arguments['unique'] = u'0'
    arguments = decode_tag_arguments(token, default_arguments)
    return SharedRenderNode(arguments['name'], arguments['separator'], arguments['unique'])


class SharedAssignNode(template.Node):
    """
    Make it possible to update content of a shared block.
    """
    def __init__(self, nodelist, name):
        self.name = name
        self.nodelist = nodelist
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        content = self.nodelist.render(context)
        #if not context.has_key(name):
        #    context[name] = u''
        #context[name] += content
        if name not in shared_content:
            shared_content[name] = SharedContentProxy()
        shared_content[name].append(content)
        return u''


@register.tag
def shared_assign(parser, token):
    """
    Template tag to append content to a shared content block.
    Usage:
      {% load shared %}
      {% shared_assign name="my_content" %}
          Some content you want to append to the shared block named 
          'my_content'. Can contain {{ MEDIA_URL }} variables or tags.
      {% endshared_assign %}
    """
    default_arguments = {}
    default_arguments['name'] = '"default"'
    arguments = decode_tag_arguments(token, default_arguments)
    nodelist = parser.parse(('endshared_assign',))
    parser.delete_first_token()
    return SharedAssignNode(nodelist, arguments['name'])


class SharedDeclareNode(template.Node):
    """
    Make it possible to update content of a shared block.
    """
    def __init__(self, name):
        self.name = name
    
    def render(self, context):
        name = parse_tag_argument(self.name, context)
        if not context.has_key(name):
            context[name] = u''
        return u''


@register.tag
def shared_declare(parser, token):
    """
    Template tag to append content to a shared content block.
    Usage:
      {% load shared %}
      {% shared_assign name="my_content" %}
          Some content you want to append to the shared block named 
          'my_content'. Can contain {{ MEDIA_URL }} variables or tags.
      {% endshared_assign %}
    """
    default_arguments = {}
    default_arguments['name'] = '"default"'
    arguments = decode_tag_arguments(token, default_arguments)
    return SharedDeclareNode(arguments['name'])
