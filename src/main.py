# Import modules
import flask

# Setup flask application 
app = flask.Flask("Recreation Site Locator")

# create basic home page
@app.route('/', methods=['GET', 'POST'])
def home_page():
    # The search input dictionary that is passed to the HTML to set the search bar to what was searched
    search_input = {
        "search_filter": "", 
        "search_type": "", 
        "query": ""
        }
    
    # The types of searches for the dropdown 
    search_types = [
        {"id": "Name", "display": "Name"},
        {"id": "Address", "display": "Address"},
    ]

    # The types of filters for the dropdown
    # Same format as search_type 
    search_filters = [
        {"id": "Camping & Cabins", "display": "Camping & Cabins"},
        {"id": "Trailhead", "display": "Trail head"},
        {"id": "Scenic Driving", "display": "Scenic Driving"},
        {"id": "Picnicking", "display": "Picnicking"},
    ]

    # Render the template
    return flask.render_template("main_page.html", search_input=search_input, search_types=search_types, search_filters=search_filters)

# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
