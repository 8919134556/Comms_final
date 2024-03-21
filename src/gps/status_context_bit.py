from hex_converter import HexConverter

class StatusContextBit():
    def __init__(self):
        self.hex_converter = HexConverter()

    def hex_bit_status_context(self, context):
        content_reverse = self.hex_converter.string_reverse(context)
        binary_content = self.hex_converter.hex_to_binary(content_reverse, 16)
        status_context_bit = self.hex_converter.string_reverse_binary(binary_content)
        return status_context_bit

if __name__=="__main__":
    process_status_context_bit = StatusContextBit()
    context = "aff7"
    status_context_bit = process_status_context_bit.hex_bit_status_context(context)
    print(status_context_bit)