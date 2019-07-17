import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

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

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation within date range"""
    results_precip = engine.execute("SELECT date, prcp FROM Measurement WHERE date BETWEEN '2016-08-23' AND '2017-08-23'").fetchall()

    # Convert list of tuples into normal list
    precip_dict = dict(results_precip)

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""

    active_stations = session.query(Station.station).all()

    # Convert list of tuples into normal list    
    stations = list(np.ravel(active_stations))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temps within date range"""
    temps = engine.execute("SELECT date, tobs FROM Measurement WHERE date BETWEEN '2016-08-23' AND '2017-08-23'").fetchall()

    # Convert list of tuples into normal list
    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)


if __name__ == '__main__':
    app.run(debug=True)