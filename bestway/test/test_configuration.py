from unittest import TestCase

from configuration import DEFAULT_CONFIG, Configuration


class TestConfiguration(TestCase):
    def test_default_config_has_bootstrap_values(self):
        cfg = Configuration(DEFAULT_CONFIG)

        self.assertEqual(cfg.username, "unset")
        self.assertEqual(cfg.password, "NONE")
        self.assertEqual(cfg.gizwits_url, "https://usapi.gizwits.com")
        self.assertEqual(cfg.did, "")
        self.assertEqual(cfg.token["user_id"], "")
        self.assertEqual(cfg.token["user_token"], "")
        self.assertEqual(cfg.token["expiry"], 0)
