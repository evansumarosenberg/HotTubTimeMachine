import json
import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

from bestway.bestway_user_token import BestwayUserToken
import tub_discover


class FakeBestwayAPI:
    devices = []

    def __init__(self, baseURL):
        self.baseURL = baseURL

    def check_login(self, token, username, password):
        return BestwayUserToken.from_values("uid", "tkn", 9999999999)

    def get_devices(self, token):
        return self.devices


class TestTubDiscover(TestCase):
    def test_selects_single_compatible_device(self):
        devices = [
            {"did": "light-1", "product_name": "Light", "dev_alias": "Light"},
            {"did": "tub-1", "product_name": "Airjet_V01", "dev_alias": "Spa"},
        ]

        selected = tub_discover.select_compatible_device(devices)

        self.assertEqual(selected["did"], "tub-1")

    def test_multiple_compatible_devices_require_did(self):
        devices = [
            {"did": "tub-1", "product_name": "Airjet_V01", "dev_alias": "Spa 1"},
            {"did": "tub-2", "product_name": "Airjet", "dev_alias": "Spa 2"},
        ]

        with self.assertRaises(SystemExit):
            tub_discover.select_compatible_device(devices)

    def test_explicit_did_selects_matching_compatible_device(self):
        devices = [
            {"did": "tub-1", "product_name": "Airjet_V01", "dev_alias": "Spa 1"},
            {"did": "tub-2", "product_name": "Airjet", "dev_alias": "Spa 2"},
        ]

        selected = tub_discover.select_compatible_device(devices, "tub-2")

        self.assertEqual(selected["did"], "tub-2")

    @patch("tub_discover.BestwayAPI", FakeBestwayAPI)
    def test_save_writes_discovered_device_id(self):
        FakeBestwayAPI.devices = [
            {
                "did": "tub-1",
                "product_name": "Airjet_V01",
                "dev_alias": "Spa",
                "is_online": True,
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            cfgfile = os.path.join(tmpdir, "configuration.json")
            with open(cfgfile, "w") as cfg:
                json.dump(
                    {
                        "username": "user",
                        "password": "pass",
                        "gizwits_url": "https://usapi.gizwits.com",
                        "did": "",
                        "token": {},
                    },
                    cfg,
                )

            tub_discover.main(["--cfgfile", cfgfile, "--save"])

            with open(cfgfile) as cfg:
                saved = json.load(cfg)

        self.assertEqual(saved["did"], "tub-1")
        self.assertEqual(saved["token"]["user_id"], "uid")
        self.assertEqual(saved["token"]["user_token"], "tkn")
