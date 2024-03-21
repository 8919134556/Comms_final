from hex_converter import HexConverter
from logger import Logger

class OBDInfo():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_obd_info(self, context):
        try:
            obd_info_bit = int(context[:2], 16)
            length_of_package = int(self.hex_converter.string_reverse(context[2:6]), 16) * 2 *obd_info_bit
            result = [obd_info_bit, length_of_package]
            return result
        except Exception as e:
            self.logging.log_data("obd_info", f"(length) Error processing GPS data: {e}")
            return None
    def obd_signal_packet_data(self, context):
        try:
            accumulated_mileage = int(self.hex_converter.string_reverse(context[0:8]), 16)
            cumulative_fuel_consumption = int(self.hex_converter.string_reverse(context[8:16]), 16)
            instant_fuel_consumption = int(self.hex_converter.string_reverse(context[16:24]), 16)*100
            vehicle_voltage = int(self.hex_converter.string_reverse(context[24:28]), 16)*100
            engine_speed = int(self.hex_converter.string_reverse(context[28:32]), 16)
            speed = int(self.hex_converter.string_reverse(context[32:36]), 16)*100
            intake_air_flow = int(self.hex_converter.string_reverse(context[36:38]), 16)
            intake_pressure = int(self.hex_converter.string_reverse(context[38:40]), 16)
            coolant_temperature = int(self.hex_converter.string_reverse(context[40:42]), 16)
            intake_air_temperature = int(self.hex_converter.string_reverse(context[42:44]), 16)
            engine_load = int(self.hex_converter.string_reverse(context[44:46]), 16)
            throttle_position = int(self.hex_converter.string_reverse(context[46:48]), 16)
            remaining_oil = int(self.hex_converter.string_reverse(context[48:50]), 16)
            engine_status = int(self.hex_converter.string_reverse(context[50:54]), 16)
            i_year = int(context[54:56])
            i_month = int(context[56:58])
            i_day = int(context[58:60])
            i_hour = int(context[60:62])
            i_minute = int(context[62:64])
            i_second = int(context[64:66])
            engine_on_time = f"{i_year + 2000}-{i_month:02d}-{i_day:02d} {i_hour:02d}:{i_minute:02d}:{i_second:02d}"
            i_year = int(context[66:68])
            i_month = int(context[68:70])
            i_day = int(context[70:72])
            i_hour = int(context[72:74])
            i_minute = int(context[74:76])
            i_second = int(context[76:78])
            engineOffTime = f"{i_year + 2000}-{i_month:02d}-{i_day:02d} {i_hour:02d}:{i_minute:02d}:{i_second:02d}"
            idling_status = int(self.hex_converter.string_reverse(context[78:80]), 16)
            hc = int(self.hex_converter.string_reverse(context[80:82]), 16)
            ha = int(self.hex_converter.string_reverse(context[82:84]), 16)
            hb = int(self.hex_converter.string_reverse(context[84:86]), 16)
            low_Battery_voltage = int(self.hex_converter.string_reverse(context[86:88]), 16)
            
            
            result = [accumulated_mileage, cumulative_fuel_consumption, instant_fuel_consumption, vehicle_voltage, engine_speed,
                    speed, intake_air_flow, intake_pressure, coolant_temperature, intake_air_temperature, engine_load, throttle_position,
                    remaining_oil, engine_status, engine_on_time, engineOffTime, idling_status, hc, ha, hb, low_Battery_voltage] 
            return result
        except Exception as e:
            self.logging.log_data("obd_info", f"(hex-str) Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_obd_info = OBDInfo()
    context = "012c00"
    obd_info = process_obd_info.hex_bit_obd_info(context)
    print(obd_info)

    signal_context = "0000000000000000000000000000000000000000000000000000002302081542590000000000000000000000"
    signal_obd_info = process_obd_info.obd_signal_packet_data(signal_context)
    print(signal_obd_info)
