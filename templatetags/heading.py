import re

from django import template
from templateaddons.utils import decode_tag_arguments


register = template.Library()


class HeadingContextNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        current_level = int(context.get('heading_current_level', 1))
        output = self.nodelist.render(context)
        for heading_level in reversed(range(1, 5)):
            output = re.sub(r'\<h%d([\s>])' % heading_level, r'<h%d\1' % (heading_level + current_level), output)
            output = re.sub(r'</h%d([\s>])' % heading_level, r'</h%d\1' % (heading_level + current_level), output)
        return output


@register.tag
def headingcontext(parser, token):
    default_arguments = {}
    arguments = decode_tag_arguments(token, default_arguments)
    
    nodelist = parser.parse(('endheadingcontext',))
    parser.delete_first_token()
    return HeadingContextNode(nodelist, **arguments)
