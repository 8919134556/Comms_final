from hex_converter import HexConverter
from db_inserting import DatabaseManager
from logger import Logger
from device_time_str_conv import DeviceTime
from status_context_bit import StatusContextBit
from location_info import LocationInfo
from g_sensor import GSensor
from basic_status import BasicStatus
from communication_module import CommunicationModule
from fuel_consumption import FuelConsumption
from mobile_network import MobileNetwork
from wifi_network import WifiNetwork
from hard_disk import HardDisk
from alarm_status import AlarmStatus
from temperature_status import TemperatureStatus
from statistics_data import StatisticsStatus
from i_button import IButton
from obd_info import OBDInfo
from voltage_status import VoltageStatus
from driver_status import DriverStatus
from bluetooth import BluetoothStatus
from current_history_data_inserting import CurrentHistoryInsert


class GpsDataProcessor:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.database_manager = DatabaseManager()
        self.logging = Logger()
        self.device_time = DeviceTime()
        self.status_context_bit = StatusContextBit()
        self.location_info = LocationInfo()
        self.g_sensor = GSensor()
        self.basic_status = BasicStatus()
        self.communication_module = CommunicationModule()
        self.fuel_consumption = FuelConsumption()
        self.mobile_network = MobileNetwork()
        self.wifi_network = WifiNetwork()
        self.hard_disk = HardDisk()
        self.alarm_status = AlarmStatus()
        self.temperature_status = TemperatureStatus()
        self.statistics_status = StatisticsStatus()
        self.i_button = IButton()
        self.obd_info = OBDInfo()
        self.voltage_status = VoltageStatus()
        self.driver_status = DriverStatus()
        self.bluetooth_status = BluetoothStatus()
        self.current_history_insert = CurrentHistoryInsert()
        

    def process_gps_service_data(self, unit_no, messageType, polling_mode, hex_data, version, device_Network_Type):
        result = []
        unit_no = unit_no
        messageType = messageType
        polling_mode = polling_mode
        version = version
        device_Network_Type = device_Network_Type
        header = hex_data[:8] # 48014110
        length = hex_data[8:16]# e1000000
        ss_id_len = hex_data[16:18] # 25
        ss_id_len = int(ss_id_len, 16) # result 37
        ss_id_len = (ss_id_len*2) + 2 # "(37*2) + 2 = 76"
        ss_no = hex_data[16:16 + ss_id_len] # 2561376161626462362d643433612d343737362d616661652d36626437663461373832666300
        ss_id_no = self.hex_converter.convert_hex_to_ascii(ss_no)
        hex_data = hex_data[16 + ss_id_len :] # 170209092604aff70000170209092604750300009b00170071c1a90800169f1c05000700000000000000000000010000001f00000103010b0000000000000110010d8e0e00000000000f00000006000000000000003f000000000000000000000001009efb010000000000012c000000000000000000000000000000000000000000000000000000002302081542590000000000000000000000020200e204000017323333333333333334343434343434352c626c61636b000100
        deviceTime = hex_data[:12] # 170209092604
        device_date_time = self.device_time.hex_str_date_time(deviceTime)
        status_context_bit_identifier = hex_data[12:16] #aff7
        status_context_bit = self.status_context_bit.hex_bit_status_context(status_context_bit_identifier) # "1111010111101111"
        content_data_pos = 16
        

        # location info
        if status_context_bit[0:1] == "1":
            location_info_bit_identifier = hex_data[content_data_pos:content_data_pos+52] # 0000170209092604750300009b00170071c1a90800169f1c0500, bit length is 52
            location = self.location_info.hex_bit_location_info(location_info_bit_identifier)
            content_data_pos = content_data_pos+52
        else:
            location = [None, None, None, None, None, None, None, None, None]

            
        # G-sensor
        if status_context_bit[1:2] == "1":
            g_sensor_bit_identifier = hex_data[content_data_pos:content_data_pos+22] # 0700000000000000000000, bit length is 22
            g_sensor = self.g_sensor.hex_bit_g_sensor(g_sensor_bit_identifier)
            content_data_pos = content_data_pos+22
        else:
            g_sensor = [None, None, None, None, None]
        
        # basic status
        if status_context_bit[2:3] == "1": 
            basic_status_bit_identifier = hex_data[content_data_pos:content_data_pos+8] # 01000000, bit length is 8
            basic_status = self.basic_status.hex_bit_basic_status(basic_status_bit_identifier)
            content_data_pos = content_data_pos+8
        else:
            basic_status = [None, None, None, None, None, None, None, None, None, None, None, None]
        
        # communication module working status
        if status_context_bit[3:4] == "1":
            module_bit_identifier = hex_data[content_data_pos:content_data_pos+16] # 1f00000103010b00, bit length is 16
            communication_module =  self.communication_module.hex_bit_communication_module(module_bit_identifier)
            content_data_pos = content_data_pos+16
        else:
            communication_module = [None, None, None, None, None]
            
        # fuel consumption status
        if status_context_bit[4:5] == "1":
            fuel_consumption_bit_identifier = hex_data[content_data_pos:content_data_pos+10] # Fuel consumption status does not exist, so no data here., bit length is 10
            fuel_consumption_data = self.fuel_consumption.hex_bit_fuel_consumption(fuel_consumption_bit_identifier)
            content_data_pos = content_data_pos+10
        else:
            fuel_consumption_data = [None, None]
        
        # mobile network status
        if status_context_bit[5:6] == "1":
            mobile_network_status_bit_identifier = hex_data[content_data_pos:content_data_pos+10] # 0000000000, bit length is 8
            mobile_network_status = self.mobile_network.hex_bit_mobile_network(mobile_network_status_bit_identifier)
            content_data_pos = content_data_pos+10
        else:
            mobile_network_status= [None, None]
        
        # WIFI network status
        if status_context_bit[6:7] == "1":
            wifi_network_status_bit_identifier = hex_data[content_data_pos:content_data_pos+30] # WIFI network: Wi-Fi module not exist, so no data here, bit length is 30 and N of bits
            wifi_network =  self.wifi_network.hex_bit_wifi_network(wifi_network_status_bit_identifier)
            ssid_length = wifi_network[4]
            content_data_pos = content_data_pos+30
            SSID_length = ssid_length * 2
            SSID_bit = hex_data[content_data_pos : content_data_pos + SSID_length]
            SSID = self.hex_converter.convert_hex_to_ascii(SSID_bit)
            content_data_pos = content_data_pos + SSID_length
        else:
            wifi_network = [None, None, None, None, None]
        
        # hard disk status
        if status_context_bit[7:8] == "1":
            position = 0
            hard_disk_status_bit_identifier = self.hard_disk.hex_bit_size(hex_data[content_data_pos:content_data_pos+2]) # 0110010d8e0e0000000000, bit length is 22
            content_data_pos = content_data_pos+2
            for i in range(len(hard_disk_status_bit_identifier)):
                if hard_disk_status_bit_identifier[i] == '1':
                    position += 20
            con = hex_data[content_data_pos : content_data_pos+position]
            hard_disk_status_data = self.hard_disk.hex_bit_hard_disk(hard_disk_status_bit_identifier, con)
            content_data_pos = content_data_pos+position
        else:
            hard_disk_status_data = [None, None, None, None]

        # alarm status
        if status_context_bit[8:9] == "1":
            alarm_status_bit_identifier = hex_data[content_data_pos:content_data_pos+24] # 0f0000000600000000000000, bit length is 24
            alarm_status = self.alarm_status.hex_bit_alarm_status(alarm_status_bit_identifier)
            content_data_pos = content_data_pos+24
        else:
            alarm_status = [None, None, None, None]
        
        # temperature and humidity status
        if status_context_bit[9:10] == "1":
            temp_bit_identifier = hex_data[content_data_pos:content_data_pos+24] # 3f0000000000000000000000, bit length is 24
            temperature_status = self.temperature_status.hex_bit_temperature_status(temp_bit_identifier)
            content_data_pos = content_data_pos+24
        else:
            temperature_status = [None, None, None, None, None, None]

        # Statistics data 
        if status_context_bit[10:11] == "1":
            statistics_data_bit_identifier = hex_data[content_data_pos:content_data_pos+20] # 01009efb010000000000, bit length is 20
            statistics_data =  self.statistics_status.hex_bit_statistics_status(statistics_data_bit_identifier)
            content_data_pos = content_data_pos+20
        else:
            statistics_data = [None, None]
        
        # i-button
        if status_context_bit[11:12] == "1":
            i_button_bit_identifier = hex_data[content_data_pos:content_data_pos+4] # I-button info: data not exist, so no data here. and bit length is 4 and N of bits
            i_button_length = self.i_button.hex_bit_i_button(i_button_bit_identifier)
            content_data_pos = content_data_pos+4
            i_button_bit = hex_data[content_data_pos : content_data_pos + i_button_length]
            i_button_number = self.hex_converter.convert_hex_to_ascii(i_button_bit)
            content_data_pos = content_data_pos + i_button_length
        else:
            i_button_number = None

        # OBD info
        if status_context_bit[12:13] == "1":
            obd_status_bit_identifier = hex_data[content_data_pos:content_data_pos+6] # 012c000000000000000000000000000000000000000000000000000000002302081542590000000000000000000000, Length N of bits
            length_of_package = self.obd_info.hex_bit_obd_info(obd_status_bit_identifier)
            length_of_package = length_of_package[1]
            signal_package_data = hex_data[content_data_pos+6:content_data_pos+6+length_of_package]
            obd_signal_packet_data = self.obd_info.obd_signal_packet_data(signal_package_data)
            content_data_pos = content_data_pos+6+length_of_package
        else:
            obd_signal_packet_data = [None, None, None, None, None, None, None, None, None, None, None, None,None, None, None, None, None, None, None, None, None]

        # Voltage Status
        if status_context_bit[13:14] == "1":
            voltage_status_bit_identifier = hex_data[content_data_pos:content_data_pos+6] # 020200e2040000, length is N of bits
            voltage_length_of_package = self.voltage_status.hex_bit_voltage_status(voltage_status_bit_identifier)
            voltage_package_data = hex_data[content_data_pos+6:content_data_pos+6+voltage_length_of_package]
            voltage = self.voltage_status.voltage_signal_packet_data(voltage_package_data)
            content_data_pos = content_data_pos+6+voltage_length_of_package
        else:
            voltage = ""

        # driver status
        if status_context_bit[14:15] == "1":
            driver_status_bit_identifier = hex_data[content_data_pos:content_data_pos+2] # 17323333333333333334343434343434352c626c61636b00
            driver_status_length = self.driver_status.hex_bit_driver_status(driver_status_bit_identifier)
            driver_status_bit = hex_data[content_data_pos+2:content_data_pos+2+driver_status_length]
            driver = self.driver_status.driver_signal_packet_data(driver_status_bit)
            content_data_pos = content_data_pos+2+driver_status_length
        else:
            driver = [None, None]
        
        # Bluetooth
        if status_context_bit[15:16] == "1":
            bluetooth_status_bit_identifier = hex_data[content_data_pos:content_data_pos+2]
            bluetooth_status_length = self.bluetooth_status.hex_bit_bluetooth_status(bluetooth_status_bit_identifier)
            bluetooth_status_data = hex_data[content_data_pos+2:content_data_pos+2+bluetooth_status_length]
            bluetooth_status = int(bluetooth_status_data, 16)
        else:
            bluetooth_status = None
        
        location_type = location[0]
        acquisition_time = location[1]
        direction_in_degree = location[2]
        satellite = location[3]
        speed = location[4]
        altitude = location[5]
        positioning_accuracy = location[6]
        lon = location[7]
        lat = location[8]
        x_acceleration =  g_sensor[0]
        y_acceleration =  g_sensor[1]
        z_acceleration =  g_sensor[2]
        tilt =  g_sensor[3]
        impact = g_sensor[4]
        ignition = basic_status[0] 
        break_1 =  basic_status[1] 
        turn_left = basic_status[2]
        turn_right = basic_status[3] 
        forward = basic_status[4]
        backward = basic_status[5] 
        left_front_door = basic_status[6]
        right_front_door = basic_status[7]
        left_middle_door = basic_status[8]
        right_middle_door = basic_status[9]
        left_back_door = basic_status[10]
        right_back_door = basic_status[11] 
        mobile_network = communication_module[0]
        gps_module = communication_module[1]
        WIFI_module = communication_module[2]
        G_sensor =  communication_module[3]
        recording_status = communication_module[4]
        fuel_consumption = fuel_consumption_data[0]
        balance_fuel = fuel_consumption_data[1]
        gsm_signal = mobile_network_status[0]
        network_type_temp = mobile_network_status[1]
        signal_intensity = wifi_network[0]
        network_address = wifi_network[1]
        gateway = wifi_network[2]
        subnet_mask = wifi_network[3]
        hard_disk_name = hard_disk_status_data[0]
        hard_disk_status = hard_disk_status_data[1]
        hard_disk_size = hard_disk_status_data[2]
        hard_disk_balance = hard_disk_status_data[3]
        video_loss_channel = alarm_status[0]
        motion_detection =  alarm_status[1]
        video_blind_channel = alarm_status[2]
        alarm_input_trigger = alarm_status[3]
        in_vehicle_temperature = temperature_status[0]
        outside_of_vehicle_temperature = temperature_status[1]
        motor_temperature = temperature_status[2]
        device_temperature = temperature_status[3]
        in_vehicle_humidity = temperature_status[4]
        outside_of_vehicle_humidity = temperature_status[5]
        total_mileage = statistics_data[0]
        current_day_mileage = statistics_data[1]
        i_button_number = i_button_number
        accumulated_mileage = obd_signal_packet_data[0]
        cumulative_fuel_consumption = obd_signal_packet_data[1]
        instant_fuel_consumption = obd_signal_packet_data[2]
        vehicle_voltage = obd_signal_packet_data[3]
        engine_speed = obd_signal_packet_data[4]
        obd_speed = obd_signal_packet_data[5]
        intake_air_flow = obd_signal_packet_data[6]
        intake_pressure = obd_signal_packet_data[7]
        coolant_temperature = obd_signal_packet_data[8]
        intake_air_temperature = obd_signal_packet_data[9]
        engine_load = obd_signal_packet_data[10]
        throttle_position = obd_signal_packet_data[11]
        remaining_oil = obd_signal_packet_data[12]
        engine_status = obd_signal_packet_data[13]
        engine_on_time = obd_signal_packet_data[14]
        engineOffTime = obd_signal_packet_data[15]
        idling_status = obd_signal_packet_data[16]
        hc = obd_signal_packet_data[17]
        ha = obd_signal_packet_data[18]
        hb = obd_signal_packet_data[19]
        low_Battery_voltage = obd_signal_packet_data[20]
        voltage = voltage
        driver_id = driver[0]
        driver_name = driver[1]
        bluetooth_status = bluetooth_status
        ec = None
        alarm_st = None
        alarm_et = None
        ch = None
        seat_belt = None
        fuel_bar = None
        panic = None
        max_value = None
        min_value = None
        average_value = None
        current_value = None
        previous_value = None
        over_speed = None
        parking_time = None
        status = None
        oil_tank_capacity = None
        balance_fuel_capacity = None
        swipe_card_type = None
        swipe_card_info = None
        DriverOrStudent_status = None
        his_real_data = None
        card_type = None
        Dw0 = None
        Dw1 = None
        Dw2 = None
        Dw3 = None
        Up0 = None
        Up1 = None
        Up2 = None
        Up3 = None
        Pat = None
        cur_peo_bus = None
        total_weight = None
        cargo_weight = None
        disk_name = None
        file_name = None
        duration = None
        slat = None
        slong = None
        mile= None


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
                       
                       alarm_st, alarm_et,ch,seat_belt, fuel_bar, panic,max_value, min_value, average_value,current_value,previous_value, over_speed, parking_time,status,oil_tank_capacity,
                       balance_fuel_capacity, swipe_card_type, swipe_card_info, DriverOrStudent_status,his_real_data, card_type,Dw0, Dw1, Dw2, Dw3, Up0, Up1,
                       Up2, Up3, Pat, cur_peo_bus, total_weight, cargo_weight, disk_name, file_name, duration, slat, slong, mile, ec))
        
        try:
            self.database_manager.insert_records(result)
        except Exception as e:
            self.logging.log_data("alarm_inserting_error", f'Error While getting into insert record: {str(e)}')
        
        try:
            self.current_history_insert.current_history_inserting(unit_no, lat, lon, device_date_time, driver_id, polling_mode, ignition, speed,direction_in_degree, gps_module, voltage)
        except Exception as e:
            self.logging.log_data("current_history_insert_error", f'Error While getting into insert record: {str(e)}')

        

if __name__=="__main__":
    process_data = GpsDataProcessor()
    unit_no = "75340"
    messageType = "1041"
    polling_mode = "Testing"
    version = "V1"
    bit_data = "48014110e10000002561376161626462362d643433612d343737362d616661652d366264376634613738326663001803160c0f30af0f00011803160c0f309e08190090030a004d064005000c051a090007ffff0000000000000100010000001f000101000107000006050000010001eaed0000000000000f00000008000000000000003f000000000000000000000001001e0000000000000002113031453934423143303130303030394100"
    device_Network_Type = "4G" 
    process_data.process_gps_service_data(unit_no, messageType, polling_mode, bit_data, version, device_Network_Type) 