# Third party imports
from branca.element import Template, MacroElement, Element


class WebParser(MacroElement):
    """
    Parse JS or HTML
    """
    _template = Template(
        u"""{% macro html(this, args) %}
            {{this.html.render(**this.args)}}
            {% endmacro %}
            {% macro script(this, args) %}
            {{this.script.render(**this.args)}}
            {% endmacro %}"""
    )

    def __init__(self, script=None, html=None, args=None):
        """
        Parse HTML of JS with args
        :param script: JS script
        :param html: HTML
        :param args: Some arguments for parse
        """
        super(WebParser, self).__init__()
        self.script = Element(script)
        self.html = Element(html)
        self._name = "JavaScript"
        if args is None:
            args = {}
        self.args = args
