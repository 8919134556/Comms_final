from hex_converter import HexConverter
from logger import Logger

class MobileNetwork():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_mobile_network(self, context):
        try:
            # Extract the mobile network bit from the context
            mobile_network_bit = context[:2]

            # Convert the hex bit to binary and reverse the binary string
            mobile_network_bit_binary = self.hex_converter.hex_to_binary(mobile_network_bit, 16)
            mobile_network_bit_binary = self.hex_converter.string_reverse_binary(mobile_network_bit_binary)

            # Extract GSM signal strength and network type
            gsm_signal = int(self.hex_converter.string_reverse(context[2:4]), 16)
            network_type_temp = int(self.hex_converter.string_reverse(context[4:6]), 16)

            # Extract the reserved data (not used in the result)
            reserved = self.hex_converter.string_reverse(context[6:10])

            result = [gsm_signal, network_type_temp]
            return result
        except Exception as e:
            self.logging.log_data("mobile_network", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    # Create an instance of MobileNetwork
    process_mobile_network = MobileNetwork()

    # Sample context with zeros, you may want to change this based on your requirements
    context = "0000000000"

    # Call the hex_bit_mobile_network method within a try-except block and print the result
    try:
        mobile_network_result = process_mobile_network.hex_bit_mobile_network(context)
        if mobile_network_result is not None:
            print(mobile_network_result)
    except Exception as e:
        # Handle any exceptions that might occur during the processing
        print(f"An error occurred during processing: {e}")
