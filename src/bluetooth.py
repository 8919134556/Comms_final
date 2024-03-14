from hex_converter import HexConverter
from logger import Logger

class BluetoothStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_bluetooth_status(self, context):
        try:
            bluetooth_length_of_package = int(self.hex_converter.string_reverse(context), 16) * 2
            return bluetooth_length_of_package
        except Exception as e:
            self.logging.log_data("bluetooth_status", f"(length) Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_bluetooth_status = BluetoothStatus()
    context = "01"
    bluetooth_status = process_bluetooth_status.hex_bit_bluetooth_status(context)

    if bluetooth_status is not None:
        print(bluetooth_status)
    else:
        print("Failed to process Bluetooth status.")
