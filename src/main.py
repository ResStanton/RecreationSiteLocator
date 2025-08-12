# Import modules
import flask

# Import database related items
from database import Database, CONNECTION_STRING
import geolocate


# Setup flask application
app = flask.Flask("Recreation Site Locator")

# Setup database connection
db = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")


# Create basic home page
@app.route('/')
def home_page():
    # create error variable in case an error needs to be displayed 
    error = ""

    # Search bar setup
    search_input = {
        "search_filter": "", 
        "search_type": "", 
        "query": ""
        }
  
    # Populate search input
    search_input["search_filter"]=flask.request.args.get("filter_type", "")
    search_input["search_type"]=flask.request.args.get("search_type", "")
    search_input["query"]=flask.request.args.get("search", "")

    # The types of searches for the dropdown 
    # Dropdown options
    search_types = [
        {"id": "Name", "display": "Name"},
        {"id": "Address", "display": "Address"},
    ]

    # Populate filters dropdown
    location_types = db.get_unique_location_types()
    location_types.remove(None)  # Remove the location type for now
    search_filters = []

    # loop through all location types for to create the filter
    for location_type in location_types:
        search_filters.append({"id": location_type, "display": location_type})

    if search_input["search_type"] == "Address":
        try:
            address_location = geolocate.get_location_from_address(search_input["query"])
        except AttributeError:
            error = r"That Address Could Not Be Found.\nMake sure yoy spelled everything correctly and try again.\nAlso try removing the city from the address"
        except TimeoutError:
            error = r"Request Timed Out.\nPlease try again later."
        else:
            print(address_location)
        locations = db.query_all()
    else:
        # Determine what query to use 
        if search_input["query"] and search_input["search_filter"]:
            # Search by name while filtering by activity type
            locations = db.query_name_and_activity_type(search_input["query"], search_input["search_filter"])
        elif search_input["query"]:
            locations = db.query_by_name(search_input["query"])
        elif search_input["search_filter"]:
            # Code for searching by activity selected in search bar
            locations = db.query_by_activity_type(search_input["search_filter"])
        else:
            # Get all locations from the database
            locations = db.query_all()
    
    # loop thought locations to skip broken data and only include the required data 
    markers = []
    for loc in locations:
        try:
            coords = loc['geometry']['coordinates']  # formatted in a list as [lon, lat]
            name = loc['properties']['RECAREANAME']
            markers.append({
                'name': name,
                'lat': coords[1],
                'lon': coords[0]
            })
        except TypeError: # if data is broken and is missing one of the felids, skip
            continue
        except KeyError: # Skip any broken enteries for now
            print(loc['properties']['RECAREANAME'])

    # Render the main page with points and search input passed in
    return flask.render_template(
        "main_page.html",
        search_input=search_input,
        search_types=search_types,
        search_filters=search_filters,
        markers=markers,
        error=error
    )


@app.route('/location', methods=['POST'])
def location():
    # get data from javascript
    raw_data = flask.request.json
    latitude = raw_data['lat']
    longitude = raw_data['lng']

    # get location from database
    location = db.query_latitude_longitude(latitude, longitude)

    # pass only useful data back to javascript
    properties = location["properties"]
    location_information = {
        "name": properties["RECAREANAME"],
        "activity": properties["MARKERACTIVITY"],
        "activity_group": properties["MARKERACTIVITYGROUP"],
        "description": properties["RECAREADESCRIPTION"],
        "hours": properties["OPERATIONAL_HOURS"],
        "fees": properties["FEEDESCRIPTION"],
        "restrictions": properties["RESTRICTIONS"],
        "reservations": properties["RESERVATION_INFO"]
        }
    
    # replace any missing data with notice
    if location_information["hours"] is None:
        location_information["hours"] = "<i>No hours listed.</i>"
    if location_information["fees"] is None:
        location_information["fees"] = "<i>No fee listed.</i>"
    if location_information["restrictions"] is None:
        location_information["restrictions"] = "<i>No restrictions listed.</i>"
    if location_information["reservations"] is None:
        location_information["reservations"] = "<i>No reservation requirements listed.</i>"

    return flask.jsonify(location_information)


# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
    db.close() # by closing the database here, it should close after flask closes