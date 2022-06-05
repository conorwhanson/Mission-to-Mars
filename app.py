from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import pymongo
import scraping

app = Flask(__name__)

## connect to Mongo using PyMongo
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

## define app route to root page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars ## define variable that points to mongo db
    mars_data = scraping.scrape_all() # holds scraped data
    mars.update_one({}, {'$set':mars_data}, upsert=True) # updates the database with the newly scraped data
    return redirect('/', code=302)

if __name__ == "__main_":
    app.run(debug=True)