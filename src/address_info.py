from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from logger import Logger

class Geocoder:
    def __init__(self):
        self.logging = Logger()
        self.geolocator = Nominatim(user_agent="my-geocoding-app/1.0")

    def reverse_geocode_and_print_address(self, latitude, longitude, language=''):
        try:
            # Reverse geocode the coordinates with the specified language
            location = self.geolocator.reverse((latitude, longitude), language=language)
            return location.address
        except Exception as e:
            self.logging.log_data("address_info", f"Error processing Address data: {e}")
            return None

    def get_nearby_locations(self, center_latitude, center_longitude, radius=1000, language=''):
        try:
            # Find nearby locations based on the center coordinates
            nearby_locations = self.geolocator.reverse((center_latitude, center_longitude), language=language, exactly_one=False)

            # Filter locations within the specified radius
            filtered_locations = [location for location in nearby_locations if
                                geodesic((center_latitude, center_longitude),
                                        (location.latitude, location.longitude)).meters <= radius]

            # Extract street-level information from the results
            street_details = []
            for location in filtered_locations:
                street_data = location.raw.get('address', {}).get('road')
                if street_data:
                    street_details.append(street_data)

            return street_details[0]
        except Exception as e:
            self.logging.log_data("address_info", f"Error processing Address data: {e}")
            return None

if __name__ == "__main__":
    # Create an instance of the Geocoder class
    geocoder = Geocoder()

    # Example latitude and longitude coordinates
    latitude = 12.994225
    longitude = 77.57346

    # Input for language
    language = "en"

    # Check if language input is empty, use default 'en'
    if not language:
        language = 'en'

    # Reverse geocode the coordinates
    address = geocoder.reverse_geocode_and_print_address(latitude, longitude, language=language)

    # Print the address
    print("Reverse Geocoded Address:", address)

    # Get nearby street-level information
    nearby_streets = geocoder.get_nearby_locations(latitude, longitude, radius=2000, language=language)

    # Print nearby street-level information
    print("\nNearby Streets:")
    for idx, street in enumerate(nearby_streets, start=1):
        print(f"{idx}. {street}")
