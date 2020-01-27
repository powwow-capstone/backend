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

# @app.route("/api/fields/<id_>")
# def get_field_by_id(id_):
#     try:
#         field = Field.query.filter_by(id=id_).first()
#         return jsonify(field.serialize())
#     except Exception as e:
# 	    return(str(e))

@app.route("/api/eta")
def get_ETa_data_by_year_and_day():
    # nasty code lol
    try:
        year_ = request.args.get('year', '2010')
        day_ = request.args.get('day', '1')
        switcher = { 
            '2010': ETa2010.query.filter_by(dayofyear=day_).all(), 
            '2011': ETa2011.query.filter_by(dayofyear=day_).all(), 
            '2012': ETa2012.query.filter_by(dayofyear=day_).all(),  
            '2013': ETa2013.query.filter_by(dayofyear=day_).all(), 
            '2014': ETa2014.query.filter_by(dayofyear=day_).all(),
            '2015': ETa2015.query.filter_by(dayofyear=day_).all(),
            '2016': ETa2016.query.filter_by(dayofyear=day_).all(),
            '2017': ETa2017.query.filter_by(dayofyear=day_).all(),
            '2018': ETa2018.query.filter_by(dayofyear=day_).all(),
        } 
        yearlyETadata = switcher.get(year_, "Error: No records for specified year.")
        return jsonify([e.serialize() for e in yearlyETadata])
    except Exception as e:
        return (str(e))

# @app.route("/api/eta/2010_temp")
# def get_field():
#     try:
#         yearlyETadata = ETa2010.query.all()
#         return jsonify([e.serialize() for e in yearlyETadata])
#     except Exception as e:
#         return (str(e))

# @app.route("/api/eta/2010_temp/<day_>")
# def get_eta_by_day_of_year(day_):
#     try:
#         yearlyETadata = ETa2010.query.filter_by(dayofyear=day_).all()
#         return jsonify([e.serialize() for e in yearlyETadata])
#     except Exception as e:
#         return (str(e))

if __name__ == '__main__':
    app.run()



