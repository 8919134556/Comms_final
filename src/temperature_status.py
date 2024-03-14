from hex_converter import HexConverter
from logger import Logger

class TemperatureStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_temperature_status(self, context):
        try:
            temperature_bit_identifier = context[:4]
            temperature_bit_identifier = self.hex_converter.string_reverse(temperature_bit_identifier)
            temperature_bit_identifier_binary = self.hex_converter.hex_to_binary(temperature_bit_identifier, 16)
            temperature_bit_identifier_binary = self.hex_converter.string_reverse_binary(temperature_bit_identifier_binary)

            in_vehicle_temperature_data_valid = temperature_bit_identifier_binary[0]
            outside_of_vehicle_temperature_data_valid = temperature_bit_identifier_binary[1]
            motor_temperature_data_valid = temperature_bit_identifier_binary[2]
            device_temperature_data_valid = temperature_bit_identifier_binary[3]
            in_vehicle_humidity_data_valid = temperature_bit_identifier_binary[4]
            outside_of_vehicle_humidity_data_valid = temperature_bit_identifier_binary[5]

            in_vehicle_temperature, outside_of_vehicle_temperature, motor_temperature, device_temperature, in_vehicle_humidity, outside_of_vehicle_humidity = None, None, None, None, None, None

            if in_vehicle_temperature_data_valid == "1":
                in_vehicle_temperature = int(context[4:8], 16)
            
            if outside_of_vehicle_temperature_data_valid == "1":
                outside_of_vehicle_temperature = int(context[8:12], 16)
            
            if motor_temperature_data_valid == "1":
                motor_temperature = int(context[12:16], 16)
            
            if device_temperature_data_valid == "1":
                device_temperature = int(context[16:20], 16)
            
            if in_vehicle_humidity_data_valid == "1":
                in_vehicle_humidity = int(context[20:22], 16)
            
            if outside_of_vehicle_humidity_data_valid == "1":
                outside_of_vehicle_humidity = int(context[22:24], 16)
            
            result = [in_vehicle_temperature, outside_of_vehicle_temperature, motor_temperature, 
                    device_temperature, in_vehicle_humidity, outside_of_vehicle_humidity]
            return result

        except Exception as e:
            self.logging.log_data("temperature_status", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_temperature_status = TemperatureStatus()
    context = "3f0000000000000000000000"
    temperature_status = process_temperature_status.hex_bit_temperature_status(context)
    print(temperature_status)
