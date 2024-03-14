from hex_converter import HexConverter
from logger import Logger

class WifiNetwork():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_wifi_network(self, context):
        try:
            # Extract the wifi network bit from the context
            wifi_network_bit = context[:2]

            # Convert the hex bit to binary and reverse the binary string
            wifi_network_bit_binary = self.hex_converter.hex_to_binary(wifi_network_bit, 16)
            wifi_network_bit_binary = self.hex_converter.string_reverse_binary(wifi_network_bit_binary)

            # Extract flags indicating the presence of various data
            signal_intensity_data_valid = wifi_network_bit_binary[0:1]
            network_address_data_valid = wifi_network_bit_binary[1:2]
            gateway_data_valid = wifi_network_bit_binary[2:3]
            subnet_mask_data_valid = wifi_network_bit_binary[3:4]
            ssid_length_data_valid = wifi_network_bit_binary[4:5]

            # Initialize variables to store data
            signal_intensity = 0
            network_address = 0
            gateway = 0
            subnet_mask = 0
            ssid_length = 0

            # Check if signal intensity data is valid and extract the value
            if signal_intensity_data_valid == "1":
                signal_intensity = int(self.hex_converter.string_reverse(context[2:4]), 16)

            # Check if network address data is valid and extract the value
            if network_address_data_valid == "1":
                network_address = int(self.hex_converter.string_reverse(context[4:12]), 16)

            # Check if gateway data is valid and extract the value
            if gateway_data_valid == "1":
                gateway = int(self.hex_converter.string_reverse(context[12:20]), 16)

            # Check if subnet mask data is valid and extract the value
            if subnet_mask_data_valid == "1":
                subnet_mask = int(self.hex_converter.string_reverse(context[20:28]), 16)

            # Check if SSID/SSID length data is valid and extract the value
            if ssid_length_data_valid == "1":
                ssid_length_temp = context[28:30]
                ssid_length = int(ssid_length_temp, 16)

            result = [signal_intensity, network_address, gateway, subnet_mask, ssid_length]
            return result

        except Exception as e:
            self.logging.log_data("wifi_network", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    # Create an instance of WifiNetwork
    process_wifi_network = WifiNetwork()

    # Sample context with zeros, you may want to change this based on your requirements
    context = "000000000000000000000000000000"

    # Call the hex_bit_wifi_network method within a try-except block and print the result
    try:
        wifi_network_result = process_wifi_network.hex_bit_wifi_network(context)
        if wifi_network_result is not None:
            print(wifi_network_result)
    except Exception as e:
        # Handle any exceptions that might occur during the processing
        print(f"An error occurred during processing: {e}")
