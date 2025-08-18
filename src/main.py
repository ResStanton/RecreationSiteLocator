# Import modules
import flask

# Import database related items
from database import Database, CONNECTION_STRING
import geolocate

# Setup flask application
app = flask.Flask("Recreation Site Locator")

# Setup database connection
db = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")

def get_data_from_search(search_input):
    # setup variables
    locations = []
    error = ""

    # query the data according to the search
    if search_input["query"] and search_input["search_filter"]:   # query for combined data
        # use query according to search type
        if search_input["search_type"] == "Address":
            # Search for an address with a filter
            address_location, error = geolocate.get_location_from_address(search_input["query"])
            if not error: # if no errors occurred
                locations = db.activity_type_and_query_near_location(address_location["longitude"], address_location["latitude"], search_input["search_filter"])
        else: # search_type == "name"
            # Search by name while filtering by activity type
            locations = db.query_name_and_activity_type(search_input["query"], search_input["search_filter"])
    elif search_input["query"]:  # query for only the search text
        # use query according to search type
        if search_input["search_type"] == "Address":
            # Get coordinates and any errors from the address entered in the search bar 
            address_location, error = geolocate.get_location_from_address(search_input["query"])
            if not error: # if no errors occurred
                locations = db.query_near_location(address_location["longitude"], address_location["latitude"])
        else:  # search_type == "name"
            locations = db.query_by_name(search_input["query"])
    elif search_input["search_filter"]:  # query for only the filter
        # Code for searching by activity selected in search bar
        locations = db.query_by_activity_type(search_input["search_filter"])
    else:  # No query of filter is given, query all data
        # Get all locations from the database
        locations = db.query_all()

    # return locations and any error messages
    return locations, error


# Create basic home page
@app.route('/')
def home_page():
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
    search_filters = []

    # loop through all location types for to create the filter
    for location_type in location_types:
        search_filters.append({"id": location_type, "display": location_type})

    # query the data according to the search
    locations, error = get_data_from_search(search_input)

    # loop thought locations to skip broken data and only include the required data 
    markers = []
    for loc in locations:
        try:
            coords = loc['geometry']['coordinates']  # formatted in a list as [lon, lat]
            name = loc['properties']['RECAREANAME']
            markers.append({
                'name': name,
                'lat': coords[1],
                'lon': coords[0],
                'id': str(loc['_id'])
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


def is_missing_information(info: str):
    """Returns true if the info given actually contains information"""
    return not (info and info != "<br />")


@app.route('/location', methods=['POST'])
def location():
    # get data from javascript
    raw_data = flask.request.json
    location_id = raw_data["id"]

    # get location from database
    location = db.query_id(location_id)

    # pass only useful data back to javascript
    properties = location["properties"]
    location_information = {
        "name": properties["RECAREANAME"],
        "activity": properties["MARKERACTIVITY"],
        "activity_group": properties["MARKERACTIVITYGROUP"],
        "description": properties["RECAREADESCRIPTION"].replace(".css", ""),
        "hours": properties["OPERATIONAL_HOURS"],
        "fees": properties["FEEDESCRIPTION"],
        "restrictions": properties["RESTRICTIONS"],
        "reservations": properties["RESERVATION_INFO"]
        }
    
    # replace any missing data with notice
    if is_missing_information(location_information["name"]):
        location_information["name"] = "<i>No name listed</i>"
    if is_missing_information(location_information["activity"]):
        location_information["activity"] = ""
    if is_missing_information(location_information["description"]):
        location_information["description"] = "<i>No description listed</i>"
    if is_missing_information(location_information["hours"]):
        location_information["hours"] = "<i>No hours listed.</i>"
    if is_missing_information(location_information["fees"]):
        location_information["fees"] = "<i>No fee listed.</i>"
    if is_missing_information(location_information["restrictions"]):
        location_information["restrictions"] = "<i>No restrictions listed.</i>"
    if is_missing_information(location_information["reservations"]):
        location_information["reservations"] = "<i>No reservation requirements listed.</i>"

    return flask.jsonify(location_information)


# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
    db.close() # by closing the database here, it should close after flask closes