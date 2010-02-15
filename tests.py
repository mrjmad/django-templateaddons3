from django.template import Template
from django.test import TestCase


class HeadingContextTemplateTagTestCase(TestCase):
    """Tests the {% headingcontext %} template tag"""
    def test_output(self):
        # set up fixtures
        fixtures = [
            ('{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', '<h2>Test</h2>'),
            ('{% headingcontext %}<H1>Test</H1>{% endheadingcontext %}', '<h2>Test</h2>'),
            ('{% headingcontext %}<h1 class="test">Test</h1>{% endheadingcontext %}', '<h2 class="test">Test</h2>'),
            ('{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', '<h2>Test</h2>'),
            ('{% headingcontext %}<h2>Test</h2>{% endheadingcontext %}', '<h3>Test</h3>'),
            ('{% headingcontext source_level=2 %}<h2>Test</h2>{% endheadingcontext %}', '<h2>Test</h2>'),
            ('{% headingcontext source_level=5 %}<h5>Test</h5>{% endheadingcontext %}', '<h2>Test</h2>'),
            ('{% headingcontext source_level=2 target_level=4 %}<h2>Test</h2>{% endheadingcontext %}', '<h4>Test</h4>'),
            ('{% headingcontext source_level=5 target_level=4 %}<h5>Test</h5>{% endheadingcontext %}', '<h4>Test</h4>'),
            ]
        # add template tag library to template code
        fixtures = [('{% load heading %}' + template_code, valid_output) for (template_code, valid_output) in fixtures]            
        # test real output
        for (template_code, valid_output) in fixtures:
            t = Template(template_code)
            output = t.render({})
            self.assertEquals(output, valid_output)
