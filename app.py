from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# 1. import Flask
from flask import Flask, request, render_template, session, redirect, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




measure_df = pd.read_sql_query('select * from Measurement where date > "2016-08-22"', con=engine)
measure_df = measure_df.dropna(how='any')

meas_date = measure_df

prcp_df = pd.DataFrame([meas_date['prcp'], meas_date['date']])


out = prcp_df.to_dict()
prcp_dict = out
p_dict = {}
for entry in prcp_dict:
    p_dict.update({prcp_dict[entry]['date'] : prcp_dict[entry]['prcp']})
#ok = prcp_dict.tojson(orient='index')

######Creat dict for temp json

temp_df = pd.DataFrame(measure_df['tobs'])
temp_df.index = measure_df['date']
temp_df

t_dict = temp_df.to_dict()
t_dict = t_dict['tobs']
t_dict

glon = "hello there"

qb_date = ""
qe_date = ""
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

####DATA FRAME EXAMPLE
# 3. Define what to do when a user hits the index route
#@app.route('/', methods=("POST", "GET"))
#def html_table():
#    return render_template('index.html',  tables=[measure_df.to_html(classes='data')], titles='measure_df.columns.values')
    #return render_template('index.html',  tables=[measure_df.to_html(classes='data')], titles='Precipitation')

# 3. Define what to do when a user hits the index route
@app.route('/', methods=("POST", "GET"))
def html_table():

#    return render_template('index.html',  tables=[measure_df.to_html(classes='data')], titles='measure_df.columns.values')
    #return (
        #f'Available Routes:<br/>'
        #f'<a href="/api/v1.0/stations">Stations</a><br/>'
        #f'<a href="/api/v1.0/tob">Observations</a><br/>'
        #f'<a href="/result">Enter Dates</a>'
        #f'<p>Maths <input type ="text" name = "Mathematics" /></p>'
    #)
    return render_template('index.html')
# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def about():
    print("Server received request for 'API' page...")
    return jsonify(p_dict)
    #return ok


@app.route("/api/v1.0/tob")
def stations():
    print("Server received request for 'API' page...")
    return jsonify(t_dict)
    #return ok

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
        result = request.form
        qb_date = result['b_date']
        qe_date = result['e_date']
        if qe_date == "":
            if qe_date == "" and qb_date == "":
                return ("You need to enter a date")
            measure_df = pd.read_sql_query(f'select * from Measurement where date > "{qb_date}"', con=engine)
        if qb_date == "":
            measure_df = pd.read_sql_query(f'select * from Measurement where date < "{qe_date}"', con=engine)
        else:
            measure_df = pd.read_sql_query(f'select * from Measurement where date between "{qb_date}" and "{qe_date}"', con=engine)
            #y = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                #filter(Measurement.date >= qb_date).filter(Measurement.date <= qe_date).all()
        #measure_df = measure_df.dropna(how='any')
        temp_max = measure_df.groupby('station')['tobs'].max()
        temp_min = measure_df.groupby('station')['tobs'].min()
        temp_avg = measure_df.groupby('station')['tobs'].mean()
        temp_df = pd.DataFrame(list(zip(temp_max, temp_min, temp_avg)), columns=['Max', 'Min', 'Average'], index=temp_min.index)
        t_dict = temp_df.to_dict(orient='index')
        t_json = temp_df.to_json(orient='records')
        #return render_template("display.html",result = t_json)
        #return print(calc_temps('2015-01-01', '2016-01-01'))
        return jsonify(t_dict)


if __name__ == "__main__":
    app.run(debug=True)