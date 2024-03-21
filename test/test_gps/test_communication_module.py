import unittest
from src.gps.communication_module import CommunicationModule  

class TestCommunicationModule(unittest.TestCase):

    def setUp(self):
        self.communication_module_processor = CommunicationModule()

    def test_valid_input(self):
        context = "1f00000103010b00"
        expected_result = [0, 1, 3, 1, '1,2,4'] 
        result = self.communication_module_processor.hex_bit_communication_module(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.communication_module_processor.hex_bit_communication_module(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.communication_module_processor.hex_bit_communication_module(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "1f"
        result = self.communication_module_processor.hex_bit_communication_module(context)
        self.assertIsNone(result)

    def test_integer_input(self):
        context = 1
        result = self.communication_module_processor.hex_bit_communication_module(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
