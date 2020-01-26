import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# TODO: Remove the CORS line before submitting final version!
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

sys.path.append('models')
sys.path.append('algorithm')
from fields import *
from field_cluster import *
from eta2010 import *
from eta2011 import *
from eta2012 import *
from eta2013 import *
from eta2014 import *
from eta2015 import *
from eta2016 import *
from eta2017 import *
from eta2018 import *

@app.route("/")
def hello():
    return "Hello Cruel World!"

@app.route("/api/fields")
def get_all_field_data():
    try:
        allFields = Field.query.all()
        for e in allFields:
            e.set_centroid()
        alg(allFields)
        return jsonify([e.serialize() for e in allFields])
    except Exception as e:
        return (str(e))

@app.route("/api/fields/<id_>")
def get_field_by_id(id_):
    try:
        field = Field.query.filter_by(id=id_).first()
        return jsonify(field.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/api/eta/<year_>")
def get_ETa_data_by_year(year_):
    try:
        switcher = { 
            2010: ETa2010.query.all(), 
            2011: ETa2011.query.all(), 
            2012: ETa2012.query.all(),  
            2013: ETa2013.query.all(), 
            2014: ETa2014.query.all(),
            2015: ETa2015.query.all(),
            2016: ETa2016.query.all(),
            2017: ETa2017.query.all(),
            2018: ETa2018.query.all(),
        } 
        yearlyETadata = switcher.get(year_, "Error: No records for specified year.")
        return jsonify([e.serialize() for e in yearlyETadata])
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()



