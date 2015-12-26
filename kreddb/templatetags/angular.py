import json

from django import template

register = template.Library()


@register.inclusion_tag('kreddb/angular_app.html', takes_context=True)
def angular_app(context, app):
    return {
        'app_context': json.dumps(context[app]),
        'app': app,
    }
