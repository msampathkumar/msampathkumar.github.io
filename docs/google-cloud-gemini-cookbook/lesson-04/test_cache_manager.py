import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the directory containing cache.py and config.py to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the entire google.genai module before importing cache
mock_genai = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = mock_genai
sys.modules['google.genai.types'] = MagicMock()

from cache import CacheManager
import config

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        # Reset the mock client for each test
        with patch('cache.genai.Client') as mock_client_class:
            self.mock_client = mock_client_class.return_value
            self.cache_manager = CacheManager()

    def test_list_caches_no_cleanup(self):
        # Setup mock caches
        mock_cache = MagicMock()
        mock_cache.display_name = config.CACHE_NAME
        mock_cache.name = "projects/123/locations/us-central1/cachedContents/456"
        mock_cache.model = "gemini-1.5-flash"
        mock_cache.update_time = "2023-01-01T00:00:00Z"
        mock_cache.expire_time = "2023-01-01T01:00:00Z"

        self.mock_client.caches.list.return_value = [mock_cache]

        # Call list_caches with cleanup=False
        self.cache_manager.list_caches(cleanup=False)

        # Verify delete was NOT called
        self.mock_client.caches.delete.assert_not_called()

    def test_list_caches_with_cleanup_matching_name(self):
        # Setup mock caches
        mock_cache = MagicMock()
        mock_cache.display_name = config.CACHE_NAME
        mock_cache.name = "projects/123/locations/us-central1/cachedContents/456"

        self.mock_client.caches.list.return_value = [mock_cache]

        # Call list_caches with cleanup=True
        self.cache_manager.list_caches(cleanup=True)

        # Verify delete WAS called with the correct name
        self.mock_client.caches.delete.assert_called_once_with(mock_cache.name)

    def test_list_caches_with_cleanup_non_matching_name(self):
        # Setup mock caches
        mock_cache = MagicMock()
        mock_cache.display_name = "OTHER-CACHE"
        mock_cache.name = "projects/123/locations/us-central1/cachedContents/789"

        self.mock_client.caches.list.return_value = [mock_cache]

        # Call list_caches with cleanup=True
        self.cache_manager.list_caches(cleanup=True)

        # Verify delete was NOT called because name doesn't match
        self.mock_client.caches.delete.assert_not_called()

if __name__ == '__main__':
    unittest.main()
