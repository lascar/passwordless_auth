# https://stackoverflow.com/a/63761743
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set_breakpoint(context, *args):
    """
    Set breakpoints in the template for easy examination of the context,
    or any variables of your choice.

    Usage:
        {% load breakpoint %}
        {% set_breakpoint %}
              - or -
        {% set_breakpoint your_variable your_other_variable %}

    - The context is always accessible in the pdb console as a dict 'context'.

    - Additional variables can be accessed as vars[i] in the pdb console.
      - e.g. in the example above, your_variable will called vars[0] in the
             console, your_other_variable is vars[1]
    """

    vars = [arg for arg in locals()['args']]  # noqa F841
    breakpoint()
