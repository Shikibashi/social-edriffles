import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'upstream' / 'social-app'

class SocialAppWiringTests(unittest.TestCase):
    def test_following_settings_expose_local_toggle(self):
        source = (ROOT / 'src/screens/Settings/FollowingFeedPreferences.tsx').read_text()
        self.assertIn('Use local feed reranking', source)
        self.assertIn('setLocalFeedEnabled', source)

    def test_feed_pipeline_passes_local_preferences_and_explanations(self):
        page = (ROOT / 'src/view/com/feeds/FeedPage.tsx').read_text()
        feed = (ROOT / 'src/view/com/posts/PostFeed.tsx').read_text()
        item = (ROOT / 'src/view/com/posts/PostFeedItem.tsx').read_text()
        self.assertIn('localFeedPreferences', page)
        self.assertIn('rerankLocally', feed)
        self.assertIn('Why this post?', item)

    def test_appview_provider_selection_is_persisted_and_explicit(self):
        schema = (ROOT / 'src/state/persisted/schema.ts').read_text()
        providers = (ROOT / 'src/state/session/providers.ts').read_text()
        core = (ROOT / 'src/state/session/session-core.ts').read_text()
        clients = (ROOT / 'src/state/session/clients.ts').read_text()
        self.assertIn('appviewProviders', schema)
        self.assertIn('appviewSelections', schema)
        self.assertIn('selectAppViewProvider', providers)
        self.assertIn('registerAppViewProvider', providers)
        self.assertIn('switchAppViewProvider', core)
        self.assertIn('provider.endpoint', clients)
        self.assertIn('provider.serviceDid', clients)
if __name__ == '__main__':
    unittest.main()
