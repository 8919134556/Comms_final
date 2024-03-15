import asyncio
import aioredis
import configparser
from logger import Logger
from datetime import datetime
from gps_process import GpsDataProcessor


class GPSData:
    def __init__(self, config_file="src/config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.logging = Logger()
        self.redis_client = None
        self.redis_key = self.config.get('Redis', 'key')
        self.gps_data_processor = GpsDataProcessor()
        self.previous_date_time = ''

    async def connect_to_redis(self):
        try:
            redis_host = self.config.get('Redis', 'host')
            redis_port = self.config.getint('Redis', 'port')
            self.redis_client = await aioredis.create_redis_pool(f'redis://{redis_host}:{redis_port}')
        except Exception as e:
            self.logging.log_data("RedisError", f"main.py ---> Error connecting to Redis: {e}")

    async def fetch_and_process_data_from_redis(self, sleep_duration=1, max_iterations=None):
        iterations = 0
        while max_iterations is None or iterations < max_iterations:
            try:
                value = await self.redis_client.blpop(self.redis_key, timeout=sleep_duration)
                if value:
                    decoded_value = value[1].decode('utf-8')
                    await self.process_gps_data(decoded_value)
                else:
                    await asyncio.sleep(sleep_duration)
            except aioredis.RedisError as redis_error:
                self.logging.log_data("RedisError", f"main.py ---> Redis error: {redis_error}")
                await asyncio.sleep(sleep_duration)
            iterations += 1

    async def process_gps_data(self, data):
        try:
            unit_no, version, device_network_type, hex_data = data.split('|')
            message_type = hex_data[6:8] + hex_data[4:6]
            if hex_data and message_type == '1041':
                result = self.gps_data_processor.process_gps_service_data(
                    unit_no, message_type, "Normal", hex_data, version, device_network_type)
                message = f"{datetime.now()} - hex_data: {hex_data}, Unit: {unit_no}"
                self.logging.log_data("1041", message)
            else:
                message = f"Invalid message type data: {hex_data}"
                self.logging.log_data("InvalidMessageType", message)
        except ValueError:
            self.logging.log_data("InvalidDataFormat", f"main.py ---> Invalid data format retrieved from Redis: {data}")
        except Exception as e:
            self.logging.log_data("DataProcessingError", f"main.py ---> Error processing GPS data: {e}")

if __name__ == '__main__':
    gps_data_processor = GPSData()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gps_data_processor.connect_to_redis())
    tasks = [
        gps_data_processor.fetch_and_process_data_from_redis()
    ]
    loop.run_until_complete(asyncio.gather(*tasks))
