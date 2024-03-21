import unittest
from src.gps.g_sensor import GSensor

class TestGSensor(unittest.TestCase):

    def setUp(self):
        self.g_sensor = GSensor()

    def test_valid_input(self):
        context = "0700000000000000000000"
        expected_result = [0.0, 0.0, 0.0, 0.0, 0.0]
        result = self.g_sensor.hex_bit_g_sensor(context)
        self.assertEqual(result, expected_result)
    
    def test_invalid_input(self):
        context = "070000000000"
        result = self.g_sensor.hex_bit_g_sensor(context)
        self.assertIsNone(result)
    
    def test_alpha_value_input(self):
        context = "abcd"
        result = self.g_sensor.hex_bit_g_sensor(context)
        self.assertIsNone(result)
    
    def test_none_value_input(self):
        context = ""
        result = self.g_sensor.hex_bit_g_sensor(context)
        self.assertIsNone(result)
    
    def test_integer_value_input(self):
        context = 123456
        result = self.g_sensor.hex_bit_g_sensor(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
