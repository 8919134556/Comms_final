import unittest
from src.gps.mobile_network import MobileNetwork

class TestMobileNetwork(unittest.TestCase):

    def setUp(self):
        self.mobile_network_processor = MobileNetwork()

    def test_valid_input(self):
        context = "0000000000"  
        expected_result = [0, 0]  
        result = self.mobile_network_processor.hex_bit_mobile_network(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.mobile_network_processor.hex_bit_mobile_network(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.mobile_network_processor.hex_bit_mobile_network(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "00"
        result = self.mobile_network_processor.hex_bit_mobile_network(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 1234
        result = self.mobile_network_processor.hex_bit_mobile_network(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
