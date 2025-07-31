# Import modules
import flask

# Import database related items
from database import Database, CONNECTION_STRING


# Setup flask application
app = flask.Flask("Recreation Site Locator")

# Setup database connection
db = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")


# Create basic home page
@app.route('/', methods=['GET', 'POST'])
def home_page():
    # Search bar setup
    search_input = {
        "search_filter": "", 
        "search_type": "", 
        "query": ""
    }

    # Dropdown options
    search_types = [
        {"id": "Name", "display": "Name"},
        {"id": "Address", "display": "Address"},
    ]

    search_filters = [
        {"id": "Camping & Cabins", "display": "Camping & Cabins"},
        {"id": "Trailhead", "display": "Trail head"},
        {"id": "Scenic Driving", "display": "Scenic Driving"},
        {"id": "Picnicking", "display": "Picnicking"},
    ]

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
    data = flask.request.json
    print(data)
    return "YOU CLICKED THE POINT"


# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
    db.close() # by closing the database here, it should close after flask closes