import numpy as np

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"For the precipitation: /api/v1.0/precipitation<br/>"
        f"For stations: /api/v1.0/stations<br/>"
        f"Temperatures from 1 year ago: /api/v1.0/tobs<br/>"
        f"Min, Avg, and Max temperatures since a certain date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Min, Avg, and Max temperatures in a date range (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()


    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)
  
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    year_ago = dt.date(latest_date.year -1, latest_date.month, latest_date.day)
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()
   

    session.close()
 
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    temp_all = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min
        temp_dict['Average Temperature'] = avg
        temp_dict['Maximum Temperature'] = max
        temp_all.append(temp_dict)

        return jsonify(temp_all)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temp_all = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min
        temp_dict['Average Temperature'] = avg
        temp_dict['Maximum Temperature'] = max
        temp_all.append(temp_dict)

        return jsonify(temp_all)

if __name__ == '__main__':
    app.run(debug=True)