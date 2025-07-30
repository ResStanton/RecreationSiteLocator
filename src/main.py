# Import modules
import flask
from database import Database  # ✅ STEP 1: Import your DB class

# Setup flask application
app = flask.Flask("Recreation Site Locator")

# Your MongoDB connection string
CONNECTION_STRING = "mongodb+srv://PythonBacked:NJgAD1jRPc7j441F@cluster0.ykhbmhb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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

    # ✅ STEP 2: Connect to DB and get markers
    db = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")
    locations = db.query_all()
    db.close()

    markers = []
    for loc in locations:
        try:
            coords = loc['geometry']['coordinates']  # [lon, lat]
            name = loc['properties']['RECAREANAME']
            markers.append({
                'name': name,
                'lat': coords[1],
                'lon': coords[0]
            })
        except KeyError:
            continue

    # ✅ STEP 3: Pass markers to template
    return flask.render_template(
        "main_page.html",
        search_input=search_input,
        search_types=search_types,
        search_filters=search_filters,
        markers=markers  # <- you’ll use this in main_page.html
    )

# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
