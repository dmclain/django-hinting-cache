

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
    
    def _get_with_hints(self, keys):
        keys = list(self.hints.union(keys))
        if len(keys) == 1:
            tmp = self.get_cache.get(keys[0])
            if tmp is not None:
                result = {keys[0]: tmp}
            else:
                result = {}
        else:
            result = self.get_cache.get_many(keys)
        for k, v in result.items():
            if k in self.hints:
                self.fetched[k] = v
                print 'saving: %s' % k
        self.hints = set()
        return result
    
    def get(self, key, default=None, version=None):
        if key in self.fetched:
            print 'prefetched: %s' % key
            return self.fetched[key]
        return self._get_with_hints([key]).get(key, default)

    def get_many(self, keys, version=None):
        return self._get_with_hints(keys, version=version)
    
    def hint(self, *keys):
        self.hints = self.hints.union(keys)

    def __getattr__(self, name ):
        return getattr(self.get_cache, name)