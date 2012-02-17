
class HintingCache(object):
    def __init__(self, cache):
        self.cache = cache
        self._hints = set()
        self.fetched = {}
    
    def _get_with_hints(self, keys, *args, **kwargs):
        keys = list(self._hints.union(keys))
        if len(keys) == 1:
            tmp = self.cache.get(keys[0], *args, **kwargs)
            if tmp is not None:
                result = {keys[0]: tmp}
            else:
                result = {}
        else:
            result = self.cache.get_many(keys, *args, **kwargs)
        for k, v in result.items():
            if k in self._hints:
                self.fetched[k] = v
        self._hints = set()
        return result
    
    def get(self, key, *args, **kwargs):
        if key in self.fetched:
            return self.fetched[key]
        return self._get_with_hints([key], *args, **kwargs).get(key, None)

    def get_many(self, keys, *args, **kwargs):
        return self._get_with_hints(keys, *args, **kwargs)
    
    def hint(self, *keys):
        self._hints = self._hints.union(keys)

    def __getattr__(self, name ):
        return self.cache.__getattr__(name)