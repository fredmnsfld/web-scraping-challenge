
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os
 

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_info = mongo.db.mars_info

    temp = scrape_mars.scrape_mars_news()

    mars_data = {
        'news_title' : temp['news_title'],
        'news_paragraph' : temp['news_paragraph'],
        'feat_image_url' : scrape_mars.scrape_mars_image(),
        'data' : scrape_mars.scrape_mars_facts(),
        'hemi_image_urls' : scrape_mars.scrape_mars_hemispheres()

    }
    #mars_data = scrape_mars.scrape_mars_news()
    #mars_data = scrape_mars.scrape_mars_image()
    #mars_data = scrape_mars.scrape_mars_facts()
    #mars_data = scrape_mars.scrape_mars_hemispheres()

    mars_info.update({}, mars_data, upsert=True)
    
    print(mars_data)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)