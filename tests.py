from django.template import Template, Context
from django.test import TestCase


class TemplateTagTestCase(TestCase):
    """
    Base class to test template tags.
    """
    def validate_template_code_result(self, fixtures):
        """
        Validates that the template code in given fixtures match the 
        corresponding expected output.
        
        The given 'fixtures' argument is an iterable of 2-items lists matching 
        the following scheme::
          
          (
            (template_code_1, expected_output_1),
            (template_code_2, expected_output_2),
            ...
          )
        """
        for (template_code, valid_output) in fixtures:
            t = Template(template_code)
            c = Context()
            output = t.render(c)
            self.assertEquals(output, valid_output)


class AssignTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% assign %} template tag"""
    def test_output(self):
        # set up fixtures
        fixtures = [
            (u'{% assign %}1234{% endassign %}', u''), # silent capture
            (u'{% assign %}1234{% endassign %}5678{{ assign }}', u'56781234'), # default name is "assign"
            (u'{% assign name="sample" %}1234{% endassign %}5678{{ sample }}', u'56781234'), # "name" parameter
            (u'{% assign name="sample" %}1234{% endassign %}{% assign name="sample" %}5678{% endassign %}{{ sample }}', u'5678'), # context override
            (u'{% assign silent=1 %}1234{% endassign %}', u''), # silent capture
            (u'{% assign silent=0 %}1234{% endassign %}', u'1234'), # non silent capture
            ]
        # add template tag library to template code
        fixtures = [(u'{% load assign %}' + template_code, valid_output) for (template_code, valid_output) in fixtures]            
        # test real output
        self.validate_template_code_result(fixtures)


class CounterTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% counter %} template tag"""
    def test_output(self):
        # set up fixtures
        fixtures = [
            (u'{% counter %}', u'0'), # default call
            (u'{% counter %}{% counter %}', u'01'), # default call, 2 calls
            (u'{% counter %}{% counter %}{% counter %}', u'012'), # default call, 3 calls
            (u'{% counter %}{% counter name="c2" %}{% counter %}{% counter %}', u'0012'), # name parameter
            (u'{% counter name="c2" %}{% counter %}{% counter name="c2" %}{% counter name="c2" %}', u'0012'), # name parameter
            (u'{% counter name="c1" %}{% counter name="c2" %}{% counter name="c1" %}{% counter name="c1" %}{% counter name="c2" %}', u'00121'), # name parameter
            (u'{% counter %}{% counter name="default" %}', u'01'), # default name is "default"
            (u'{% counter start=1 %}{% counter %}', u'12'), # start parameter
            (u'{% counter step=4 %}{% counter %}{% counter %}', u'048'), # step parameter
            (u'{% counter step=-4 %}{% counter %}{% counter %}', u'0-4-8'), # negative step parameter
            (u'{% counter ascending=1 %}{% counter %}{% counter %}', u'012'), # ascending parameter
            (u'{% counter ascending=0 %}{% counter %}{% counter %}', u'0-1-2'), # ascending parameter
            (u'{% counter ascending=0 step=-1 %}{% counter %}{% counter %}', u'012'), # ascending parameter and negative step
            (u'{% counter silent=1 %}{% counter %}{% counter %}', u'12'), # silent parameter
            (u'{% counter %}{% counter silent=1 %}{% counter %}', u'02'), # silent parameter
            (u'{% counter silent=1 %}{% counter silent=1 %}{% counter %}', u'2'), # silent parameter
            (u'{% counter assign="c1" %}{{ c1 }}{% counter %}{% counter assign="c1" %}{{ c1 }}{% counter %}{% counter assign="c2" %}{% counter %}{{ c1 }}{{ c2 }}', u'0012234524'), # assign parameter
            (u'{% counter start=4 step=4 ascending=0 %}{% counter start=8 step=23 ascending=1 %}{% counter %}', u'40-4'), # only first declaration affects step and ascending parameters
            ]
        # add template tag library to template code
        fixtures = [(u'{% load counter %}' + template_code, valid_output) for (template_code, valid_output) in fixtures]            
        # test real output
        self.validate_template_code_result(fixtures)


class HeadingContextTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% headingcontext %} template tag"""
    def test_output(self):
        # set up fixtures
        fixtures = [
            (u'{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', u'<h2>Test</h2>'),
            (u'{% headingcontext %}<H1>Test</H1>{% endheadingcontext %}', u'<h2>Test</h2>'),
            (u'{% headingcontext %}<h1 class="test">Test</h1>{% endheadingcontext %}', u'<h2 class="test">Test</h2>'),
            (u'{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', u'<h2>Test</h2>'),
            (u'{% headingcontext %}<h2>Test</h2>{% endheadingcontext %}', u'<h3>Test</h3>'),
            (u'{% headingcontext source_level=2 %}<h2>Test</h2>{% endheadingcontext %}', u'<h2>Test</h2>'),
            (u'{% headingcontext source_level=5 %}<h5>Test</h5>{% endheadingcontext %}', u'<h2>Test</h2>'),
            (u'{% headingcontext source_level=2 target_level=4 %}<h2>Test</h2>{% endheadingcontext %}', u'<h4>Test</h4>'),
            (u'{% headingcontext source_level=5 target_level=4 %}<h5>Test</h5>{% endheadingcontext %}', u'<h4>Test</h4>'),
            ]
        # add template tag library to template code
        fixtures = [(u'{% load heading %}' + template_code, valid_output) for (template_code, valid_output) in fixtures]            
        # test real output
        self.validate_template_code_result(fixtures)
