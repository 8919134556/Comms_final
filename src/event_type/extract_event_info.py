import json

class ExtractEventInfo:
    def __init__(self):
        pass

    def extract_event_info(self, json_data):
        alarm_description = json_data.get('det', {})
        event_type = json_data.get('ec', '')
        start_time = json_data.get('st', '')
        end_time = json_data.get('et', '')

        # Initializing variables
        start_time = start_time or None
        end_time = end_time or None
        polling_mode = ""
        seat_belt = 0
        fuel_bar = 0
        panic = 0
        max_value = 0
        min_value = 0
        average_value = 0
        current_value = 0
        previous_value = 0
        over_speed = 0
        parking_time = ""
        status = ""
        oil_tank_capacity = ""
        balance_fuel_capacity = ""
        swipe_card_type = ""
        swipe_card_info = ""
        DriverOrStudent_status = ""
        data = ""
        card_type = ""
        ha = ""
        hb = ""
        voltage = ""
        Dw0 = Dw1 = Dw2 = Dw3 = Up0 = Up1 = Up2 = Up3 = Pat = cur_peo_bus = 0
        total_weight = ""
        cargo_weight = ""
        disk_name = ""
        file_name = ""
        ch = " "
        duration = slat = slong = ""
        mile = ""
        
        if event_type in ["0", "1", "2", "3"]:
            ch = alarm_description.get('ch', '')
            event_types_map = {"0": "unknown alert", "1": "video lost", "2": "motion detection", "3": "video blind"}
            polling_mode = f"{event_types_map[event_type]} {'start' if not end_time else 'end'}"
        elif event_type == "4":
            polling_mode, fuel_bar, seat_belt = self.get_input_trigger_mode(alarm_description)
        elif event_type == "5":
            polling_mode = "panic {'start' if not end_time else 'end'}"
            panic = 1
        elif event_type in ["6", "7", "8", "9"]:
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            alarm_type = "low" if event_type in ["8", "9"] else "over" if event_type in ["6", "7"] else " "
            sensor_type = self.get_sensor_type(alarm_description.get('num', ''))
            alarm_event = "speed" if event_type in ["6", "7"] else "temperature"
            polling_mode = f"{sensor_type} {alarm_type} {alarm_event} {'start' if not end_time else 'end'}"
            if event_type == "7":
                over_speed = 1
        elif event_type == "11":
            parking_time = alarm_description.get('vt', '')
            polling_mode = f"parking overtime {'start' if not end_time else 'end'}"
        elif event_type == "12":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            direction = int(alarm_description.get('dt', ''))
            direction_mapping = {
                1: "x_accel", 2: "y_accel", 3: "z_accel", 4: "impact",
                5: "tilt", 6: "turn", 7: "Harsh acceleration", 8: "harsh braking"
            }
            polling_mode = f"{direction_mapping.get(direction, 'Unknown')} {'start' if not end_time else 'end'}"
        elif event_type in ["13", "14"]:
            status_mapping = {
                "0": "ENTER", "1": "LEAVE", "2": "over speed alarm", "3": "over speed warning",
                "4": "low speed alarm", "5": "low speed warning", "6": "forbidden parking engine star",
                "7": "forbidden parking engine off", "8": "overtime stay in geo_fence",
                "9": "Pre-entry", "10": "Pre-exit"
            }
            status = status_mapping.get(alarm_description.get('st', ''), "")
            alarm_event = "GEO fencing" if event_type == "13" else "electronic route"
            polling_mode = f"{alarm_event} {'start' if not end_time else 'end'}"
        elif event_type == "15":
            ch = alarm_description.get('ch', '')
            num = alarm_description.get('num', '')
            st = alarm_description.get('st', '')
            door_status = "CLOSE" if st == "0" else "OPEN" if st == "1" else ""
            door_type = {"2": "front", "3": "mid", "4": "back"}.get(num, "")
            polling_mode = f"{door_type} door {door_status}"
        elif event_type == "16":
            status_mapping = {"0": "LOSS", "1": "BROKEN", "2": "CANNOT OVERWRITE", "3": "WRITE BLOCK FAIL",
                              "4": "DISK BROKEN", "5": "MOUNT_FAILURE", "6": "TOO_MANY_BAD_BLOCKS",
                              "7": "INVALID_BLOCK", "8": "PAUSED_WRITE", "9": "RECORDING_EXCEPTION",
                              "10": "NO_RECORDING", "11": "SLOW_WRITE"}
            status = status_mapping.get(alarm_description.get('st', ''), "AVAILABLE")
            polling_mode = f"storage abnormal {'start' if not end_time else 'end'}"
            disk_name = alarm_description.get('num', '')
        elif event_type == "17":
            polling_mode = f"fatigue driving {'start' if not end_time else 'end'}"
        elif event_type == "18":
            oil_tank_capacity = int(alarm_description.get('to', ''))
            balance_fuel_capacity = int(alarm_description.get('fr', ''))
            alarmType = alarm_description.get('dt', '')
            fuel_status = "Refuel" if alarmType == "1" else "Fuel theft" if alarmType == "2" else "Unknown"
            polling_mode = f"fuel {fuel_status} {'start' if not end_time else 'end'}"
        elif event_type == "19":
            polling_mode = f"illegal ACC off {'start' if not end_time else 'end'}"
        elif event_type == "20":
            polling_mode = f"GPS module abnormal {'start' if not end_time else 'end'}"
        elif event_type == "21":
            polling_mode = "front panel {'open' if not end_time else 'close'}"
        elif event_type == "22":
            tp = alarm_description.get('tp', '')
            swipe_card_type = {"1": "driver", "2": "Student", "3": "invalid card"}.get(tp, "")
            onboard_off_board = alarm_description.get('up', '')
            DriverOrStudent_status = "Onboard" if onboard_off_board == "1" else "Off_board" if onboard_off_board == "2" else "invalid"
            history = alarm_description.get('ht', '')
            data = "Historical data" if history == "1" else "Realtime data" if history == "2" else "invalid"
            it = alarm_description.get('it', '')
            swipe_card_info = alarm_description.get('cn', '')
            card_type_mapping = {"0": "RF_ID", "1": "i-button", "2": "face_recognition", "3": "i-button+face_recognition"}
            card_type = card_type_mapping.get(it, "")
            polling_mode = f"swipe card {'start' if not end_time else 'end'}"
        elif event_type == "23":
            polling_mode = f"i-button {'start' if not end_time else 'end'}"
        elif event_type == "24":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            polling_mode = f"ha {'start' if not end_time else 'end'}"
            ha = 1
        elif event_type == "25":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            polling_mode = f"ha {'start' if not end_time else 'end'}"
            hb = 1
        elif event_type == "26":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            polling_mode = f"low_speed warn {'start' if not end_time else 'end'}"
        elif event_type == "27":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            polling_mode = f"over_speed warn {'start' if not end_time else 'end'}"
        elif event_type == "28": 
            dt = int(alarm_description.get('dt', ''))
            voltage = int(alarm_description.get('cur', ''))
            voltage_mapping = {
                1: "low voltage", 2: "high voltage", 3: "Power off", 4: "Power on",
                5: "Power off when moving", 6: "Low voltage shutdown", 7: "Start up"
            }
            polling_mode = voltage_mapping.get(dt, "")
        elif event_type == "29":  
            Dw0 = int(alarm_description.get('dw0', ''))
            Dw1 = int(alarm_description.get('dw1', ''))
            Dw2 = int(alarm_description.get('dw2', ''))
            Dw3 = int(alarm_description.get('dw3', ''))
            Up0 = int(alarm_description.get('up0', ''))
            Up1 = int(alarm_description.get('up1', ''))
            Up2 = int(alarm_description.get('up2', ''))
            Up3 = int(alarm_description.get('up3', ''))
            Pat = int(alarm_description.get('pat', ''))
            Va = int(alarm_description.get('va', ''))
            cur_peo_bus = int(alarm_description.get('cur', ''))
            tm = alarm_description.get('tm', '')
            polling_mode = f"People Counting {'start' if not end_time else 'end'}"
        elif event_type == "30":
            tp = int(alarm_description.get('tp', ''))
            adas_events = {
                2: "Lane Change", 17: "Front Collision", 18: "Head Way Monitoring", 33: "Driver Fatigue",
                34: "Mobile Phone Usage", 35: "Smoking Alerts", 36: "Driver Distraction", 65: "Eye closed",
                66: "Yawning", 67: "Camera cover", 69: "Seat belt not closed", 70: "No driver",
                71: "Liquid Drinking"
            }
            polling_mode = adas_events.get(tp)
        elif event_type == "31":
            polling_mode = f"illegal ACC on {'start' if not end_time else 'end'}"
        elif event_type == "32":
            max_value, min_value, average_value, current_value, previous_value = self.extract_values(alarm_description)
            polling_mode = f"idle {'start' if not end_time else 'end'}"
        elif event_type == "33":
            polling_mode = f"Gps antenna break {'start' if not end_time else 'end'}"
        elif event_type == "34":
            polling_mode = f"Gps antenna short {'start' if not end_time else 'end'}"
        elif event_type == "35":
            polling_mode = f"IO output {'start' if not end_time else 'end'}"
        elif event_type == "36":
            polling_mode = f"CAN Bus connection abnormal {'start' if not end_time else 'end'}"
        elif event_type == "37":
            polling_mode = f"Towing {'start' if not end_time else 'end'}"
        elif event_type == "38":
            polling_mode = f"Free wheeling {'start' if not end_time else 'end'}"
        elif event_type == "39":
            polling_mode = f"RPM exceeds {'start' if not end_time else 'end'}"
        elif event_type == "40":
            polling_mode = f"Vehicle Move {'start' if not end_time else 'end'}"
        elif event_type == "41":
            polling_mode = "Trip start"
        elif event_type == "42":
            polling_mode = "In trip"
        elif event_type == "43":
            polling_mode = "Trip ends"
        elif event_type == "44":
            polling_mode = f"GPS location recover {'start' if not end_time else 'end'}"
        elif event_type == "45": 
            polling_mode = f"Video abnormal {'start' if not end_time else 'end'}"
        elif event_type == "46": 
            polling_mode = f"None trip position {'start' if not end_time else 'end'}"
        elif event_type == "47": 
            polling_mode = f"Main unit anomaly {'start' if not end_time else 'end'}"
        elif event_type == "48": 
            polling_mode = f"Excessive over_speed {'start' if not end_time else 'end'}"
        elif event_type == "49": 
            total_weight = alarm_description.get('tw', '')
            cargo_weight = alarm_description.get('gw', '')
            polling_mode = "load alarm" if not end_time else "Excessive over_speed end"
        elif event_type == "768":
            average_value = alarm_description.get('avg', '')
            max_value = alarm_description.get('max', '')
            duration = alarm_description.get('dur', '')
            slat = alarm_description.get('slat', '')
            slong = alarm_description.get('slng', '')
            mile = alarm_description.get('mile', '')
            polling_mode = "Trip notification" if not end_time else "Trip notification end"
        elif event_type == "769":
            polling_mode = "Tire pressure notification" if not end_time else "Tire pressure notification end"
        elif event_type == "770":
            disk_name = alarm_description.get('num', '')
            polling_mode = "Disk detection" if not end_time else "Disk detection end"
        elif event_type in ["1280", "1281", "1282", "1283"]:
            file_type = alarm_description.get('ft', '') 
            file_name = alarm_description.get('fn', '') 
            file_size = alarm_description.get('fs', '')
            file_type_mapping = {
                "0": "unknown", "1": "general recording", "2": "alarm recording",
                "3": "general snapshot file", "4": "alarm snapshot file",
                "5": "upgrade file", "6": "log file", "7": "Configuration file",
                "8": "Black box file", "9": "Visible alarm video/snapshot"
            }
            polling_mode = file_type_mapping.get(file_type, "")
        else:
            polling_mode = "Unknown"

        result = (polling_mode, ch, seat_belt, fuel_bar, panic, max_value, min_value, average_value,
                current_value, previous_value, over_speed, parking_time, status, oil_tank_capacity,
                balance_fuel_capacity, swipe_card_type, swipe_card_info, DriverOrStudent_status, data, card_type, ha, hb, voltage,
                Dw0, Dw1, Dw2, Dw3, Up0, Up1, Up2, Up3, Pat,cur_peo_bus, total_weight, cargo_weight, disk_name, file_name, duration, slat, slong, mile, event_type, start_time, end_time)

        return  result
    def extract_values(self, alarm_description):
        max_value = int(alarm_description.get('max', ''))
        min_value = int(alarm_description.get('min', ''))
        average_value = int(alarm_description.get('avg', ''))
        current_value = int(alarm_description.get('cur', ''))
        previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
        return max_value, min_value, average_value, current_value, previous_value

    def get_input_trigger_mode(self, alarm_description):
        num = alarm_description.get('num', '')
        ch = alarm_description.get('ch', '')
        trigger_modes = {
            "0": ("close", 0, 0),
            "1": ("Emergency/ Panic", 0, 0),
            "2": ("F-door open", 1 if ch == "2" else 0, 1 if ch == "3" else 0),
            "3": ("M-door open", 1 if ch == "2" else 0, 1 if ch == "3" else 0),
            "4": ("B-door open", 1 if ch == "2" else 0, 1 if ch == "3" else 0),
            "5": ("Near light", 0, 0),
            "6": ("Far light", 0, 0),
            "9": ("R-Turn (right turn)", 0, 0),
            "10": ("L-Turn (left turn)", 0, 0),
            "11": ("Braking", 0, 0),
            "12": ("Reverse", 0, 0),
            "13": ("Reserved 1", 0, 0),
            "14": ("F-door close", 0, 0),
            "15": ("M-door close", 0, 0),
            "16": ("B-door close", 0, 0),
            "17": ("Talk (start the intercom)", 0, 0),
            "18": ("Raise up", 0, 0),
            "19": ("Airtight", 0, 0),
            "20": ("load", 0, 0),
            "22": ("Custom defines", 0, 0),
            "23": ("Safe to load", 0, 0),
            "31": ("IBT2", 0, 0)
        }
        return trigger_modes.get(num, ("Unknown", 0, 0))

    def get_sensor_type(self, num):
        sensor_types = {"0": "CPU", "1": "HDD", "2": "cabin"}
        return sensor_types.get(num, "")


if __name__ == "__main__":
    process_data = ExtractEventInfo()
    json_data = {
        "det": {
        "ch": "1"
        },
        "dtu": "2018-09-14 14:31:07",
        "ec": "2",
        "et": "",
        "pa": "",
        "st": "2018-09-14 14:31:07"
    }
    result = process_data.extract_event_info(json_data)
    print(result)
