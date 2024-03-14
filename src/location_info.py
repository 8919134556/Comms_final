from hex_converter import HexConverter
from logger import Logger

class LocationInfo():
    def __init__(self):
        self.hex_converter = HexConverter()
        self.logging = Logger()

    def hex_bit_location_info(self, context):
        try:
            # Extracting information from the context
            location_info = context[0:2]
            location_info_bin = self.hex_converter.hex_to_binary(location_info, 16)
            location_info_bin = self.hex_converter.string_reverse_binary(location_info_bin)

            # Parsing location information
            if location_info_bin[0:1] == "0":
                direction = 0
            elif location_info_bin[0:1] == "1":
                direction = 1

            if location_info_bin[1:2] == "0":
                longitude_Mark = "East"
                longitude_Sign = ""
            elif location_info_bin[1:2] == "1":
                longitude_Mark = "West"
                longitude_Sign = "-"

            if location_info_bin[2:3] == "0":
                Altitude = "Above sea level"
            elif location_info_bin[2:3] == "1":
                Altitude = "lower than sea level"

            if location_info_bin[3:4] == "0":
                mileage_data_not_exist = "0"
            elif location_info_bin[3:4] == "1":
                mileage_data_exist = "1"

            if location_info_bin[4:5] == "0":
                latitude_mark = "North"
                latitude_Sign = ""
            elif location_info_bin[4:5] == "1":
                latitude_mark = "South"
                latitude_Sign = "-"

            # Extracting additional location information
            location_type = context[2:4]  # location type
            track_time_Temp = context[4:32]
            iYear1 = int(track_time_Temp[0:2], 16)
            iMonth1 = int(track_time_Temp[2:4], 16)
            iDay1 = int(track_time_Temp[4:6], 16)
            iHour1 = int(track_time_Temp[6:8], 16)
            iMinute1 = int(track_time_Temp[8:10], 16)
            iSecond1 = int(track_time_Temp[10:12], 16)
            acquisition_time = f"{iYear1 + 2000}-{iMonth1:02d}-{iDay1:02d} {iHour1:02d}:{iMinute1:02d}:{iSecond1:02d}"
            
            # Handling direction and speed
            direction_in_degree = int(context[16:18], 16)
            satellite = int(context[18:20], 16)
            if direction == 1:
                direction_in_degree = direction_in_degree + 180

            speed_temp = self.hex_converter.string_reverse(context[20:24])
            speed = int(speed_temp, 16) / 100

            # Extracting altitude and positioning information
            altitude = int(self.hex_converter.string_reverse(context[24:28]), 16)
            positioning_accuracy = int(self.hex_converter.string_reverse(context[28:32]), 16)
            Degree_of_longitude = int(context[32:34], 16)

            # Extracting longitude information
            Minute_of_longitude_temp = self.hex_converter.string_reverse(context[34:42])
            Minute_of_longitude = float(int(Minute_of_longitude_temp, 16)) / 10000 / 60
            lon = float(Degree_of_longitude + Minute_of_longitude)
            lonStr = longitude_Sign + str(lon)
            lon = float(lonStr)

            # Extracting latitude information
            Degree_of_latitude = int(context[42:44], 16)
            Minute_of_latitude_temp = self.hex_converter.string_reverse(context[44:52])
            Minute_of_latitude = float(int(Minute_of_latitude_temp, 16)) / 10000 / 60
            lat = float(Degree_of_latitude + Minute_of_latitude)
            latStr = latitude_Sign + str(lat)
            lat = float(latStr)

            # Creating result list
            result = [location_type, acquisition_time, direction_in_degree, satellite, speed, altitude, positioning_accuracy, lon, lat]
            return result

        except Exception as e:
            self.logging.log_data("location_info", f"Error processing GPS data: {e}")
            return None


if __name__ == "__main__":
    process_location_info = LocationInfo()
    context = "0000170209092604750300009b00170071c1a90800169f1c0500"
    status_location_info = process_location_info.hex_bit_location_info(context)

    if status_location_info is not None:
        print(status_location_info)
