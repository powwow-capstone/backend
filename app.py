import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy, Model
from flask_sqlalchemy_caching import CachingQuery, FromCache
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'

# TODO: Remove the CORS line before submitting final version!
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Model.query_class = CachingQuery
db = SQLAlchemy(session_options={'query_cls': CachingQuery})
db.init_app(app)

cache = Cache(app)

sys.path.append('models')
sys.path.append('algorithm')
from fields import *
from field_cluster import *
from field_formatter import *
from eta import *

@app.route("/")
def hello():
    return "Hello Cruel World!"

@app.route("/api/fields")
def get_all_field_data():
    try:
        allFields = Field.query.options(FromCache(cache)).all()
        for e in allFields:
            e.set_centroid()
            e.set_mean()
            
        alg(allFields)
        print("About to format")
        
        return jsonify(field_formatter([e.serialize() for e in allFields]))
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
        objectid_ = request.args.get('objectid')

        yearlyETadata = ETa.query.filter_by(objectid=objectid_).order_by(ETa.date).options(FromCache(cache)).all()
        return jsonify([e.serialize() for e in yearlyETadata])
    except Exception as e:
        return (str(e))

@app.route('/api/filter_fields', methods=['POST'])
def get_filtered_field_data():
    data = request.json
    # print(type(data))
    try:
        allFields = Field.query.all()
       
        filtered_fields = []
        for e in allFields:
            e.set_centroid()
            e.set_mean()
            if e.get_id() in data:
                filtered_fields.append(e)
        
        alg(filtered_fields)
        return jsonify(field_formatter([e.serialize() for e in filtered_fields]))
        
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



