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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
    
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


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(measurement.station).group_by(measurement.station).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)


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



@app.route(f"/api/v1.0/<start>")
def start(start):
    start = dt.datetime(start)
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=start)
    filter(measurement.station=='USC00519281').all()
    session.close()

    start = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    start = datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.strptime(end, "%Y-%m-%d").date()
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=start).\
    filter(measurement.date<=end)
    filter(measurement.station=='USC00519281').all()
    session.close()

    tobs = list(np.ravel(results))
    return jsonify(tobs)

if __name__ == '__main__':
    app.run(debug=True)
