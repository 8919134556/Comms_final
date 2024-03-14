import unittest
from src.wifi_network import WifiNetwork

class TestWifiNetwork(unittest.TestCase):

    def setUp(self):
        self.wifi_network_processor = WifiNetwork()

    def test_valid_input(self):
        context = "000000000000000000000000000000" 
        expected_result = [0, 0, 0, 0, 0]
        result = self.wifi_network_processor.hex_bit_wifi_network(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.wifi_network_processor.hex_bit_wifi_network(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.wifi_network_processor.hex_bit_wifi_network(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "1"
        result = self.wifi_network_processor.hex_bit_wifi_network(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 12345
        result = self.wifi_network_processor.hex_bit_wifi_network(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
