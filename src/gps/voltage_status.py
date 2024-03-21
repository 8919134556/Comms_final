from hex_converter import HexConverter
from logger import Logger

class VoltageStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_voltage_status(self, context):
        try:
            voltage_status_bit = int(context[:2], 16)
            voltage_length_of_package = int(self.hex_converter.string_reverse(context[2:6]), 16) * 2 * voltage_status_bit
            return voltage_length_of_package
        except Exception as e:
            self.logging.log_data("voltage_status", f"(length) Error processing GPS data: {e}")
            return None
    
    def voltage_signal_packet_data(self, context):
        try:
            voltage = int(self.hex_converter.string_reverse(context[0:4]), 16) / 100
            return voltage
        except Exception as e:
            self.logging.log_data("voltage_status", f"(hex-str) Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_voltage_status = VoltageStatus()

    # Example for hex_bit_voltage_status
    context = "020200"
    try:
        voltage_status = process_voltage_status.hex_bit_voltage_status(context)
        if voltage_status is not None:
            print(voltage_status)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Example for voltage_signal_packet_data
    signal_context = "e2040000"
    try:
        signal_voltage_info = process_voltage_status.voltage_signal_packet_data(signal_context)
        if signal_voltage_info is not None:
            print(signal_voltage_info)
    except Exception as e:
        print(f"An error occurred: {e}")
