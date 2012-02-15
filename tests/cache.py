import unittest
import fudge
import random

from django_hinting_cache.cache import HintingCache
from fudge.inspector import arg

def matching(bound):
    def inner(inner_set):
        for obj in inner_set:
            if not obj in bound:
                return False
        return True
    return arg.passes_test(inner)

class HintingCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.inner_cache = fudge.Fake()
        self.cache = HintingCache(self.inner_cache)

    def test_no_hint_get(self):
        key = 'key:%i' % random.randint(100,300)
        value = 'val:%i' % random.randint(100,300)
        self.inner_cache.expects('get').with_args(key).returns(value)
        self.assertEqual(value, self.cache.get(key))

    def test_no_hint_get_many(self):
        num = random.randint(2, 7)
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num)]
        result = dict(zip(keys, values))
        self.inner_cache.expects('get_many').with_args(matching(keys)).returns(dict(zip(keys, values)))
        self.assertEqual(result, self.cache.get_many(keys))
        
    def test_single_hint_get(self):
        hint_key = 'hint_key:%i' % random.randint(100,300)
        key = 'key:%i' % random.randint(100,300)
        value = 'val:%i' % random.randint(100,300)
        result = {key: value}
        self.cache.hint(hint_key)
        self.inner_cache.expects('get_many').with_args(matching([hint_key, key])).returns(result)
        self.assertEqual(result, self.cache.get(key))
        
    def test_single_hint_get_many(self):
        num = random.randint(2, 7)
        hint_key = 'hint_key:%i' % random.randint(100,300)
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num)]
        self.cache.hint(hint_key)
        value = dict(zip(keys, values))
        self.inner_cache.expects('get_many').with_args(matching([hint_key] + keys)).returns(value)
        self.assertEqual(value, self.cache.get_many(keys))
        
    def test_single_hint_get_with_same_key(self):
        hint_key = 'hint_key:%i' % random.randint(100,300)
        key = hint_key
        value = 'val:%i' % random.randint(100,300)
        self.cache.hint(hint_key)
        self.inner_cache.expects('get').with_args(key).returns(value)
        self.assertEqual(value, self.cache.get(key))
        
    def test_multi_hint_get(self):
        num = random.randint(2, 6)
        hint_keys = ['hint_key:%i' % random.randint(100,300) for i in range(num)]
        key = 'key:%i' % random.randint(100,300)
        value = 'val:%i' % random.randint(100,300)
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(hint_keys + [key]).returns(value)
        self.assertEqual(value, self.cache.get(key))
        
    def test_multi_hint_get_many(self):
        num = random.randint(2, 6)
        hint_keys = ['hint_key:%i' % random.randint(100,300) for i in range(num)]
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        value = 'val:%i' % random.randint(100,300)
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(hint_keys + keys).returns(value)
        self.assertEqual(value, self.cache.get_many(keys))
        
    def test_multi_hint_get_with_same_key(self):
        num = random.randint(2, 6)
        hint_keys = ['hint_key:%i' % random.randint(100,300) for i in range(num)]
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        keys = keys + [hint_keys[0]]
        value = 'val:%i' % random.randint(100,300)
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(hint_keys + keys).returns(value)
        self.assertEqual(value, self.cache.get_many(keys))
        
    def test_multi_hint_get_many_with_overlap(self):
        pass
        
    def test_hint_get_get_with_matching_key(self):
        pass
        

if __name__ == '__main__':
    unittest.main()