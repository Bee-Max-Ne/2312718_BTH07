
import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


class TestMediumLevel(unittest.TestCase):
    """Kiem thu chuc nang ap dung ma khuyen mai (apply_promo_code)"""

    def test_apply_promo_code_valid_online(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000.0)

    def test_apply_promo_code_offline_raises_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_promo_code_invalid_code(self):
        app = YummyApp(network_status="online", os_version=15)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "SAIMAT")

    def test_apply_promo_code_os_version_too_low(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Kiem thu Mocking phan cung GPS cho get_nearby_restaurants"""

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_inside_area(self, mock_get_location):
        mock_get_location.return_value = (10.0, 105.0)
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_outside_area(self, mock_get_location):
        mock_get_location.return_value = (20.0, 110.0)
        app = YummyApp()
        self.assertEqual(app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_gps_lost(self, mock_get_location):
        mock_get_location.side_effect = gps_service.GPSSignalLostError(
            "Lost signal"
        )
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )


if __name__ == '__main__':
    unittest.main()
