

class HintingCache(object):
    def __init__(self, location, params):
        self.cache = None
        self.location = location
        self.hints = set()
        self.fetched = {}

    @property
    def get_cache(self):
        if not self.cache:
            from django.core.cache import get_cache
            self.cache = get_cache(self.location)
        return self.cache
    
    def _get_with_hints(self, keys, *args, **kwargs):
        keys = list(self.hints.union(keys))
        if len(keys) == 1:
            tmp = self.get_cache.get(keys[0], *args, **kwargs)
            if tmp is not None:
                result = {keys[0]: tmp}
            else:
                result = {}
        else:
            result = self.get_cache.get_many(keys, *args, **kwargs)
        for k, v in result.items():
            if k in self.hints:
                self.fetched[k] = v
        self.hints = set()
        return result
    
    def get(self, key, *args, **kwargs):
        if key in self.fetched:
            return self.fetched[key]
        return self._get_with_hints([key], *args, **kwargs).get(key, None)

    def get_many(self, keys, *args, **kwargs):
        return self._get_with_hints(keys, *args, **kwargs)
    
    def hint(self, *keys):
        self.hints = self.hints.union(keys)

    def __getattr__(self, name ):
        return self.get_cache.__getattr__(name)