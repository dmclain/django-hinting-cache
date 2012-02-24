import hashlib
from django.template import Library, Node
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.http import urlquote

register = Library()


def get_cache_key(fragment_name, vary_on, context):
    args = hashlib.md5(u':'.join([urlquote(resolve_variable(var, context)) for var in vary_on]))
    return 'template.cache.%s.%s' % (fragment_name, args.hexdigest())


class CacheHintNode(Node):
    def __init__(self, fragment_name, vary_on):
        self.fragment_name = fragment_name
        self.vary_on = vary_on

    def render(self, context):
        cache.hint(get_cache_key(self.fragment_name, self.vary_on, context))
        return ''


@register.tag
def cache_hint(parser, token):
    tokens = token.contents.split()
    return CacheHintNode(tokens[1], tokens[2:])


class CacheHintMultiNode(Node):
    def __init__(self, fragment_names):
        self.fragment_names = fragment_names

    def render(self, context):
        for fragment_name in self.fragment_names:
            cache.hint(get_cache_key(fragment_name, [], context))
        return ''


@register.tag
def cache_hint_multi(parser, token):
    tokens = token.contents.split()
    return CacheHintMultiNode(tokens)
