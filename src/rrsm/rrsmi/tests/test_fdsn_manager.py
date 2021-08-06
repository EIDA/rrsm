from django.test import TestCase
from rrsmi.fdsn.base_classes import MotionDataStationChannel
from rrsmi.fdsn import fdsn_manager


class FdsnManagerTests(TestCase):
    def setUp(self):
        self.motion_manager = fdsn_manager.FdsnMotionManager()

    def test_components_invalid(self):
        X = MotionDataStationChannel()
        Y = MotionDataStationChannel()
        Z = MotionDataStationChannel()
        result = None

        X.pga_value = 9.9
        Y.pga_value = 1
        Z.pga_value = 1
        components = {
            "X": X,
            "Y": Y,
            "Z": Z,
        }
        result = self.motion_manager._components_invalid(components)
        self.assertFalse(result)

        X.pga_value = 10
        Y.pga_value = 1
        Z.pga_value = 1
        components = {
            "X": X,
            "Y": Y,
            "Z": Z,
        }
        result = self.motion_manager._components_invalid(components)
        self.assertTrue(result)
