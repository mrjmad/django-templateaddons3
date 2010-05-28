from setuptools import setup, find_packages


setup(
    name='Django-TemplateAddOns',
    version='0.1dev',
    url='http://bitbucket.org/benoitbryon/django-templateaddons/',
    author='Benoit Bryon',
    author_email='benoit@marmelune.net',
    packages=find_packages(),
    license='BSD',
    description = "A set of tools for use with templates of the Django " \
                  "framework: additional template tags, context processors " \
                  "and utilities for template tag development.",
    long_description=open('README').read(),
    include_package_data = True,
)
