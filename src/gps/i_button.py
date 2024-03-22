from hex_converter import HexConverter
from logger import Logger

class IButton():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_i_button(self, context):
        try:
            i_button_bit_identifier = context[:2]
            i_button_bit_identifier = self.hex_converter.string_reverse(i_button_bit_identifier)
            i_button_bit_binary = self.hex_converter.hex_to_binary(i_button_bit_identifier, 16)
            i_button_bit_binary = self.hex_converter.string_reverse_binary(i_button_bit_binary)

            ibutton_id_length = int(context[2:4], 16)
            result = ibutton_id_length * 2
            return result
        except Exception as e:
            self.logging.log_data("i_button", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_i_button = IButton()
    context = "0211"
    try:
        i_button = process_i_button.hex_bit_i_button(context)
        if i_button is not None:
            print(i_button)
    except Exception as e:
        print(f"An error occurred during processing: {e}")
