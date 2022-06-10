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
        super(WebParser, self).__init__()
        self.script = Element(script)
        self.html = Element(html)
        self._name = "JavaScript"
        if args is None:
            args = {}
        self.args = args
