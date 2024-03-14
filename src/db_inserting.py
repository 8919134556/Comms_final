import pyodbc
from configparser import ConfigParser
from threading import Lock
import datetime
from logger import Logger

class DatabaseManager:
    _instance = None
    _lock = Lock()
    
    def __init__(self):
        self.logging = Logger()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._connection = None
                cls._instance._cursor = None
                cls._instance.connect()
            return cls._instance

    def connect(self):
        try:
            if self._connection is None:
                config = ConfigParser()
                config.read('C:\\suryaanand\\daily-work\\09-03-2024\\MDVR-final\\GPS_1041\\src\\config.ini')  # Adjust the file path as needed
                driver = config.get('Database', 'driver')
                server = config.get('Database', 'server')
                database = config.get('Database', 'database')
                username = config.get('Database', 'username')
                password = config.get('Database', 'password')

                connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
                # Using connection pooling by adding 'Pooling=True' to the connection string
                self._connection = pyodbc.connect(connection_string + ';Pooling=True', autocommit=True)
                self._cursor = self._connection.cursor()
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error connecting to the database: {e}")

    def insert_records(self, records):
        """
        Bulk insert records into the database.
        
        Args:
            records (list): List of tuples, where each tuple represents a set of parameters for a record.
        """
        query = '''EXEC InsertIntoRawTable @unit_no = ?, @vehicle_no = ?, @messageType = ?, @polling_mode = ?, @version = ?,
                    @device_Network_Type = ?, @track_time = ?, @location_type = ?, @acquisition_time = ?, @direction_in_degree = ?,
                    @satellite = ?, @speed = ?, @altitude = ?, @positioning_accuracy = ?, @lat = ?, @lon = ?,  @x_acceleration = ?,
                    @y_acceleration = ?, @z_acceleration = ?, @tilt = ?, @impact = ?, @ignition = ?, @break_1 = ?, @turn_left = ?,
                    @turn_right = ?, @forward = ?, @backward = ?, @left_front_door = ?, @right_front_door = ?, @left_middle_door = ?,
                    @right_middle_door = ?, @left_back_door = ?, @right_back_door = ?, @mobile_network = ?, @gps_module = ?, @WIFI_module = ?,
                    @G_sensor = ?, @recording_status = ?, @fuel_consumption = ?, @balance_fuel = ?, @gsm_signal = ?, @network_type_temp = ?,
                    @signal_intensity = ?, @network_address = ?, @gateway = ?, @subnet_mask = ?, @hard_disk_name = ?, @hard_disk_status = ?,
                    @hard_disk_size = ?, @hard_disk_balance = ?, @video_loss_channel = ?, @motion_detection = ?, @video_blind_channel = ?,
                    @alarm_input_trigger = ?, @in_vehicle_temperature = ?, @outside_of_vehicle_temperature = ?, @motor_temperature = ?,
                    @device_temperature = ?, @in_vehicle_humidity = ?, @outside_of_vehicle_humidity = ?, @total_mileage = ?, @current_day_mileage = ?,
                    @i_button_number = ?, @accumulated_mileage = ?, @cumulative_fuel_consumption = ?, @instant_fuel_consumption = ?,
                    @vehicle_voltage = ?, @engine_speed = ?, @obd_speed = ?, @intake_air_flow = ?, @intake_pressure = ?, @coolant_temperature = ?,
                    @intake_air_temperature = ?, @engine_load = ?, @throttle_position = ?, @remaining_oil = ?, @engine_status = ?, @engine_on_time = ?,
                    @engineOffTime = ?, @idling_status = ?, @hc = ?, @ha = ?,@hb = ?, @low_Battery_voltage = ?, @voltage = ?, @driver_id = ?, @driver_name = ?,
                    @bluetooth_status = ?, @ec = ?, @alert_datetime = ?, @panic = ?, @fuel_bar = ?, @over_speed = ?, @seat_belt = ?,
                    @previous_value = ?, @tp = ?, @dt = ?, @Up0 = ?, @Dw0 = ?, @Up1 = ?, @Dw1 = ?, @tm = ?, @Va = ?, @Cur = ?, @Pat = ?;
            '''
        try:
            # Using executemany for bulk insertion
            self._cursor.executemany(query, records)
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error executing SQL query: {e}")
    
    def current_records(self, records):
        """
        Bulk insert records into the database.
        Args:
            records (list): List of tuples, where each tuple represents a set of parameters for a record.
        """
        query = '''EXEC UpsertGpsDataCurrent @VehicleID = ?, @ClientID = ?, @DriverRFID = ?, @VehicleNo = ?, 
                    @Unitno = ?, @pollingmode = ?, @tracktime = ?, @lat = ?, @lon = ?, @location = ?, @locationnearby = ?, @roadtype = ?, @ignition = ?, 
                    @speed = ?, @odometer = ?, @direction = ?, @gpsstatus = ?, @immobalizer = ?, @panic = ?, @mainpower = ?, 
                    @seatbelt = ?, @idleduration = ?, @stopduration = ?, @travelduration = ?, @ModifiedDate = ?, 
                    @ModifiedUserId = ?, @AlertInd = ?, @GEOFENCEID = ?'''
        try:
            # Using executemany for bulk insertion
            self._cursor.executemany(query, records)
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error executing SQL query at Current records: {e}")



    def history_records(self, records):
        """
        Bulk insert records into the database.
        
        Args:
            records (list): List of tuples, where each tuple represents a set of parameters for a record.
        """
        query = '''EXEC InsertIntoMdvrGpsDataHistory @VehicleID = ?, @ClientID = ?, @DriverRFID = ?, @VehicleNo = ?, 
                    @Unitno = ?, @pollingmode = ?, @tracktime = ?, @lat = ?, @lon = ?, @location = ?, @locationnearby = ?, @roadtype = ?, @ignition = ?, 
                    @speed = ?, @odometer = ?, @direction = ?, @gpsstatus = ?, @immobalizer = ?, @panic = ?, @mainpower = ?, 
                    @seatbelt = ?, @idleduration = ?, @stopduration = ?, @travelduration = ?, @ModifiedDate = ?, 
                    @ModifiedUserId = ?, @AlertInd = ?, @GEOFENCEID = ?'''

        try:
            # Using executemany for bulk insertion
            self._cursor.executemany(query, records)
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error executing SQL query at history records: {e}")
    
    

    def previous_records(self, unit_no):
        query = '''EXEC GetRowByUnitno @Unitno = ?'''
        try:
            # Using execute for a single set of parameters
            result_set = self._cursor.execute(query, unit_no).fetchall()
            # Check if there is at least one row in the result set
            if result_set:
                result_str = [str(value) for value in result_set[0]]
                return result_str
            else:
                return None  # No records found
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error executing SQL query at previous records: {e}")
    
    def get_records(self, unit_no):
        query = '''EXEC GetVehicleDetails @Unitno = ?'''
        try:
            # Using execute for a single set of parameters
            result_set = self._cursor.execute(query, unit_no).fetchall()
            # Check if there is at least one row in the result set
            if result_set:
                result_str = [str(value) for value in result_set[0]]
                return result_str
            else:
                return None  # No records found
        except pyodbc.Error as e:
            self.logging.log_data("DB_connection_error", f"Error executing SQL query at previous records: {e}")




# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Example data for bulk insertion
    records = [
        ("91006", "91006", 0, datetime.datetime.now(), 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, "testing", 65200, 0, 0, "0000", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "testing", "1G", datetime.datetime.now(), 0, 0, 0),
        # Add more records as needed
    ]

    db_manager.insert_records(records)
