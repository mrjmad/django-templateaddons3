#!/usr/bin/env python
# coding= utf-8
import re
from django import template


def parse_tag_argument(argument, context):
    """Parses a template tag argument within given context.
    
    Consider the tag:
    {% my_tag name='Toto' surname="Tata" age=32 size=1.70 person=object.get_person %}
    
    The values used above are interpreted as:
    - 'Toto' and "Tata" are converted to their string value (without quotes),
    respectively 'Toto' and 'Tata'
    - 32 is converted to an integer
    - 1.70 is converted to a float
    - object.get_person is interpreted as a variable and parsed within the context
    """
    if isinstance(argument, (str, unicode)) and argument:
        if argument[0] == argument[-1] and argument[0] in ('"', "'"):
            argument = argument[1:-1]
        else:
            m = re.match(r'(?P<int>\d+)(\.(?P<decimal>\d+))?', argument)
            if m is not None:
                if m.group('decimal'):
                    argument = float(argument)
                else:
                    argument = int(argument)
            else:
                argument = template.Variable(argument).resolve(context)
    return argument


def decode_tag_argument(argument):
    """Extracts argument name and value from the given string"""
    match = re.match(r'((?P<name>[\w-]+)=)?(?P<value>.+)', argument)
    if match is None:
        raise template.TemplateSyntaxError, "invalid tag argument syntax '%s'" % argument
    else:
        return {'name': match.group('name'), 'value':match.group('value')} 


def decode_tag_arguments(token, default_arguments={}):
    """Returns a dictionnary of arguments that can be found in the given token.
    
    This can be useful to code template tags like this:
    {% my_tag name='Toto' surname="Tata" age=32 size=1.70 person=object.get_person %}
    In this syntax, arguments order is not important.
    
    You can provide default argument values with the parameter default_arguments.
    """
    arguments = {}
    args = token.split_contents()   # TODO: fix bug that occurs when an argument value contains whitespaces. Example: my_arg=" "
    args.reverse()
    
    for (arg_name, arg_value) in default_arguments.iteritems():
        arguments[arg_name] = arg_value
    
    for arg in args:
        argument = decode_tag_argument(arg)
        arguments[argument['name']] = argument['value']
    
    return arguments
