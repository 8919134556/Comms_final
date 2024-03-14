import unittest
from src.fuel_consumption import FuelConsumption 

class TestFuelConsumption(unittest.TestCase):

    def setUp(self):
        self.fuel_consumption_processor = FuelConsumption()

    def test_valid_input(self):
        context = "0000000000"  
        expected_result = [0, 0]  
        result = self.fuel_consumption_processor.hex_bit_fuel_consumption(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.fuel_consumption_processor.hex_bit_fuel_consumption(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.fuel_consumption_processor.hex_bit_fuel_consumption(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "023"
        result = self.fuel_consumption_processor.hex_bit_fuel_consumption(context)
        self.assertIsNone(result)
    
    def test_integer_input(self):
        context = 0
        result = self.fuel_consumption_processor.hex_bit_fuel_consumption(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
