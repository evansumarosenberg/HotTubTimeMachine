from unittest import TestCase
from unittest.mock import patch

import bestway.bestway_device as bestway_device
from bestway.bestway_device_airjet import BestwayDeviceAirjet, BestwayStatusAirjet
from bestway.bestway_device_airjet_v01 import BestwayDeviceAirjet_V01, BestwayStatusAirjet_V01


class FakeApi:
    def __init__(self):
        self.controls = []

    def send_controls(self, token, device_id, controls):
        self.controls.append((device_id, controls))


class TestBestwayDeviceAirjetControls(TestCase):
    def setUp(self):
        self.api = FakeApi()
        raw_device = {"product_name": bestway_device.AIRJET, "dev_alias": "Spa"}
        self.device = BestwayDeviceAirjet(self.api, "did-1", raw_device)

    def test_sends_switch_and_temp_controls(self):
        command = bestway_device.BestwayCommand()
        command.set_pump(False)
        command.set_heat(False)
        command.set_target_temp(99)
        command.set_bubbles(bestway_device.BUBBLES_HIGH)

        self.device.send_controls(None, command)

        self.assertEqual(
            self.api.controls,
            [
                (
                    "did-1",
                    {
                        "attrs": {
                            "filter_power": 0,
                            "heat_power": 0,
                            "temp_set": 99,
                            "wave_power": 1,
                        }
                    },
                )
            ],
        )

    def test_sends_schedule_controls(self):
        command = bestway_device.BestwayCommand()
        command.set_schedule(0, 30)

        self.device.send_controls(None, command)

        self.assertEqual(
            self.api.controls,
            [
                (
                    "did-1",
                    {
                        "attrs": {
                            "heat_appm_min": 0,
                            "heat_timer_min": 30,
                        }
                    },
                )
            ],
        )

    def test_decodes_binary_bubbles(self):
        status = BestwayStatusAirjet({"wave_power": 1})
        self.assertEqual(status.get_bubble_level(), bestway_device.BUBBLES_HIGH)

        status = BestwayStatusAirjet({"wave_power": 0})
        self.assertEqual(status.get_bubble_level(), bestway_device.BUBBLES_OFF)


class TestBestwayDeviceAirjetV01Controls(TestCase):
    def setUp(self):
        self.api = FakeApi()
        raw_device = {"product_name": bestway_device.AIRJET_V01, "dev_alias": "Spa"}
        self.device = BestwayDeviceAirjet_V01(self.api, "did-1", raw_device)

    def test_sends_switch_and_temp_controls(self):
        command = bestway_device.BestwayCommand()
        command.set_pump(False)
        command.set_heat(False)
        command.set_target_temp(99)

        self.device.send_controls(None, command)

        self.assertEqual(
            self.api.controls,
            [
                (
                    "did-1",
                    {
                        "attrs": {
                            "filter": 0,
                            "heat": 0,
                            "Tset": 99,
                        }
                    },
                )
            ],
        )

    def test_sends_airjet_massage_levels(self):
        for level, expected_value in [
            (bestway_device.BUBBLES_OFF, 0),
            (bestway_device.BUBBLES_LOW, 51),
            (bestway_device.BUBBLES_HIGH, 100),
        ]:
            with self.subTest(level=level):
                self.api.controls.clear()
                command = bestway_device.BestwayCommand()
                command.set_bubbles(level)

                self.device.send_controls(None, command)

                self.assertEqual(self.api.controls[0][1], {"attrs": {"wave": expected_value}})

    @patch("bestway.bestway_device_airjet_v01.time.sleep")
    def test_sends_schedule_controls_in_v01_order(self, sleep):
        command = bestway_device.BestwayCommand()
        command.set_schedule(0, 30)

        self.device.send_controls(None, command)

        self.assertEqual(
            self.api.controls,
            [
                ("did-1", {"attrs": {"word1": 30}}),
                ("did-1", {"attrs": {"word0": 0}}),
            ],
        )
        sleep.assert_called_once_with(3)

    def test_decodes_airjet_massage_levels(self):
        status = BestwayStatusAirjet_V01({"wave": 100})
        self.assertEqual(status.get_bubble_level(), bestway_device.BUBBLES_HIGH)

        status = BestwayStatusAirjet_V01({"wave": 51})
        self.assertEqual(status.get_bubble_level(), bestway_device.BUBBLES_LOW)

        status = BestwayStatusAirjet_V01({"wave": 0})
        self.assertEqual(status.get_bubble_level(), bestway_device.BUBBLES_OFF)
