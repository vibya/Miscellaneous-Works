from flask import Flask, jsonify, render_template
from mission_to_mars import scrape
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import time

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars

@app.route("/")
def home():
    marsInfo = db.mars.find_one()
    if marsInfo == None:
        return render_template("index0.html")
    return render_template("index.html", marsInfo=marsInfo)

@app.route("/scrape")
def mars_scrape():
    collection.drop()
    mars_info = scrape()
    collection.insert_one(mars_info)
    return home()

if __name__ == "__main__":
    app.run()