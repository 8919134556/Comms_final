from hex_converter import HexConverter
from logger import Logger

class AlarmStatus:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_alarm_status(self, context):
        try:
            if len(context) < 24:
                raise ValueError("Context string is too short")

            # Extracting the alarm status bit identifier
            alarm_status_bit_identifier = context[:8]
            # Reversing the string
            alarm_status_bit_identifier = self.hex_converter.string_reverse(alarm_status_bit_identifier)
            # Converting hexadecimal to binary
            alarm_status_bit_identifier_binary = self.hex_converter.hex_to_binary(alarm_status_bit_identifier, 16)
            # Reversing the binary string
            alarm_status_bit_identifier_binary = self.hex_converter.string_reverse_binary(alarm_status_bit_identifier_binary)

            # Extracting individual alarm status flags
            flags = [
                "video_loss_data_valid", "motion_detection_data_valid", "video_blind_data_valid",
                "alarm_input_trigger_data_valid", "over_speed_alarm", "low_speed_alarm", "emergency_alarm",
                "over_time_stop", "vibration_alarm", "out_of_GEO_fencing_alarm", "enter_GEO_fencing_alarm",
                "exist_line_alarm", "enter_line_alarm", "fuel_level_alarm"
            ]

            alarm_flags = {}
            try:
                for i, flag in enumerate(flags):
                    if i < len(alarm_status_bit_identifier_binary):  # Check if index is within the bounds
                        alarm_flags[flag] = alarm_status_bit_identifier_binary[i]
                    else:
                        alarm_flags[flag] = None  # Placeholder value if index is out of bounds
            except Exception as e:
                self.logging.log_data("alarm_status", f"Error processing alarm data: {str(e)}")

            # Extracting specific alarm data based on flag validity
            result = {}
            for flag, valid in alarm_flags.items():
                if valid == "1":
                    start_index = 8 + 4 * len(result)
                    end_index = start_index + 4
                    if end_index <= len(context):
                        data = context[start_index:end_index]
                        data = self.hex_converter.string_reverse(data)
                        data = self.hex_converter.hex_to_binary(data, 16)
                        data = self.hex_converter.string_reverse_binary(data)
                        channels = [str(i + 1) for i, bit in enumerate(data) if bit == "1"]
                        result[flag] = ",".join(channels)
                    else:
                        result[flag] = None
                else:
                    result[flag] = None

            return [
                result.get("video_loss_data_valid"),
                result.get("motion_detection_data_valid"),
                result.get("video_blind_data_valid"),
                result.get("alarm_input_trigger_data_valid")
            ]
        except Exception as e:
            self.logging.log_data("alarm_status", f"Error processing GPS data: {str(e)}")
            return [None, None, None, None]

if __name__ == "__main__":
    process_alarm_status = AlarmStatus()
    context = "0f0000000f00000000000000"
    alarm_status = process_alarm_status.hex_bit_alarm_status(context)
    print(alarm_status)
