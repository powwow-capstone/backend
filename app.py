import os
import sys
import time
from datetime import date
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy, Model
from flask_sqlalchemy_caching import CachingQuery, FromCache
from flask_caching import Cache
=======
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
>>>>>>> master

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
from eta import *
from field_formatter import *
from field_cluster import *
from fields import *
from db_helper import *

@app.route("/")
def hello():
    return "Hello Cruel World!"

def field_query_helper(time_range):
    # Query the Field table and calculate each field's centroid and mean ETa
    # The mean ETa is determined by the time range, which is a dictionary of the
    # following format:
    # {  "month" : val1,  "year" : val2 }
    # If "month" is None, then get a yearly ETa average for each field
    # else get a monthly ETa average

    try:
        allFields = Field.query.all()

        start_month = 1
        end_month = 12
        if time_range["month"] != None:
            start_month = int(time_range["month"])
            end_month = int(time_range["month"])

        start = date(year=int(time_range["year"]), month=start_month, day=1)
        end = date(year=int(time_range["year"]), month=end_month,
                   day=get_days_in_month(end_month))

        eta_means = dict(ETa.query.with_entities(ETa.objectid, func.avg(ETa._mean)).filter(
            ETa.date <= end).filter(ETa.date >= start).group_by(ETa.objectid).all())

        for e in allFields:

            e.set_centroid()
            if eta_means.get(e.get_id()) != None:
                e.set_mean(eta_means.get(e.get_id()))
            else:
                e.set_mean(0)
        
        return allFields
        
    except Exception as e:
        print(str(e))
        return []


@app.route("/api/fields")
def get_all_field_data():
    month = request.args.get('month')
    print(month)
    if month == "null":
        month = None
    year = request.args.get('year')
    data = { "month" : month, "year" : year } 

    print(data);

    allFields = field_query_helper(data)

    alg(allFields)
    return jsonify(field_formatter([e.serialize() for e in allFields]))


@app.route("/api/eta")
def get_ETa_data_by_year_and_day():
    try:
        objectid_ = request.args.get('objectid')

        yearlyETadata = ETa.query.filter_by(
            objectid=objectid_).order_by(ETa.date).all()
        return jsonify([e.serialize() for e in yearlyETadata])
    except Exception as e:
        return (str(e))


@app.route('/api/filter_fields', methods=['POST'])
def get_filtered_field_data():
    params = request.json
    data = params["data"]
    time_range = { "month" : params["month"], "year" : params["year"] }
    try:
        allFields = field_query_helper(time_range)

        filtered_fields = []
        for e in allFields:
            if e.get_id() in data:
                filtered_fields.append(e)

        alg(filtered_fields)
        return jsonify(field_formatter([e.serialize() for e in filtered_fields]))

    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
