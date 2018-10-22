import datetime as dt
from datetime import datetime
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine('sqlite:///hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

# Query the table to find the latest date and derive an year old date
last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
last_date = datetime.strptime(last, '%Y-%m-%d')
year_ago = last_date - dt.timedelta(days=365)

@app.route("/")
def home():
    return (
        f"Available Routes<br/>"
        f"<br/>"        
        f"Precipitation Data<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations Data<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Stations Data<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max and Avg Temperature from a given date<br/>"
        f"/api/v1.0/start_date <--Replace 'start_date' with a date in 'YYYY-MM-DD' format<br/>"
        f"<br/>"
        f"Min, Max and Avg Temperature between 2 dates<br/>"
        f"/api/v1.0/start_date/end_date <--Replace 'start_date' and 'end_date' with dates in 'YYYY-MM-DD' format<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    sel = [Station.station,Station.name]
    active_stations = session.query(*sel).all()
    return jsonify(active_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago.strftime('%Y-%m-%d')).all()
    precipitation_data = []
    for result in results:
        precipitation_dict = {}
        precipitation_dict[result.date] = result.prcp
        precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago.strftime('%Y-%m-%d')).all()
    tempObs_data = []
    for result in results:
        tempObs_dict = {}
        tempObs_dict[result.date] = result.tobs
        tempObs_data.append(tempObs_dict)
    return jsonify(tempObs_data)

@app.route("/api/v1.0/<start>")
def tempStart(start):
    startDate = dt.datetime.strptime(start, "%Y-%m-%d")

    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    temp_data = session.query(*sel).\
        filter(Measurement.date >= startDate.strftime("%Y-%m-%d")).all()

    temp_dict = {}
    temp_dict["Average Temperature"] = temp_data[0][2]
    temp_dict["Minimum Temperature"] = temp_data[0][0]
    temp_dict["Maximum Temperature"] = temp_data[0][1]

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    startDate = dt.datetime.strptime(start, "%Y-%m-%d")
    endDate = dt.datetime.strptime(end, "%Y-%m-%d")

    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    temp_data = session.query(*sel).\
        filter(Measurement.date >= startDate.strftime("%Y-%m-%d")).\
        filter(Measurement.date <= endDate.strftime("%Y-%m-%d")).all()

    temp_dict = {}
    temp_dict["Average Temperature"] = temp_data[0][2]
    temp_dict["Minimum Temperature"] = temp_data[0][0]
    temp_dict["Maximum Temperature"] = temp_data[0][1]

    return jsonify(temp_dict)

if __name__ == "__main__":
    app.run()
