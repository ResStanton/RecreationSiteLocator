# Import libraries
import geopy.exc
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Static variables 
USER_AGENT = "cit440a_recreation_site_locator"
TIMEOUT = 7

NOT_FOUND_ERROR = r"That Address Could Not Be Found.\nMake sure yoy spelled everything correctly and try again.\nAlso try removing the city from the address"
TIMEOUT_ERROR = r"Request Timed Out.\nPlease try again later."

# Configure and create locator object
geopy.geocoders.options.default_user_agent = USER_AGENT
geopy.geocoders.options.default_timeout = TIMEOUT
_locator = Nominatim()

# Use the rate limiter to safely abide by the "No heavy uses" requirement of the Nominatim Usage Policy
# https://operations.osmfoundation.org/policies/nominatim/
safe_geocode = RateLimiter(_locator.geocode, min_delay_seconds=2)

def get_location_from_address(address: str) -> dict:
    """
    Get the geospacial location of an written address

    Arguments: address: str The address to get the location of

    Returns: 
        The longitude and latitude in a dictionary {"longitude": float "latitude": float}
        An error message string if an error occurred. If no error an empty string.  
    """
    error = ""
    try:
        # try and get the location from the address
        location = safe_geocode(address)
    except geopy.exc.GeocoderTimedOut:
        # The lookup timed out. Pass the error message to the main application
        error = TIMEOUT_ERROR
        return {}, error
    # make sure the lookup was successful 
    if location is None:
        # The lookup must have failed. Pass the error message to the main application
        error = NOT_FOUND_ERROR
        return {}, error

    # An location was found. Return the longitude and latitude
    return {"longitude": location.longitude, "latitude": location.latitude}, error

if __name__ == "__main__":
    print(get_location_from_address("11147 Pikes Peak Drive Parker"))

