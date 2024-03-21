from hex_converter import HexConverter
from db_inserting import DatabaseManager
from logger import Logger
from datetime import datetime
from event_type.event_type_process import AlarmEventType
from current_history_data_inserting import CurrentHistoryInsert
from gps.gps_process import GpsDataProcessor
import configparser
import redis


class AlarmDataProcessor:
    def __init__(self, config_file="src/config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.logging = Logger()
        self.hex_converter = HexConverter()
        self.database_manager = DatabaseManager()
        self.event_type_process = AlarmEventType()
        self.gps_process = GpsDataProcessor ()
        self.connect_to_redis()
        self.current_history_insert = CurrentHistoryInsert()
        
    def connect_to_redis(self):
        try:
            self.redis_host = self.config.get('Redis', 'host')
            self.redis_port = self.config.getint('Redis', 'port')
            self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0, decode_responses=True)
        except Exception as e:
            self.logging.log_data("redis_error", f'Error While getting into redis connection error: {str(e)}')
                                    
    def alarm_process_service_data(self, unit_no,json_hex_data,gps_hex_data,messageType,version,device_Network_Type):
        event_type_result = None
        gps_result = None
        result = []
        try:
            event_type_result = self.event_type_process.process_event(json_hex_data)
        except Exception as e:
            print(e)
        try:
            gps_result = self.gps_process.process_gps_service_data(gps_hex_data)
        except Exception as e:
            print(e)
    
        unit_no
        unit_no
        messageType
        version,
        polling_mode = event_type_result[0]
        ch = event_type_result[1]
        seat_belt = event_type_result[2]
        fuel_bar = event_type_result[3]
        panic = event_type_result[4]
        max_value = event_type_result[5]
        min_value = event_type_result[6]
        average_value = event_type_result[7]
        current_value = event_type_result[8]
        previous_value = event_type_result[9]
        over_speed = event_type_result[10]
        parking_time = event_type_result[11]
        status = event_type_result[12]
        oil_tank_capacity = event_type_result[13]
        balance_fuel_capacity = event_type_result[14]
        swipe_card_type = event_type_result[15]
        swipe_card_info = event_type_result[16]
        DriverOrStudent_status = event_type_result[17]
        his_real_data = event_type_result[18]
        card_type = event_type_result[19]
        Dw0 = event_type_result[23]
        Dw1 = event_type_result[24]
        Dw2 = event_type_result[25]
        Dw3 = event_type_result[26]
        Up0 = event_type_result[27]
        Up1 = event_type_result[28]
        Up2 = event_type_result[29]
        Up3 = event_type_result[30]
        Pat = event_type_result[31]
        cur_peo_bus = event_type_result[32]
        total_weight = event_type_result[33]
        cargo_weight = event_type_result[34]
        disk_name = event_type_result[35]
        file_name = event_type_result[36]
        duration = event_type_result[37]
        slat = event_type_result[38]
        slong = event_type_result[39]
        mile = event_type_result[40]
        event_type= event_type_result[41]
        alarm_st = event_type_result[42]
        alarm_et = event_type_result[43]

        device_date_time = gps_result[0]
        location_type = gps_result[1]
        acquisition_time = gps_result[2]
        direction_in_degree = gps_result[3]
        satellite = gps_result[4]
        speed = gps_result[5]
        altitude = gps_result[6]
        positioning_accuracy = gps_result[7]
        lat = gps_result[8]
        lon = gps_result[9]
        x_acceleration =  gps_result[10]
        y_acceleration =  gps_result[11]
        z_acceleration =  gps_result[12]
        tilt =  gps_result[13]
        impact = gps_result[14]
        ignition = gps_result[15]
        break_1 =  gps_result[16]
        turn_left = gps_result[17]
        turn_right = gps_result[18]
        forward = gps_result[19]
        backward = gps_result[20]
        left_front_door = gps_result[21]
        right_front_door = gps_result[22]
        left_middle_door = gps_result[23]
        right_middle_door = gps_result[24]
        left_back_door = gps_result[25]
        right_back_door = gps_result[26]
        mobile_network = gps_result[27]
        gps_module = gps_result[28]
        WIFI_module = gps_result[29]
        G_sensor =  gps_result[30]
        recording_status = gps_result[31]
        fuel_consumption = gps_result[32]
        balance_fuel = gps_result[33]
        gsm_signal = gps_result[34]
        network_type_temp = gps_result[35]
        signal_intensity = gps_result[36]
        network_address = gps_result[37]
        gateway = gps_result[38]
        subnet_mask = gps_result[39]
        hard_disk_name = gps_result[40]
        hard_disk_status = gps_result[41]
        hard_disk_size = gps_result[42]
        hard_disk_balance = gps_result[43]
        video_loss_channel = gps_result[44]
        motion_detection =  gps_result[45]
        video_blind_channel = gps_result[46]
        alarm_input_trigger = gps_result[47]
        in_vehicle_temperature = gps_result[48]
        outside_of_vehicle_temperature = gps_result[49]
        motor_temperature = gps_result[50]
        device_temperature = gps_result[51]
        in_vehicle_humidity = gps_result[52]
        outside_of_vehicle_humidity = gps_result[53]
        total_mileage = gps_result[54]
        current_day_mileage = gps_result[55]
        i_button_number = gps_result[56]
        accumulated_mileage = gps_result[57]
        cumulative_fuel_consumption = gps_result[57]
        instant_fuel_consumption = gps_result[59]
        vehicle_voltage = gps_result[60]
        engine_speed = gps_result[61]
        obd_speed = gps_result[62]
        intake_air_flow = gps_result[63]
        intake_pressure = gps_result[64]
        coolant_temperature = gps_result[65]
        intake_air_temperature = gps_result[66]
        engine_load = gps_result[67]
        throttle_position = gps_result[68]
        remaining_oil = gps_result[69]
        engine_status = gps_result[70]
        engine_on_time = gps_result[71]
        engineOffTime = gps_result[72]
        idling_status = gps_result[73]
        hc = gps_result[74]

        ha = event_type_result[20]
        hb = event_type_result[21]
        voltage = event_type_result[22]

        low_Battery_voltage = gps_result[77]
        driver_id = gps_result[79]
        driver_name = gps_result[80]
        bluetooth_status = gps_result[81]

        result.append((unit_no,unit_no, messageType, polling_mode, version, device_Network_Type,device_date_time,location_type,acquisition_time,
                       direction_in_degree,satellite,speed,altitude,positioning_accuracy, lat, lon, x_acceleration, y_acceleration, z_acceleration,
                       tilt, impact, ignition, break_1, turn_left, turn_right, forward, backward, left_front_door, right_front_door, left_middle_door,
                       right_middle_door, left_back_door, right_back_door, mobile_network, gps_module,WIFI_module, G_sensor, recording_status,
                       fuel_consumption, balance_fuel, gsm_signal, network_type_temp, signal_intensity, network_address, gateway, subnet_mask,
                       hard_disk_name, hard_disk_status, hard_disk_size, hard_disk_balance,video_loss_channel, motion_detection,video_blind_channel,alarm_input_trigger,
                       in_vehicle_temperature, outside_of_vehicle_temperature, motor_temperature, device_temperature, in_vehicle_humidity, outside_of_vehicle_humidity,
                       total_mileage, current_day_mileage, i_button_number,accumulated_mileage, cumulative_fuel_consumption, instant_fuel_consumption,
                       vehicle_voltage, engine_speed, obd_speed, intake_air_flow, intake_pressure, coolant_temperature, intake_air_temperature,
                       engine_load, throttle_position, remaining_oil, engine_status, engine_on_time, engineOffTime, idling_status, hc, ha, hb, low_Battery_voltage, voltage, driver_id, driver_name, bluetooth_status,
                       
                       alarm_st,alarm_et,ch,seat_belt, fuel_bar, panic,max_value, min_value, average_value,current_value,previous_value, over_speed, parking_time,status,oil_tank_capacity,
                       balance_fuel_capacity, swipe_card_type, swipe_card_info, DriverOrStudent_status,his_real_data, card_type,Dw0, Dw1, Dw2, Dw3, Up0, Up1,
                       Up2, Up3, Pat, cur_peo_bus, total_weight, cargo_weight, disk_name, file_name, duration, slat, slong, mile, event_type))


        try:
            self.database_manager.insert_records(result)
        except Exception as e:
            self.logging.log_data("gps_inserting_error", f'Error While getting into insert record: {str(e)}')


        try:
            self.current_history_insert.current_history_inserting(unit_no, lat, lon, device_date_time, driver_id, polling_mode, ignition, speed,direction_in_degree, gps_module, voltage)
        except Exception as e:
            self.logging.log_data("current_history_insert_error", f'Error While getting into insert record: {str(e)}')

        


if __name__=="__main__":
    process_data = AlarmDataProcessor()
    unit_no = "91006"
    messageType = "1051"
    version = "V1"
    device_Network_Type = "4G"
    json_hex_data = "7b22646574223a7b22617667223a2230222c2264726964223a22222c22647572223a22313539222c226d6178223a2230222c226d696c65223a2230222c22736c6174223a2233332e393139323737222c22736c6e67223a223133302e373938303139227d2c22647475223a22323032332d31312d30312032303a35333a3538222c226563223a22373638222c226574223a22323032332d31312d30312032303a35333a3538222c227374223a22323032332d31312d30312032303a35313a3139222c2275756964223a22227d"
    gps_hex_data = "170B0114353AAF070101170B0114353A5F0400001900260082514E070021B76A08000701000300010000000300000000001F00010103010F00000805000001000180B90300000000000F000000F0000000000000003F000000000000000000000001004A0A060082120200"
    process_data.alarm_process_service_data(unit_no,json_hex_data, gps_hex_data.lower(), messageType, version, device_Network_Type) 
