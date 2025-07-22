# Import modules
import flask

# Setup flask application 
app = flask.Flask("Recreation Site Locator")

# create basic home page
@app.route('/')
def home_page():
    return flask.render_template("main_page.html")

# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
