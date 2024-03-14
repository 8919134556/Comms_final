from hex_converter import HexConverter
from logger import Logger

class BasicStatus():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_basic_status(self, context):
        try:
            basic_status_bit_binary = self.hex_converter.hex_to_binary(context[0:2], 16)
            basic_status_bit_binary = self.hex_converter.string_reverse_binary(basic_status_bit_binary) # 1000000000000000
            acc = basic_status_bit_binary[0:1]
            ignition = int(acc)
            break_1 = basic_status_bit_binary[1:2]
            turn_left = basic_status_bit_binary[2:3]
            turn_right = basic_status_bit_binary[3:4]
            forward = basic_status_bit_binary[4:5]
            backward = basic_status_bit_binary[5:6]
            left_front_door = basic_status_bit_binary[6:7]
            right_front_door = basic_status_bit_binary[7:8]

            basic_status_bit_binary_2 = self.hex_converter.hex_to_binary(context[2:4], 16)
            basic_status_bit_binary_2 = self.hex_converter.string_reverse_binary(basic_status_bit_binary_2)
            left_middle_door = basic_status_bit_binary_2[0:1]
            right_middle_door = basic_status_bit_binary_2[1:2]
            left_back_door = basic_status_bit_binary_2[2:3]
            right_back_door = basic_status_bit_binary_2[3:4]

            # context:[4:8] ---> reverse
            
            result=[ignition, break_1, turn_left, turn_right, forward, 
                    backward, left_front_door, right_front_door, left_middle_door, right_middle_door,
                    left_back_door, right_back_door]
            return result

        except Exception as e:
            self.logging.log_data("basic_status", f"Error processing GPS data: {e}")
            return None

if __name__ == "__main__":
    process_basic_status = BasicStatus()
    context = "01000000"
    basic_status = process_basic_status.hex_bit_basic_status(context)
    
    if basic_status is not None:
        print(basic_status)
    else:
        print("Failed to process basic status data.")
