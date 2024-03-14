from hex_converter import HexConverter
from logger import Logger

class DriverStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_driver_status(self, context):
        try:
            driver_length_of_package = int(self.hex_converter.string_reverse(context), 16) * 2
            return driver_length_of_package
        except Exception as e:
            self.logging.log_data("driver_status", f"(length) Error processing GPS data: {e}")
            return None

    def driver_signal_packet_data(self, context):
        try:
            driver = self.hex_converter.convert_hex_to_ascii(context).strip()
            result = driver.split(',')
            result = [value.strip() for value in result]
            return result
        except Exception as e:
            self.logging.log_data("driver_status", f"(hex-str) Error processing GPS data: {e}")
            return None


if __name__ == "__main__":
    process_driver_status = DriverStatus()
    context = "17"
    driver_status = process_driver_status.hex_bit_driver_status(context)
    print(driver_status)

    driver_context = "323333333333333334343434343434352c626c61636b00"
    signal_driver_info = process_driver_status.driver_signal_packet_data(driver_context)
    print(signal_driver_info)
