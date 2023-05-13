# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import pandas as pd
import numpy as np
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
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

# 1.
@app.route("/")
def homepage():
    # """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"Last Year Precipitation<br/>"
        f"/api/v1.0/precipitation:<br>"
        f"<br/>"
        f"Most Active Station<br/>"
        f"/api/v1.0/stations:<br/>"
        f"<br/>"
        f"Most Active Station Analysis<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"<br/>"
        f"Min, Max, & Avg<br/>"
        f"/api/v1.0/<start>:<br/>"
        f"<br/>"
        f"Start & End Dates<br/>"
        f"/api/v1.0/<start>/<end>")

# 2.
@app.route("/api/v1.0/precipitation")
def precipitaion():
    # Calculate the date one year from the last date in data set.
    last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # last_date

    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(Measurement.date, Measurement.prcp).filter \
    (Measurement.date >= last_date). \
    order_by(Measurement.date.desc()).all()

    # Save the query results as a Pandas DataFrame and set the index to the date column
    score_df = pd.DataFrame(scores, columns=['Date', 'Participation']) \
    .set_index('Date')

    # Sort the dataframe by date
    date_score_df = score_df.sort_values(by='Date')
    # date_score_df

    # Converting into a dictionary
    precipitation = []

    for date, prec in date_score_df:
        prec_dict = {}
        prec_dict["Date"] = date
        prec_dict["Prec"] = prec[0]

        
        precipitation.append(prec_dict)
        
    session.close
    return jsonify(precipitation)

# 3.
@app.route("/api/v1.0/stations")
def stations():
    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    best_stations = session.query(Measurement.station, func.count(Measurement.station)). \
        group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
        # best_stations
        # Converting into a dictionary
    pop_stations = []

    for result in stations:
        station_dict = {}
        station_dict["Date"] = stations[0][0]
          
        pop_stations.append(station_dict)
            
    session.close
    return jsonify(station_dict)

# 4.
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set.
    last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    best_stations = session.query(Measurement.station, func.count(Measurement.station)). \
        group_by(Measurement.station). \
        order_by(func.count(Measurement.station).desc()).all()
        # best_stations

    # Using the most active station id from the previous query, 
    # calculate the lowest, highest, and average temperature.

    most_active = best_stations[0][0]

    active_statation_temp = session.query(func.min(Measurement.tobs), \
                                          func.max(Measurement.tobs), \
                                            func.avg(Measurement.tobs)). \
                                            filter(most_active == Measurement.station).all()
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    active_last_year_temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(Measurement.date >= last_date).\
        order_by(Measurement.date).all()

    # Converting into a dictionary
    tobs_stations = []

    for result in active_last_year_temps:
        tobs_dict = {}
        tobs_dict["station"] = result[0]
        tobs_dict["date"] = result[1]
        tobs_dict["tobs"] = result[2]

        
        tobs_stations.append(tobs_dict)
        
    session.close
    return jsonify(tobs_dict)

# 5.
@app.route("/api/v1.0/<start>")
def start(start, name=None):
    
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    start_time = session.query(func.min(Measurement.tobs), \
                               func.max(Measurement.tobs), \
                               func.avg(Measurement.tobs)). \
                                filter(Measurement.date >= start_date).\
                                    order_by(Measurement.date).all()

    start_tobs = []

    for result in start_tobs:
        start_df = {}
        start_df["Min Temp"] = result[0]
        start_df["Max Temp"] = result[1]
        start_df["Avg Temp"] = result[2]
        start_tobs.append(start_df)
    
    session.close
    return jsonify(start_df)

@app.route("/api/v1.0/<start>/<end>")
def start(start, end, name=None):
    
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    end_date = dt.date(2019, 8, 23) - dt.timedelta(days=365)
    
    end_time = session.query(func.min(Measurement.tobs), \
                             func.max(Measurement.tobs), \
                             func.avg(Measurement.tobs)). \
                                filter(Measurement.date >= start_date).\
                                    order_by(Measurement.date).all()

    end_tobs = []

    for result in end_tobs:
        end_df = {}
        end_df["Min Temp"] = result[0]
        end_df["Max Temp"] = result[1]
        end_df["Avg Temp"] = result[2]
        end_tobs.append(end_df)
    
    session.close
    return jsonify(end_df)

# Debugging
if __name__ == "__main__":
    app.run(debug=True)