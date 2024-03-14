import unittest
from src.voltage_status import VoltageStatus

class TestVoltageStatus(unittest.TestCase):

    def setUp(self):
        self.voltage_status_processor = VoltageStatus()

    def test_hex_bit_voltage_status_valid_input(self):
        context = "020200" 
        expected_result = 8 
        result = self.voltage_status_processor.hex_bit_voltage_status(context)
        self.assertEqual(result, expected_result)

    def test_hex_bit_voltage_status_invalid_input(self):
        context = "invalid_context_data"
        result = self.voltage_status_processor.hex_bit_voltage_status(context)
        self.assertIsNone(result)
    
    def test_hex_bit_voltage_status_empty_input(self):
        context = " "
        result = self.voltage_status_processor.hex_bit_voltage_status(context)
        self.assertIsNone(result)
    
    def test_hex_bit_voltage_status_short_input(self):
        context = "020"
        result = self.voltage_status_processor.hex_bit_voltage_status(context)
        self.assertIsNone(result)
    
    def test_hex_bit_voltage_status_integer_input(self):
        context = 1234567
        result = self.voltage_status_processor.hex_bit_voltage_status(context)
        self.assertIsNone(result)

    def test_voltage_signal_packet_data_valid_input(self):
        context = "e2040000" 
        expected_result = 12.5
        result = self.voltage_status_processor.voltage_signal_packet_data(context)
        self.assertEqual(result, expected_result)

    def test_voltage_signal_packet_data_invalid_input(self):
        context = "invalid_context_data"
        result = self.voltage_status_processor.voltage_signal_packet_data(context)
        self.assertIsNone(result)
    
    def test_voltage_signal_packet_data_empty_input(self):
        context = ""
        result = self.voltage_status_processor.voltage_signal_packet_data(context)
        self.assertIsNone(result)

    def test_voltage_signal_packet_data_short_input(self):
        context = "e"
        result = self.voltage_status_processor.voltage_signal_packet_data(context)
        self.assertIsNone(result)
    
    def test_voltage_signal_packet_data_integer_input(self):
        context = 1234567
        result = self.voltage_status_processor.voltage_signal_packet_data(context)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
