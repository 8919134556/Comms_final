import unittest
from src.gps.temperature_status import TemperatureStatus  

class TestTemperatureStatus(unittest.TestCase):

    def setUp(self):
        self.temperature_status_processor = TemperatureStatus()

    def test_valid_input(self):
        context = "3f0000000000000000000000"
        expected_result = [0, 0, 0, 0, 0, 0]
        result = self.temperature_status_processor.hex_bit_temperature_status(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.temperature_status_processor.hex_bit_temperature_status(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.temperature_status_processor.hex_bit_temperature_status(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "3f00000000000"
        result = self.temperature_status_processor.hex_bit_temperature_status(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 123456
        result = self.temperature_status_processor.hex_bit_temperature_status(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
