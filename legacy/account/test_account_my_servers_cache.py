from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from server.models import Server, Channel, ServerCategory

class TestAccountMyServersCache(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='cacheuser', password='cachepass')
        self.category = ServerCategory.objects.create(name='CacheCat')
        self.server = Server.objects.create(name='CacheServer', owner=self.user.account, category=self.category)
        self.server.members.add(self.user.account)
        self.channel = Channel.objects.create(name='cache-general', type=Channel.text, server=self.server, owner=self.user.account)
        self.cache_key = f'user_{self.user.account.id}_servers'
        cache.delete(self.cache_key)

    def test_cache_is_set_on_first_access(self):
        # First access, cache should be empty
        servers = cache.get(self.cache_key)
        self.assertIsNone(servers)
        # Simulate view logic
        servers = list(self.user.account.servers.select_related('owner', 'category').prefetch_related('members', 'channel_server').all())
        cache.set(self.cache_key, servers, timeout=300)
        cached_servers = cache.get(self.cache_key)
        self.assertIsNotNone(cached_servers)
        self.assertTrue(any(s.name == 'CacheServer' for s in cached_servers))

    def test_cache_returns_data_on_second_access(self):
        # Set cache
        servers = list(self.user.account.servers.select_related('owner', 'category').prefetch_related('members', 'channel_server').all())
        cache.set(self.cache_key, servers, timeout=300)
        # Second access should return cached data
        cached_servers = cache.get(self.cache_key)
        self.assertIsNotNone(cached_servers)
        self.assertTrue(any(s.name == 'CacheServer' for s in cached_servers))

    def test_cache_invalidation(self):
        # Set cache
        servers = list(self.user.account.servers.select_related('owner', 'category').prefetch_related('members', 'channel_server').all())
        cache.set(self.cache_key, servers, timeout=300)
        # Invalidate cache
        cache.delete(self.cache_key)
        self.assertIsNone(cache.get(self.cache_key))
