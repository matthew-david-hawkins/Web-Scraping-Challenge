from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)

# The home route will display information from the scrape with the featured image as the background
@app.route("/")
def index():

    # Find last document in the collection
    doc_no = mongo.db.webpage.estimated_document_count()-1

    latest_scrape = mongo.db.webpage.find({})[doc_no]

    # Render the template with the latest scraped data
    return render_template("index.html", latest_scrape = latest_scrape)


# The /scrape route will call the scrape function, add the results of the scrape to the database, and redirect to the home page
@app.route("/scrape")
def scraper():
    
    # Define the collection to use
    collection = mongo.db.webpage
    
    # Get dictionary of scrape results
    webpage_data = scrape_mars.scrape()

    # Print feedback
    print("\n\n\n SCRAPE COMPLETE \n\n\n")
    
    # Insert the scrape results into the database
    collection.insert_one(webpage_data)

    # Redirect to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)