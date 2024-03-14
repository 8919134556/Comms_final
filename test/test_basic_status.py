import unittest
from src.basic_status import BasicStatus  # Replace 'your_module_name' with the actual module name

class TestBasicStatus(unittest.TestCase):

    def setUp(self):
        self.basic_status_processor = BasicStatus()

    def test_valid_input(self):
        context = "01000000"
        expected_result = [1, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        result = self.basic_status_processor.hex_bit_basic_status(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.basic_status_processor.hex_bit_basic_status(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.basic_status_processor.hex_bit_basic_status(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "01"
        result = self.basic_status_processor.hex_bit_basic_status(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 1
        result = self.basic_status_processor.hex_bit_basic_status(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
