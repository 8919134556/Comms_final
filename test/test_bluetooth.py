import unittest
from src.bluetooth import BluetoothStatus

class TestBluetoothStatus(unittest.TestCase):

    def setUp(self):
        self.bluetooth_status_processor = BluetoothStatus()

    def test_valid_input(self):
        context = "01"  
        expected_result = 2 
        result = self.bluetooth_status_processor.hex_bit_bluetooth_status(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.bluetooth_status_processor.hex_bit_bluetooth_status(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.bluetooth_status_processor.hex_bit_bluetooth_status(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "0"
        result = self.bluetooth_status_processor.hex_bit_bluetooth_status(context)
        self.assertIsNone(result)

    def test_integer_input(self):
        context = 123456
        result = self.bluetooth_status_processor.hex_bit_bluetooth_status(context)
        self.assertIsNone(result)
    

if __name__ == '__main__':
    unittest.main()
