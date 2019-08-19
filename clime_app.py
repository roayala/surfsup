# Step 2 - Climate App
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.\
# Use FLASK to create your routes.
# Routes
# /
# Home page.
# List all routes that are available.

# /api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

# /api/v1.0/tobs
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.




# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def index():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)


    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()


    dictionary = []
    for date, prcp in results:
        mesasure = {}
        mesasure["date"] = date
        mesasure["precipitation"] = prcp
        dictionary.append(mesasure)

    return jsonify(dictionary)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.station).all()

    session.close()
    
    #return statement
    
    stations = []
    for station in results:
        stations.append(station)
        
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)


    lastdate = str(session.query(Measurement.date).order_by(Measurement.date.desc()).first())[2:][:-3]
    lastdate = dt.datetime.strptime(lastdate, '%Y-%m-%d')
    delta = lastdate - dt.timedelta(days=365)
    
    lastYear = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= delta).all()

    session.close()
    
    year_temps = []
    for date, temp in lastYear:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temp
        year_temps.append(temp_dict)
        
    return jsonify(year_temps)

@app.route("/api/v1.0/<start>")
def dateinfo(start):
    
\
    session = Session(engine)
 
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = str(lastdate)
    lastdate = lastdate[2:]
    lastdate = lastdate[:-3]
    
    result = calc_temps_with_session(start, lastdate, session)
    
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def datestartend(start, end):
    session = Session(engine)

    result = calc_temps_with_session(start, end, session)
    
    return jsonify(result)
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)