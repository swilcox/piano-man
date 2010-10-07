"""
"markup" template filter for Django. This filter transforms plain text markup
syntaxes to HTML; an additional argument is used to determine which markup
language/engine to use.
"""

from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

def markup(value, arg=''):
    if arg == 'rst':
        from docutils.core import publish_parts
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=smart_str(value), writer_name="html4css1", settings_overrides=docutils_settings)
        return mark_safe(force_unicode(parts["html_body"]))
    elif arg == 'markdown':
        import markdown
        extensions = ['codehilite']
        safe_mode = True
        return mark_safe(markdown.markdown(force_unicode(value), extensions, safe_mode=safe_mode))
    elif arg == 'textile':
        import textile
        return mark_safe(force_unicode(textile.textile(smart_str(value), encoding='utf-8', output='utf-8')))
    elif arg == 'creole':
        import creoleparser
        from creole_macros import pygments_macro
        dialect = creoleparser.create_dialect(creoleparser.dialects.creole11_base, macro_func=pygments_macro)
        parser = creoleparser.Parser(dialect=dialect)
        return mark_safe(parser(value))
    elif arg == 'html':
        return mark_safe(value)
    elif arg == 'txt':
        return mark_safe('<pre>%s</pre>' % value)
    else:
        return value
markup.is_safe = True


register.filter(markup)