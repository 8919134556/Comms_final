from db_inserting import DatabaseManager
from odometer_calculator import OdometerCalculator
from address_info import Geocoder
from datetime import datetime
from logger import Logger
import configparser
import redis
import json

class CurrentHistoryInsert:
    def __init__(self, config_file="src/config.ini"):
        self.config = configparser.ConfigParser()
        self.database_manager = DatabaseManager()
        self.odometer_calculator = OdometerCalculator()
        self.address_info = Geocoder()
        self.config.read(config_file)
        self.logging = Logger()
        self.connect_to_redis()

    def connect_to_redis(self):
        try:
            self.redis_host = self.config.get('Redis', 'host')
            self.redis_port = self.config.getint('Redis', 'port')
            self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0, decode_responses=True)
        except Exception as e:
            self.logging.log_data("redis_error", f'Error connecting to Redis: {str(e)}')

    def current_history_inserting(self, unit_no, lat, lon, device_date_time, driver_id, polling_mode, ignition, speed, direction, gps_module, voltage):
        try:
            previous_data = self.redis_client.hget(unit_no, 'previous_record')
            if previous_data is None or previous_data == "null":
                previous_data = self.database_manager.previous_records(unit_no)
                self.redis_client.hset(unit_no, 'previous_record', json.dumps(previous_data))
            else:
                previous_data = json.loads(previous_data)
        except Exception as e:
            self.logging.log_data("redis_error", f'Error while getting previous record: {str(e)}')

        try:
            previous_date_time = previous_data[7]
        except Exception as e:
            self.logging.log_data("redis_error", f'Error while getting previous date time: {str(e)}')

        try:
            device_date_time = datetime.strptime(device_date_time, '%Y-%m-%d %H:%M:%S')
            previous_date_time = datetime.strptime(previous_date_time, '%Y-%m-%d %H:%M:%S')
            current_history_records = []
            Vehicle_id_data = self.database_manager.get_records(unit_no)
            Vehicle_id = int(Vehicle_id_data[0])
            Client_id = int(Vehicle_id_data[1])
            driver_RF_id = driver_id if driver_id else 0
            Vehicle_no = unit_no
            polling_mode = polling_mode
            track_time = device_date_time
            lat = lat
            lon = lon
            info_location = self.database_manager.get_address(float(lat), float(lon))
            location = info_location[0]
            if location == ['None']:  # Check if the result is ['None']
                location = self.address_info.reverse_geocode_and_print_address(float(lat), float(lon), "en")
                if location is not None:  # Check if a valid address is obtained
                    location = location.encode('utf-8')
                    self.database_manager.insert_address(float(lat), float(lon), location)
            location_near_by = ""
            road_type = " "
            ignition = ignition
            speed = int(speed)
            odo_meter = self.odometer_calculator.calculate_distance(float(lat), float(lon), float(previous_data[8]), float(previous_data[9]), float(previous_data[15]))
            direction = float(direction)
            gps_status = gps_module
            immobalizer = 0
            panic = 0
            seatbelt = 0
            main_power = 1 if voltage else 0
            idle_duration = 0
            stop_duration = 0
            travel_duration = 0
            ModifiedDate = datetime.now()
            ModifiedUserId = 0
            AlertInd = 0
            GEO_FENCE_ID = 0
            
            current_history_records.append((Vehicle_id, Client_id, driver_RF_id, Vehicle_no, unit_no, polling_mode, track_time,
                                            lat, lon, location, location_near_by, road_type, ignition, speed, odo_meter,direction, gps_status,immobalizer,
                                            panic, main_power, seatbelt, idle_duration, stop_duration, travel_duration, ModifiedDate, ModifiedUserId,
                                            AlertInd, GEO_FENCE_ID))

            if previous_date_time <= device_date_time:
                try:
                    self.database_manager.current_records(current_history_records)
                    self.database_manager.history_records(current_history_records)
                except Exception as e:
                    self.logging.log_data("current_history_record_insert", f'Error during insert records into Current and history table: {str(e)}') 
                try:
                    previous_data[6] = polling_mode
                    previous_data[7] = str(track_time)
                    previous_data[8] = lat
                    previous_data[9] = lon
                    previous_data[15] = odo_meter
                    previous_data[16] = direction
                    previous_data[17] = gps_status
                    previous_data[18] =immobalizer
                    previous_data[19] = panic 
                    previous_data[20] = main_power 
                    previous_data[21] = seatbelt 
                    previous_data[22] = idle_duration 
                    previous_data[23] = stop_duration 
                    previous_data[24] = travel_duration 
                    previous_data[25] = str(ModifiedDate) 
                    previous_data[26] = ModifiedUserId
                    previous_data[27] = AlertInd 
                    previous_data[28] = GEO_FENCE_ID

                    updated_record_str = json.dumps(previous_data)
                    self.redis_client.hset(unit_no, 'previous_record', updated_record_str)
                except Exception as e:
                    self.logging.log_data("redis_error", f'Error during update records into redis: {str(e)}') 
            else:
                self.database_manager.history_records(current_history_records)
        except Exception as e:
            self.logging.log_data("datetime_comparison_error", f'Error during datetime comparison: {str(e)}')

if __name__ == "__main__":
    current_history_insert = CurrentHistoryInsert()
    unit_no = "91006"
    lat = 33.8036231994629
    lon = -117.989677429199
    device_date_time = "2024-03-06 15:30:00"
    driver_id = "1234564"
    polling_mode = "testing"
    ignition = 1
    speed = 0.0
    gps_module = 1
    voltage = 12.5
    direction = 175
    current_history_insert.current_history_inserting(unit_no, lat, lon, device_date_time, driver_id, polling_mode, ignition, speed, direction, gps_module, voltage)
