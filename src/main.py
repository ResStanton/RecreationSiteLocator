# Import modules
import flask

# Import database related items
from database import Database, CONNECTION_STRING


# Setup flask application
app = flask.Flask("Recreation Site Locator")

# Setup database connection
db = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")


# Create basic home page
@app.route('/')
def home_page():
    # Search bar setup
    search_input = {
        "search_filter": "", 
        "search_type": "", 
        "query": ""
        }
  
    search_input["search_filter"]=flask.request.args.get("filter_type", "")
    search_input["search_type"]=flask.request.args.get("search_type", "")
    search_input["query"]=flask.request.args.get("search", "")
    print(search_input)

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
    if search_input["search_filter"] != "":
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

    # Render the main page with points and search input passed in
    return flask.render_template(
        "main_page.html",
        search_input=search_input,
        search_types=search_types,
        search_filters=search_filters,
        markers=markers
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