from hex_converter import HexConverter
from logger import Logger

class HardDisk():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_hard_disk(self, context):
        try:
            hard_disk_bit = context[:2]
            hard_disk_bit_binary = self.hex_converter.hex_to_binary(hard_disk_bit, 16)
            hard_disk_bit_binary = self.hex_converter.string_reverse_binary(hard_disk_bit_binary)
            
            if hard_disk_bit_binary[0:1] == "1":
                id = int(context[2:4], 16)
                hard_disk_status = int(context[4:6], 16)
                hard_disk_size = int(self.hex_converter.string_reverse(context[6:14]), 16) / 1024
                hard_disk_balance = int(self.hex_converter.string_reverse(context[14:22]), 16) / 1024

                # Mapping disk types
                if 11 <= id <= 20:
                    disk_mapping = {
                        11: "hdd1",
                        12: "hdd2",
                        13: "hdd3",
                        14: "hdd4",
                        15: "sd1",
                        16: "sd2",
                        17: "sd3",
                        18: "sd4",
                        19: "usb1",
                        20: "usb2"
                    }
                    id = disk_mapping.get(id, f"Unknown Disk Type ({id})")

                # Mapping hard disk status
                status_mapping = {
                    0: "unknown",
                    1: "recording",
                    2: "idle",
                    3: "abnormal",
                    4: "full"
                }
                hard_disk_status = status_mapping.get(hard_disk_status, f"Unknown Status ({hard_disk_status})")

                result = [id, hard_disk_status, hard_disk_size, hard_disk_balance]
                return result

        except Exception as e:
            self.logging.log_data("hard_disk", f"Error processing GPS data: {e}")
            return None

if __name__=="__main__":
    process_hard_disk = HardDisk()
    context = "0110010d8e0e0000000000"
    try:
        hard_disk = process_hard_disk.hex_bit_hard_disk(context)
        if hard_disk is not None:
            print(hard_disk)
    except Exception as e:
        print(f"An error occurred: {e}")
