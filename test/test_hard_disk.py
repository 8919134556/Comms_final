import unittest
from src.hard_disk import HardDisk

class TestHardDisk(unittest.TestCase):

    def setUp(self):
        self.hard_disk_processor = HardDisk()

    def test_valid_input(self):
        context = "0110010d8e0e0000000000"  
        expected_result = ['sd2', 'recording', 931.5126953125, 0.0] 
        result = self.hard_disk_processor.hex_bit_hard_disk(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.hard_disk_processor.hex_bit_hard_disk(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.hard_disk_processor.hex_bit_hard_disk(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "00"
        result = self.hard_disk_processor.hex_bit_hard_disk(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 123456
        result = self.hard_disk_processor.hex_bit_hard_disk(context)
        self.assertIsNone(result)

    

if __name__ == '__main__':
    unittest.main()
