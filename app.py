import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

last_date = dt.datetime(2017, 8, 23)
year = last_date - dt.timedelta(365)


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:"
        f""
        f"/api/v1.0/precipitation"
        f''
        f'/api/v1.0/stations'
        f''
        f'/api/v1.0/tobs'
        f''
        f'/api/v1.0/<start> and /api/v1.0/<start>/<end>'
        f'<start>= start date, <end = end date>'
    )


@app.route("/api/v1.0/precipitation")
def precipation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date<=last_date).\
        filter(measurement.date>=year).all()

    session.close()

    prcp = list(np.ravel(results))
    return jsonify(prcp)


# Precipitation

# Convert the query results to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(measurement.station).group_by(measurement.station).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.station, measurement.tobs).\
        filter(measurement.station=='USC00519281').\
        filter(measurement.date<=last_date).\
        filter(measurement.date>=year).all()

    session.close()

    tobs = list(np.ravel(results))
    return jsonify(tobs)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.


@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    results = session.query(measurement.station, func.count(measurement.prcp)).filter().all()
    session.close()

    start = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def tobs():
    session = Session(engine)
    results = session.query(measurement.station, func.count(measurement.prcp)).group_by(measurement.station).all()
    session.close()

    tobs = list(np.ravel(results))
    return jsonify(tobs)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

if __name__ == '__main__':
    app.run(debug=True)
