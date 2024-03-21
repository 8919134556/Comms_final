from hex_converter import HexConverter
from logger import Logger

class StatisticsStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_statistics_status(self, context):
        try:
            statistics_status_bit_identifier = context[:4]
            statistics_status_bit_identifier = self.hex_converter.string_reverse(statistics_status_bit_identifier)
            statistics_status_bit_identifier_binary = self.hex_converter.hex_to_binary(statistics_status_bit_identifier, 16)
            statistics_status_bit_identifier_binary = self.hex_converter.string_reverse_binary(statistics_status_bit_identifier_binary)
            
            if statistics_status_bit_identifier_binary[0] == "1":
                total_mileage = int(self.hex_converter.string_reverse(context[4:12]), 16)
                current_day_mileage = int(self.hex_converter.string_reverse(context[12:20]), 16)
                result = [total_mileage, current_day_mileage]
                return result
            else:
                result = [None, None]
                return result
        except Exception as e:
            self.logging.log_data("static_status", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_statistics_status = StatisticsStatus()
    context = "0100d4ea0900b2070000"#"01009efb010000000000"
    try:
        statistics_status = process_statistics_status.hex_bit_statistics_status(context)
        if statistics_status is not None:
            print(statistics_status)
    except Exception as e:
        print(f"An error occurred during processing: {e}")
