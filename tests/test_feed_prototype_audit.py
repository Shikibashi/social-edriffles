import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[1]
PROFILE = (ROOT / "upstream/social-app/src/lib/feed-sovereignty/profile.ts").read_text()
POST_FEED = (ROOT / "upstream/social-app/src/view/com/posts/PostFeed.tsx").read_text()


class FeedPrototypeAuditTests(unittest.TestCase):
    """Characterize known prototype gaps without redesigning the prototype."""

    def test_familiarity_is_declared_but_not_scored(self):
        self.assertIn("familiarity: number", PROFILE)
        self.assertNotIn("preferences.familiarity", PROFILE)

    def test_following_integration_uses_placeholder_signals(self):
        self.assertIn("networkRelevance: 0.5", POST_FEED)
        self.assertIn("integrityWeight: 1", POST_FEED)
        self.assertIn("seen: false", POST_FEED)

    def test_following_integration_has_no_topic_signal(self):
        mapping = POST_FEED[POST_FEED.index("page.slices"):POST_FEED.index("page.slices") + 2500]
        self.assertNotIn("topic:", mapping)

    def test_page_local_reranking_is_explicit(self):
        self.assertIn("data.pages.map(page =>", POST_FEED)
        self.assertIn("rerankLocally(", POST_FEED)

    def test_explanation_reconstructs_freshness(self):
        self.assertIn("freshness: 0.5", POST_FEED)
        self.assertIn("Math.exp(-Math.max(0, ageHours) / 24)", POST_FEED)

    def test_import_has_no_decrypt_function_or_strict_limits(self):
        self.assertIn("export function importPortableProfile", PROFILE)
        self.assertNotIn("decryptPortableProfile", PROFILE)
        self.assertNotIn("maxBytes", PROFILE)


if __name__ == "__main__":
    unittest.main()
