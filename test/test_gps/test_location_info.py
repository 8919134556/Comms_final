import unittest
from src.gps.location_info import LocationInfo

class TestLocationInfo(unittest.TestCase):

    def setUp(self):
        self.process_location_info = LocationInfo()

    def test_positive_case(self):
        # Test with valid context
        context = "0000170209092604750300009b00170071c1a90800169f1c0500"
        result = self.process_location_info.hex_bit_location_info(context)
        self.assertIsNotNone(result)
    
    def test_negative_case(self):
        # Test with invalid context (shorter than expected)
        context = "0000170209092604750300"
        result = self.process_location_info.hex_bit_location_info(context)
        self.assertIsNone(result)
    
    def test_alpha_value_case(self):
        # Test with invalid context (shorter than expected)
        context = "abcd"
        result = self.process_location_info.hex_bit_location_info(context)
        self.assertIsNone(result)
    
    def test_integer_value_case(self):
        # Test with invalid context (shorter than expected)
        context = 123456789
        result = self.process_location_info.hex_bit_location_info(context)
        self.assertIsNone(result)
    
    def test_None_value_case(self):
        # Test with invalid context (shorter than expected)
        context = ""
        result = self.process_location_info.hex_bit_location_info(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
