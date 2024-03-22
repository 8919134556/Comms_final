import asyncio
import aioredis
import configparser
from logger import Logger
from datetime import datetime
from hex_converter import HexConverter
from alarm_process_data import AlarmDataProcessor

class AlarmProcessor:
    def __init__(self, config_file="src/config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.logging = Logger()
        self.hex_converter = HexConverter()
        self.alarm_process_data = AlarmDataProcessor()
        self.redis_client = None
        self.redis_key = self.config.get('Redis', 'key')

    async def setup_redis(self):
        redis_host = self.config.get('Redis', 'host')
        redis_port = self.config.getint('Redis', 'port')
        self.redis_client = await aioredis.create_redis_pool(f'redis://{redis_host}:{redis_port}')

    async def fetch_and_process_data_from_redis(self, sleep_duration=10, max_iterations=None):
        
        iterations = 0

        while max_iterations is None or iterations < max_iterations:
            value = await self.redis_client.lpop(self.redis_key)

            if value:
                decoded_value = value.decode('utf-8')
                await self.process_data(decoded_value)
            else:
                await asyncio.sleep(sleep_duration)

            iterations += 1

    async def process_data(self, data):
        # Split the data into unit_no and hex_data
        data_parts = data.split('|')
        event_type = None
        if len(data_parts) == 4:
            unit_no,version,device_Network_Type, hex_data = data_parts
            filter_data = self.hex_converter.extract_substrings(hex_data.lower())
            load_data = filter_data[0]
            bit_data = filter_data[1]
            messageType = load_data[6:8]+load_data[4:6]
            if load_data:
                if messageType == "1051":
                    load_data = load_data[16:-4]
                    ss_no_len = int(load_data[0:2], 16)
                    content_len_temp = self.hex_converter.reverse_little_endian(load_data[(ss_no_len * 2) + 2:(ss_no_len * 2) + 2 + 4])
                    content_len = int(content_len_temp, 16)
                    content_hex = load_data[(ss_no_len * 2) + 10:(ss_no_len * 2) + 10 + (content_len * 2)]
                    try:
                        alarm_process = self.alarm_process_data.alarm_process_service_data(unit_no,content_hex,bit_data,messageType,version,device_Network_Type)
                        message = f"{datetime.now()} - Unit: {unit_no}, Hex Data: {hex_data}"
                        self.logging.log_data("1051", message)
                    except Exception as e:
                        message = f"{datetime.now()} - Unit: {unit_no}, Exception : {e}"
                        self.logging.log_data("1051_exception", message)
                else:
                    message = f"Invalid message type data : "+{load_data}
                    self.logging.log_data("Invalid_msg_type", message)
            else:
                pass      
        else:
            self.logging.log_data("Invalid_data", f"Error: Invalid data format retrieved from Redis : ",{data_parts})



if __name__ == "__main__":
    alarm_processor = AlarmProcessor()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(alarm_processor.setup_redis())
    # Create tasks for both data processing and folder deletion
    tasks = [
        alarm_processor.fetch_and_process_data_from_redis()
    ]

    loop.run_until_complete(asyncio.gather(*tasks))

