# Import the dependencies
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with = engine)

# Assign the measurement class to a variable called `Measurement`
# Reflect the existing database into a new model

# Map the database tables to Python classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Initialize the Flask application
app = Flask(__name__)

# Helper function to get the most recent date in the dataset
def get_most_recent_date():
    session = Session(engine)
    recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    session.close()
    return dt.datetime.strptime(recent_date_str, "%Y-%m-%d")

# Helper function to convert date strings to datetime objects
def convert_date(date_str):
    return dt.datetime.strptime(date_str, "%Y-%m-%d")

# Helper function to find the most active station
def get_most_active_station():
    session = Session(engine)
    active_station = session.query(Measurement.station, func.count(Measurement.station).label("count")) \
                            .group_by(Measurement.station) \
                            .order_by(text("count DESC")) \
                            .first()[0]
    session.close()
    return active_station

# Helper function to format database query results for JSON response
def format_query_results(query_results):
    return [tuple(row) for row in query_results]

# Define the Flask routes

@app.route("/")
def home():
    return (
        f"<strong>Available Endpoints:</strong><br/>"
        f"<strong>Static Queries:</strong><br/>"
        f"&emsp;/api/v1.0/precipitation<br/>"
        f"&emsp;/api/v1.0/stations<br/>"
        f"&emsp;/api/v1.0/tobs<br/>"
        f"<strong>Dynamic Queries:</strong><br/>"
        f"&emsp;/api/v1.0/&lt;start&gt;<br/>"
        f"&emsp;/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"Date format: YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = get_most_recent_date()
    one_year_ago = recent_date - dt.timedelta(days=365)
    session = Session(engine)
    precipitation_data = session.query(Measurement.date, Measurement.prcp) \
                                .filter(Measurement.date > one_year_ago) \
                                .all()
    session.close()
    return jsonify(dict(precipitation_data))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_list = session.query(Station.station, Station.name).all()
    session.close()
    return jsonify(format_query_results(stations_list))

@app.route("/api/v1.0/tobs")
def temperature_observed():
    recent_date = get_most_recent_date()
    one_year_ago = recent_date - dt.timedelta(days=365)
    active_station = get_most_active_station()
    session = Session(engine)
    temperature_data = session.query(Measurement.date, Measurement.tobs) \
                              .filter(Measurement.date > one_year_ago) \
                              .filter(Measurement.station == active_station) \
                              .all()
    session.close()
    return jsonify(dict(temperature_data))

@app.route("/api/v1.0/<start>")
def temp_stats_from_start(start):
    start_date = convert_date(start)
    active_station = get_most_active_station()
    session = Session(engine)
    min_temp, max_temp, avg_temp = session.query(func.min(Measurement.tobs), 
                                                 func.max(Measurement.tobs), 
                                                 func.avg(Measurement.tobs)) \
                                          .filter(Measurement.station == active_station) \
                                          .filter(Measurement.date >= start_date) \
                                          .first()
    session.close()
    return jsonify(TMIN=f'{min_temp} F', TMAX=f'{max_temp} F', TAVG=f'{avg_temp} F')

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    start_date = convert_date(start)
    end_date = convert_date(end)
    active_station = get_most_active_station()
    session = Session(engine)
    min_temp, max_temp, avg_temp = session.query(func.min(Measurement.tobs), 
                                                 func.max(Measurement.tobs), 
                                                 func.avg(Measurement.tobs)) \
                                          .filter(Measurement.station == active_station) \
                                          .filter(Measurement.date >= start_date) \
                                          .filter(Measurement.date <= end_date) \
                                          .first()
    session.close()
    return jsonify(TMIN=f'{min_temp} F', TMAX=f'{max_temp} F', TAVG=f'{avg_temp} F')

# Run the application
if __name__ == "__main__":
    app.run()
    
