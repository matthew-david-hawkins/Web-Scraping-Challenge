from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)

@app.route("/")
def index():
    latest_scrape = mongo.db.webpage.find_one()
    print(latest_scrape['news'])
    print(latest_scrape['featured_image'])
    print(latest_scrape['mars_weather'])
    #return render_template("index.html", listings=latest_scrape['news'])
    return render_template("index.html", latest_scrape = latest_scrape)


@app.route("/scrape")
def scraper():
    collection = mongo.db.webpage
    webpage_data = scrape_mars.scrape()
    print("\n\n\n SCRAPE COMPLETE \n\n\n")
    collection.update({}, webpage_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)