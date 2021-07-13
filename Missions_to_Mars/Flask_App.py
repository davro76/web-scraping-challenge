from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
#create an instance of flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


#route to render index.html template using data from mongo
@app.route("/")
def index():
    #find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    #return template and data
    return render_template("index.html", mars=mars)

#route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    #run the scrape function
    update_data=scrape_mars.scrape()
    #update the mongo database using update and upsert=True
    mongo.db.mars.update({},update_data,upsert=True)
    #redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)