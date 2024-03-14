import unittest
from src.i_button import IButton

class TestIButton(unittest.TestCase):

    def setUp(self):
        self.i_button_processor = IButton()

    def test_valid_input(self):
        context = "0000"
        expected_result = [0]
        result = self.i_button_processor.hex_bit_i_button(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.i_button_processor.hex_bit_i_button(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.i_button_processor.hex_bit_i_button(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "0"
        result = self.i_button_processor.hex_bit_i_button(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 123
        result = self.i_button_processor.hex_bit_i_button(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
