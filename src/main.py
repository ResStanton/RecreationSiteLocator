# Import modules
import flask

# Import other python files
import database

# Setup flask application
app = flask.Flask("Recreation Site Locator")

# create basic home page
@app.route('/')
def home_page():
    # The search input dictionary that is passed to the HTML to set the search bar to what was searched
    search_input = {
        "search_filter": "", 
        "search_type": "", 
        "query": ""
        }
  
    search_input["search_filter"]=flask.request.args.get("filter_type", "")
    search_input["search_type"]=flask.request.args.get("search_type", "")
    search_input["query"]=flask.request.args.get("search", "")
    print(search_input)
        
        # Pass the results
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
