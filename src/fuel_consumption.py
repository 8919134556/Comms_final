from hex_converter import HexConverter
from logger import Logger

class FuelConsumption():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_fuel_consumption(self, context):
        try:
            # Extract the fuel consumption bit from the context
            fuel_consumption_bit = context[:2]

            # Convert the hex bit to binary and reverse the binary string
            fuel_consumption_bit_binary = self.hex_converter.hex_to_binary(fuel_consumption_bit, 16)
            fuel_consumption_bit_binary = self.hex_converter.string_reverse_binary(fuel_consumption_bit_binary)

            # Extract the fuel consumption and balance fuel data
            fuel_consumption_data_exist = fuel_consumption_bit_binary[0:1]
            balance_fuel_data_exist = fuel_consumption_bit_binary[1:2]

            fuel_consumption = 0
            balance_fuel = 0

            # Check if fuel consumption data exists and extract the value
            if fuel_consumption_data_exist == "1":
                fuel_consumption = int(self.hex_converter.string_reverse(context[2:6]), 16)

            # Check if balance fuel data exists and extract the value
            if balance_fuel_data_exist == "1":
                balance_fuel = int(self.hex_converter.string_reverse(context[6:10]), 16)

            result = [fuel_consumption, balance_fuel]
            return result

        except Exception as e:
            self.logging.log_data("fuel_consumption", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    # Create an instance of FuelConsumption
    process_fuel_consumption = FuelConsumption()

    # Sample context with zeros, you may want to change this based on your requirements
    context = "0000000000"

    # Call the hex_bit_fuel_consumption method and print the result
    fuel_consumption_result = process_fuel_consumption.hex_bit_fuel_consumption(context)
    
    if fuel_consumption_result is not None:
        print(fuel_consumption_result)
    else:
        print("Failed to process fuel consumption data.")
