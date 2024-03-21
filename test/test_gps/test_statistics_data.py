import unittest
from src.gps.statistics_data import StatisticsStatus

class TestStatisticsStatus(unittest.TestCase):

    def setUp(self):
        self.statistics_status_processor = StatisticsStatus()

    def test_valid_input(self):
        context = "01009efb010000000000"
        expected_result = [129950, 0]
        result = self.statistics_status_processor.hex_bit_statistics_status(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.statistics_status_processor.hex_bit_statistics_status(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.statistics_status_processor.hex_bit_statistics_status(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "01"
        result = self.statistics_status_processor.hex_bit_statistics_status(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 123456
        result = self.statistics_status_processor.hex_bit_statistics_status(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
