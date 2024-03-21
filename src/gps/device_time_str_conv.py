
class DeviceTime():
    def __init__(self):
        pass
    def hex_str_date_time(self, data):
        i_year = int(data[:2], 16)
        i_month = int(data[2:4], 16)
        i_day = int(data[4:6], 16)
        i_hour = int(data[6:8], 16)
        i_minute = int(data[8:10], 16)
        i_second = int(data[10:12], 16)
        device_date_time = f"{i_year + 2000}-{i_month:02d}-{i_day:02d} {i_hour:02d}:{i_minute:02d}:{i_second:02d}"
        return device_date_time


if __name__=="__main__":
    process_date_time = DeviceTime()
    hex_date_value = "170209092604"
    date_time = process_date_time.hex_str_date_time(hex_date_value)
    print(date_time)