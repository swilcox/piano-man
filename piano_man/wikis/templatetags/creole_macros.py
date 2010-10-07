import pygments
import pygments.lexers
import pygments.formatters
import genshi.core
import creoleparser
import creoleparser.core


def highlight(text, lang=None):
    lexer = None
    if lang:
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
    if not lexer:
        lexer = pygments.lexers.guess_lexer(text)
    if lexer:
        text = pygments.highlight(text, lexer, pygments.formatters.HtmlFormatter())
    return genshi.core.Markup(text)

def pygments_macro(macro_name, arg_string, body, isblock, environ):
    if macro_name == 'mycode':
        args, kwargs = creoleparser.parse_args(arg_string)
        lang = kwargs.get('lang', None)
        return highlight(body, lang)
