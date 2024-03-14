import math
from logger import Logger

class OdometerCalculator:
    def __init__(self):
        self.logging = Logger()

    def calculate_distance(self, lat1, lon1, lat2, lon2, distance_previous):
        try:
            # If lat2 is None, return the DistancePrevious
            if lat2 is None:
                return distance_previous

            # If any of the latitudes or longitudes is 0.0, return the DistancePrevious
            if any(coord == 0.0 for coord in [lat1, lon1, lat2, lon2]):
                return distance_previous

            # If DistancePrevious is None, set it to 0
            if distance_previous is None:
                distance_previous = 0

            # Calculate tempdistance
            temp_distance = math.cos(math.radians(90 - lat1)) * math.cos(math.radians(90 - lat2)) + \
                            math.sin(math.radians(90 - lat1)) * math.sin(math.radians(90 - lat2)) * math.cos(
                                math.radians(lon1 - lon2))

            # If tempDistance > 1, set distance to 0
            if temp_distance > 1:
                distance = 0
            else:
                # Calculate distance
                distance = math.acos(temp_distance) * 6371

            # Change by kumar: If distance is less than 0.02, set distance to 0
            if distance < 0.02:
                distance = 0

            # If distance is greater than 100, set distance to 0
            if distance > 100:
                distance = 0

            # Update DistancePrevious and return the sum of DistancePrevious and distance
            distance_previous += distance
            return distance_previous
        except Exception as e:
            self.logging.log_data("static_status", f"Error processing GPS data: {e}")
            return None


if __name__ == "__main__":
    # Example usage:
    odometer = OdometerCalculator()
    result = odometer.calculate_distance(33.80362319946289, -117.98967742919922, 33.813621666666665, -117.99967833333333, 346.3)
    print(result)
