import unittest
from src.obd_info import OBDInfo  

class TestOBDInfo(unittest.TestCase):

    def setUp(self):
        self.obd_info_processor = OBDInfo()

    def test_hex_bit_obd_info(self):
        context = "012c00"
        expected_result = [1, 88]
        result = self.obd_info_processor.hex_bit_obd_info(context)
        self.assertEqual(result, expected_result)
    
    def test_hex_bit_obd_info_invalid_input(self):
        context = "invalid_context_data"
        result = self.obd_info_processor.hex_bit_obd_info(context)
        self.assertIsNone(result)
    
    def test_hex_bit_obd_info_empty_input(self):
        context = ""
        result = self.obd_info_processor.hex_bit_obd_info(context)
        self.assertIsNone(result)
    
    def test_hex_bit_obd_info_short_input(self):
        context = "012"
        result = self.obd_info_processor.hex_bit_obd_info(context)
        self.assertIsNone(result)
    
    def test_hex_bit_obd_info_integer_input(self):
        context = 123456
        result = self.obd_info_processor.hex_bit_obd_info(context)
        self.assertIsNone(result)
    
    def test_obd_signal_packet_data(self):
        signal_context = "0000000000000000000000000000000000000000000000000000002302081542590000000000000000000000"
        expected_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-08 15:42:59', '2000-00-00 00:00:00', 0, 0, 0, 0, 0]  
        result = self.obd_info_processor.obd_signal_packet_data(signal_context)
        self.assertEqual(result, expected_result)

    def test_obd_signal_packet_data_invalid_input(self):
        signal_context = "invalid_signal_context_data"
        result = self.obd_info_processor.obd_signal_packet_data(signal_context)
        self.assertIsNone(result)
    
    def test_obd_signal_packet_data_empty_input(self):
        signal_context = " "
        result = self.obd_info_processor.obd_signal_packet_data(signal_context)
        self.assertIsNone(result)
    
    def test_obd_signal_packet_data_short_input(self):
        signal_context = "000000000000000000000000000000000"
        result = self.obd_info_processor.obd_signal_packet_data(signal_context)
        self.assertIsNone(result)
    
    def test_obd_signal_packet_data_integer_input(self):
        signal_context = 123456
        result = self.obd_info_processor.obd_signal_packet_data(signal_context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
