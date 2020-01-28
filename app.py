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
from eta import *

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
    try:
        objectid_ = request.args.get('objectid', '54321')

        yearlyETadata = ETa.query.filter_by(objectid=objectid_).all()
        return jsonify([e.serialize() for e in yearlyETadata])
    except Exception as e:
        return (str(e))

if __name__ == '__main__':
    app.run()



