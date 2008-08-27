#!/usr/bin/env python
# coding= utf-8
from django import template
from templateutils.utils import decode_tag_arguments, parse_tag_argument

from django.newforms.forms import BoundField
from django.newforms.util import ErrorList
from django.utils.html import escape


register = template.Library()


class RenderFormNode(template.Node):
    def __init__(self, form, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        self.form, self.normal_row, self.error_row, self.row_ender, self.help_text_html, self.errors_on_separate_row = form, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row
    
    def render(self, context):
        form = parse_tag_argument(self.form, context)
        normal_row = parse_tag_argument(self.normal_row, context)
        error_row = parse_tag_argument(self.error_row, context)
        row_ender = parse_tag_argument(self.row_ender, context)
        help_text_html = parse_tag_argument(self.help_text_html, context)
        errors_on_separate_row = parse_tag_argument(self.errors_on_separate_row, context)
        #return form._html_output(normal_row, error_row, row_ender, help_text_html, errors_on_separate_row)
        top_errors = form.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        for name, field in form.fields.items():
            bf = BoundField(form, field, name)
            bf_errors = [escape(error).encode('utf8') for error in bf.errors] # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(['(Hidden field %s) %s' % (name, e) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % tuple(bf_errors))
                #label = bf.label and bf.label_tag(escape(bf.label + ':')) or ''
                label = bf.label and bf.label_tag(escape(bf.label)) or ''
                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = u''
                #output.append(normal_row % {'errors': bf_errors, 'label': label, 'field': unicode(bf), 'help_text': help_text})
                bf_errors_output = '%s' % ''.join(['<span class="error">%s</span>' % e for e in bf_errors])
                output.append(normal_row % {'errors': bf_errors_output, 'label': label.encode('utf8'), 'field': unicode(bf).encode('utf8'), 'help_text': help_text.encode('utf8')})
        if top_errors:
            output.insert(0, error_row % top_errors)
        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and insert the hidden fields.
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else: # If there aren't any rows in the output, just append the hidden fields.
                output.append(str_hidden)
        return '\n'.join(output)


@register.tag
def render_form(parser, token):
    default_arguments = {}
    default_arguments['form'] = None
    #default_arguments['normal_row'] = '"<strong>%(errors)s</strong><p>%(label)s %(field)s%(help_text)s</p>"'
    default_arguments['normal_row'] = '"<li>%(errors)s%(label)s %(field)s%(help_text)s</li>"'
    default_arguments['error_row'] = '"<li>%s</li>"'
    default_arguments['row_ender'] = '"</li>"'
    default_arguments['help_text_html'] = "'<span class=\"help\">%s</span>'"
    default_arguments['errors_on_separate_row'] = False
    arguments = decode_tag_arguments(token, default_arguments)
    
    return RenderFormNode(
        arguments['form'],
        arguments['normal_row'],
        arguments['error_row'],
        arguments['row_ender'],
        arguments['help_text_html'],
        arguments['errors_on_separate_row'],
        )
