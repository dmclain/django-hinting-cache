
class HintingCache(object):
	def __init__(self, cache)
		self.cache = cache
	
	def get(self, key, *args, **kwargs):
		return self.get(key, *args, **kwargs)	

	def get_many(self, key, *args, **kwargs):
		return self.get_many(key, *args, **kwargs)
	
	def __getattribute__(self, name):
		return self.cache.__get_attribute__(name)