from hex_converter import HexConverter
from logger import Logger


class AlarmStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_alarm_status(self, context):
        try:
            alarm_status_bit_identifier = context[:8]
            alarm_status_bit_identifier = self.hex_converter.string_reverse(alarm_status_bit_identifier)
            alarm_status_bit_identifier_binary = self.hex_converter.hex_to_binary(alarm_status_bit_identifier, 16)
            alarm_status_bit_identifier_binary = self.hex_converter.string_reverse_binary(alarm_status_bit_identifier_binary)

            video_loss_data_valid = alarm_status_bit_identifier_binary[0]
            motion_detection_data_valid = alarm_status_bit_identifier_binary[1]
            video_blind_data_valid = alarm_status_bit_identifier_binary[2]
            alarm_input_trigger_data_valid = alarm_status_bit_identifier_binary[3]
            over_speed_alarm = alarm_status_bit_identifier_binary[4]
            low_speed_alarm = alarm_status_bit_identifier_binary[5]
            emergency_alarm = alarm_status_bit_identifier_binary[6]
            over_time_stop = alarm_status_bit_identifier_binary[7]
            vibration_alarm = alarm_status_bit_identifier_binary[8]
            out_of_GEO_fencing_alarm = alarm_status_bit_identifier_binary[9]
            enter_GEO_fencing_alarm = alarm_status_bit_identifier_binary[10]
            exist_line_alarm = alarm_status_bit_identifier_binary[11]
            enter_line_alarm = alarm_status_bit_identifier_binary[12]
            fuel_level_alarm = alarm_status_bit_identifier_binary[13]

            video_loss, motion_detection, video_blind, alarm_input_trigger = None, None, None, None

            if video_loss_data_valid == "1":
                video_loss = context[8:12]
                video_loss = self.hex_converter.string_reverse(video_loss)
                video_loss = self.hex_converter.hex_to_binary(video_loss, 16)
                video_loss = self.hex_converter.string_reverse_binary(video_loss)
                video_loss_channels = [str(i + 1) for i, bit in enumerate(video_loss) if bit == "1"]
                video_loss = ",".join(video_loss_channels)

            if motion_detection_data_valid == "1":
                motion_detection = context[12:16]
                motion_detection = self.hex_converter.string_reverse(motion_detection)
                motion_detection = self.hex_converter.hex_to_binary(motion_detection, 16)
                motion_detection = self.hex_converter.string_reverse_binary(motion_detection)
                motion_detection_channels = [str(i + 1) for i, bit in enumerate(motion_detection) if bit == "1"]
                motion_detection = ",".join(motion_detection_channels)

            if video_blind_data_valid == "1":
                video_blind = context[16:20]
                video_blind = self.hex_converter.string_reverse(video_blind)
                video_blind = self.hex_converter.hex_to_binary(video_blind, 16)
                video_blind = self.hex_converter.string_reverse_binary(video_blind)
                video_blind_channels = [str(i + 1) for i, bit in enumerate(video_blind) if bit == "1"]
                video_blind = ",".join(video_blind_channels)

            if alarm_input_trigger_data_valid == "1":
                alarm_input_trigger = context[20:24]
                alarm_input_trigger = self.hex_converter.string_reverse(alarm_input_trigger)
                alarm_input_trigger = self.hex_converter.hex_to_binary(alarm_input_trigger, 16)
                alarm_input_trigger = self.hex_converter.string_reverse_binary(alarm_input_trigger)
                alarm_input_trigger_channels = [str(i + 1) for i, bit in enumerate(alarm_input_trigger) if bit == "1"]
                alarm_input_trigger = ",".join(alarm_input_trigger_channels)

            result = [video_loss, motion_detection, video_blind, alarm_input_trigger]

            return result
        except Exception as e:
            self.logging.log_data("alarm_status", "Error processing GPS data: {}".format(e))

            return None

if __name__ == "__main__":
    process_alarm_status = AlarmStatus()
    context = "0f0000000600000000000000"
    alarm_status = process_alarm_status.hex_bit_alarm_status(context)
    print(alarm_status)
