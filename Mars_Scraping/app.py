#The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
#The second line says we'll use PyMongo to interact with our Mongo database.
#The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# first line tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
#second line is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

#The code we create next will set up our Flask routes: one for the main HTML page everyone will view when visiting the web app, and one to actually scrape new data using the code we've written.
#define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
    app.run()