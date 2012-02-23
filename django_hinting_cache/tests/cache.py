from django.test import TestCase
import fudge
import random

from django_hinting_cache.cache import HintingCache
from fudge.inspector import arg
from django.core.cache import get_cache


def matching(bound):
    def inner(inner_set):
        return set(inner_set) == set(bound)
    return arg.passes_test(inner)


class HintingCacheTestCase(TestCase):
    def setUp(self):
        self.inner_cache = fudge.Fake()
        self.cache = HintingCache('location', {})
        self.cache.cache = self.inner_cache

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
        self.assertEqual(value, self.cache.get(key))
        
    def test_single_hint_get_many(self):
        num = random.randint(2, 7)
        hint_key = 'hint_key:%i' % random.randint(100,300)
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num)]
        self.cache.hint(hint_key)
        value = dict(zip(keys, values))
        self.inner_cache.expects('get_many').with_args(matching([hint_key] + keys)).returns(value)
        self.assertEqual(value, self.cache.get_many(keys))
        
    def test_single_hint_get_miss(self):
        hint_key = 'hint_key:%i' % random.randint(100,300)
        key = 'key:%i' % random.randint(100,300)
        self.cache.hint(hint_key)
        self.inner_cache.expects('get_many').with_args(matching([hint_key, key])).returns({})
        self.assertEqual(None, self.cache.get(key))
        
    def test_single_hint_get_many_miss(self):
        num = random.randint(2, 7)
        hint_key = 'hint_key:%i' % random.randint(100,300)
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num)]
        self.cache.hint(hint_key)
        value = dict(zip(keys, values))
        self.inner_cache.expects('get_many').with_args(matching([hint_key] + keys)).returns({})
        self.assertEqual({}, self.cache.get_many(keys))
        
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
        values = ['val:%i' % random.randint(100,300) for i in range(num + 1)]
        result = dict(zip(hint_keys + [key], values))
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(matching(hint_keys + [key])).returns(result)
        self.assertEqual(result[key], self.cache.get(key))
        
    def test_multi_hint_get_many(self):
        num = random.randint(2, 6)
        hint_keys = ['hint_key:%i' % random.randint(100,300) for i in range(num)]
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num * 2)]
        result = dict(zip(hint_keys + keys, values))
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(matching(hint_keys + keys)).returns(result)
        self.assertEqual(result, self.cache.get_many(keys))
        
    def test_multi_hint_get_with_same_key(self):
        num = random.randint(2, 6)
        hint_keys = ['hint_key:%i' % random.randint(100,300) for i in range(num)]
        keys = ['key:%i' % random.randint(100,300) for i in range(num)]
        values = ['val:%i' % random.randint(100,300) for i in range(num * 2)]
        result = dict(zip(hint_keys + keys, values))
        keys = keys + [hint_keys[0]]
        self.cache.hint(*hint_keys)
        self.inner_cache.expects('get_many').with_args(matching(hint_keys + keys)).returns(result)
        self.assertEqual(result, self.cache.get_many(keys))
        
    #def test_multi_hint_get_many_with_overlap(self):
        #pass
        
    #def test_hint_get_get_with_matching_key(self):
        #pass

    def test_proxying_set(self):
        self.inner_cache.expects('set').returns_fake(callable=True)
        self.cache.set()

    def test_proxying_set_many(self):
        self.inner_cache.expects('set_many').returns_fake(callable=True)
        self.cache.set_many()

    def test_proxying_delete(self):
        self.inner_cache.expects('delete').returns_fake(callable=True)
        self.cache.delete()

    def test_proxying_delete_many(self):
        self.inner_cache.expects('delete_many').returns_fake(callable=True)
        self.cache.delete_many()

    def test_proxying_has_key(self):
        self.inner_cache.expects('has_key').returns_fake(callable=True)
        self.cache.has_key()


class HintingCacheInstantiationTestCase(TestCase):
    def testInstantiation(self):
        hinting = get_cache('default')
        inner = get_cache('real')
        hinting.set('key', 'value', 60)
        self.assertEqual(hinting.get('key'), 'value')
        self.assertEqual(inner.get('key'), 'value')
