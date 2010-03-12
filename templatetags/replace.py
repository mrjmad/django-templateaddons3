from django import template

from templateaddons.utils import decode_tag_arguments, parse_tag_argument


register = template.Library()


class ReplaceNode(template.Node):
    def __init__(self, source, search=u'', replacement=u''):
        self.nodelist = source
        self.search = search
        self.replacement = replacement
    
    def render(self, context):
        search = parse_tag_argument(self.search, context)
        replacement = parse_tag_argument(self.replacement, context)
        
        source = self.nodelist.render(context)
        output = source.replace(search, replacement)
        
        return output


def replace_tag(parser, token):
    default_arguments = {}
    default_arguments['search'] = u''
    default_arguments['replacement'] = u''
    arguments = decode_tag_arguments(token, default_arguments)
    
    source = parser.parse(('endreplace',))
    parser.delete_first_token()
    
    return ReplaceNode(source, **arguments)

register.tag('replace', replace_tag)
