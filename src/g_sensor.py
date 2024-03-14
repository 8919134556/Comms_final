from hex_converter import HexConverter
from logger import Logger


class GSensor():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_g_sensor(self, context):
        try:
            g_sensor_bit_binary = self.hex_converter.hex_to_binary(context[:2], 16)
            g_sensor_bit_binary = self.hex_converter.string_reverse_binary(g_sensor_bit_binary) # 1110000000000000
            xyz_data_exist = g_sensor_bit_binary[0:1]
            tilt_data_exist = g_sensor_bit_binary[1:2]
            impact_data_exist = g_sensor_bit_binary[2:3]
            
            x_acceleration = y_acceleration = z_acceleration = tilt = impact = None

            if xyz_data_exist == "1":
                x_acceleration = int(self.hex_converter.string_reverse(context[2:6]), 16)
                if x_acceleration > 32767:
                    x_acceleration -= 65536
                    x_acceleration /= 100.0
                else:
                    x_acceleration /= 100.0

                y_acceleration = int(self.hex_converter.string_reverse(context[6:10]), 16)
                if y_acceleration > 32767:
                    y_acceleration -= 65536
                    y_acceleration /= 100.0
                else:
                    y_acceleration /= 100.0

                z_acceleration = int(self.hex_converter.string_reverse(context[10:14]), 16)
                if z_acceleration > 32767:
                    z_acceleration -= 65536
                    z_acceleration /= 100.0
                else:
                    z_acceleration /= 100.0

            if tilt_data_exist == "1":
                tilt = int(self.hex_converter.string_reverse(context[14:18]), 16) / 100.0

            if impact_data_exist == "1":
                impact = int(self.hex_converter.string_reverse(context[18:22]), 16) / 100.0
            
            result = [x_acceleration, y_acceleration, z_acceleration, tilt, impact]
            return result

        except Exception as e:
            self.logging.log_data("g_sensor", f"Error processing GPS data: {e}")
            return None

if __name__ == '__main__':
    process_g_sensor = GSensor()
    context = "070000ffff000000000100"#"0700000000000000000000"
    g_sensor = process_g_sensor.hex_bit_g_sensor(context)
    
    if g_sensor is not None:
        print(g_sensor)
    else:
        print("Failed to process G-sensor data.")
