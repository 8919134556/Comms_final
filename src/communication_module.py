from hex_converter import HexConverter
from logger import Logger

class CommunicationModule:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_communication_module(self, context):
        try:
            communication_module_bit = context[:4]
            communication_module_bit_rev = self.hex_converter.string_reverse(communication_module_bit)
            communication_module_bit_binary = self.hex_converter.hex_to_binary(communication_module_bit_rev, 16)
            communication_module_bit_binary = self.hex_converter.string_reverse_binary(communication_module_bit_binary)
            
            mobile_network = gps_module = WIFI_module = Gsensor = recording_status = None
            mobile_net_work_data_exist = communication_module_bit_binary[0:1]
            gps_module_data_exist = communication_module_bit_binary[1:2]
            WIFI_module_data_exist = communication_module_bit_binary[2:3]
            Gsensor_data_exist = communication_module_bit_binary[3:4]
            recording_status_data_exist = communication_module_bit_binary[4:5]

            if mobile_net_work_data_exist == "1":
                mobile_network = int(context[4:6], 16)

            if gps_module_data_exist == "1":
                gps_module = int(context[6:8], 16)

            if WIFI_module_data_exist == "1":
                WIFI_module = int(context[8:10], 16)

            if Gsensor_data_exist == "1":
                Gsensor = int(context[10:12], 16)

            if recording_status_data_exist == "1":
                recording_status = context[12:16]
                recording_status = self.hex_converter.string_reverse(recording_status)
                recording_status = self.hex_converter.hex_to_binary(recording_status, 16)
                recording_status = self.hex_converter.string_reverse_binary(recording_status)
                channels_recording = []
                for i, bit in enumerate(recording_status):
                    if bit == "1":
                        channels_recording.append(str(i + 1))
                recording_status = ",".join(channels_recording)
            
            result = [mobile_network, gps_module, WIFI_module, Gsensor, recording_status]
            return result

        except Exception as e:
            self.logging.log_data("communication_module", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_communication_module = CommunicationModule()
    context = "1f00000103010b00"
    communication_module = process_communication_module.hex_bit_communication_module(context)
    
    if communication_module is not None:
        print(communication_module)
    else:
        print("Failed to process communication module data.")
