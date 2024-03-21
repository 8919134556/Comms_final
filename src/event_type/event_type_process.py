from hex_converter import HexConverter
from event_type.extract_event_info import ExtractEventInfo
import json

class AlarmEventType:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.extract_event_info = ExtractEventInfo()

    def process_event(self, json_hex_data):
        result = []
        ascii_data = self.hex_converter.convert_hex_to_ascii(json_hex_data)
        if ascii_data:
            json_data = json.loads(ascii_data)
            self.extract_event_info.extract_event_info(json_data)
            result= self.extract_event_info.extract_event_info(json_data)
        return result

    

if __name__ == "__main__":
    process_data = AlarmEventType()
    json_hex_data = "7b22646574223a7b226e756d223a22736432222c227374223a2234227d2c22647475223a22323032332d31312d30312030373a31323a3037222c226563223a223136222c226574223a22323032332d31312d30312030373a31323a3037222c227374223a22227d"
    json_hex_data = json_hex_data.lower()
    result = process_data.process_event(json_hex_data)
    print(result)
