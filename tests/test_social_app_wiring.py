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
        self.assertIn('rankLocallyWithTrace', feed)
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
        self.assertIn('switchAppViewProvider: switchAppView', (ROOT / 'src/state/session/index.tsx').read_text())
        self.assertIn('not a safe HTTPS origin', providers)
        self.assertIn("redirect: 'error'", clients)
        self.assertIn('AbortSignal.timeout(15_000)', clients)
        screen = (ROOT / 'src/screens/Settings/ServicesSettings.tsx').read_text()
        self.assertIn('Use Bluesky once', screen)
        self.assertIn('Use Bluesky and remember this choice', screen)
        self.assertIn('Cancel', screen)
        self.assertIn('appviewProviders: z.array(appviewProviderSchema).optional()', schema)
        self.assertIn('appviewSelections: z.record(z.string(), z.string()).optional()', schema)
        self.assertIn('appviewFallbacks', schema)
        self.assertIn('getAppViewFallback', providers)
        self.assertIn('project-appview', schema)
        self.assertIn('PersonalizationSettings', (ROOT / 'src/Navigation.tsx').read_text())
        personalization = (ROOT / 'src/lib/personalization.ts').read_text()
        self.assertIn('PERSONALIZATION_FORMAT', personalization)
        self.assertIn('encryptPersonalization', personalization)
        self.assertIn('resetLearnedState', personalization)
        local_feed = (ROOT / 'src/state/preferences/local-feed.tsx').read_text()
        self.assertIn('PERSONALIZATION_STORAGE_PREFIX', personalization)
        self.assertIn('accountDid', local_feed)
        self.assertIn('loadPersonalization', local_feed)
        self.assertNotIn('exportPersonalization', clients)
        self.assertIn("'appview-selection'", providers)
if __name__ == '__main__':
    unittest.main()
