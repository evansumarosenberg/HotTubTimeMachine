from unittest import TestCase

import bestway.bestway_device as bestway_device


class TestBestwayCommand(TestCase):
    def test_stores_target_temp(self):
        command = bestway_device.BestwayCommand()

        command.set_target_temp(99)

        self.assertEqual(command.get_target_temp(), 99)

    def test_stores_explicit_false_values(self):
        command = bestway_device.BestwayCommand()

        command.set_pump(False)
        command.set_heat(False)
        command.set_bubbles(False)

        self.assertFalse(command.get_pump())
        self.assertFalse(command.get_heat())
        self.assertEqual(command.get_bubbles(), bestway_device.BUBBLES_OFF)

    def test_normalizes_boolean_bubbles(self):
        command = bestway_device.BestwayCommand()

        command.set_bubbles(True)
        self.assertEqual(command.get_bubbles(), bestway_device.BUBBLES_HIGH)

        command.set_bubbles(False)
        self.assertEqual(command.get_bubbles(), bestway_device.BUBBLES_OFF)
