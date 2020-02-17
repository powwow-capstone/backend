import os
import sys
import time
import statistics
import json
import multiprocessing
from datetime import date
from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
# from flask_caching import Cache
from sqlalchemy.sql import table, column, select, func

app = Flask(__name__)

# TODO: Remove the CORS line before submitting final version!
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = SQLAlchemy(app)

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
        if time_range["start_month"] != None and time_range["end_month"] != None:
            start_month = int(time_range["start_month"])
            end_month = int(time_range["end_month"])

        start = date(year=int(time_range["start_year"]), month=start_month, day=1)
        end = date(year=int(time_range["end_year"]), month=end_month,
                   day=get_days_in_month(end_month))

        eta_means = dict(ETa.query.with_entities(ETa.objectid, func.sum(ETa._mean)).filter(
            ETa.date <= end).filter(ETa.date >= start).group_by(ETa.objectid).all())

        if len(eta_means) == 0:
            # No data fits this time range
            return []

        for e in allFields:

            e.set_centroid()
            if eta_means.get(e.get_id()) != None:
                e.set_mean(eta_means.get(e.get_id()))
            else:
                e.set_mean(-1)
        
        return allFields

        e.set_mean()
            
        alg(allFields)
        print("About to format")
        return jsonify(field_formatter([e.serialize() for e in allFields]))

    except Exception as e:
        print(str(e))
        return []




@app.route("/api/fields")
# @app.cache.cached(timeout=300)
def get_all_field_data():
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')
    if start_month == "null" or end_month == "null":
        start_month = None
        end_month = None
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    data = { "start_month" : start_month, "start_year" : start_year, "end_month" : end_month, "end_year" : end_year } 

    allFields = field_query_helper(data)
    if len(allFields) > 0:

        alg(allFields)        
        return jsonify(field_formatter([e.serialize() for e in allFields]))
    else:
        # No data fits within this time range
        # Return 404
        return {}, 404

@app.route("/api/eta")
# @app.cache.cached(timeout=120)
def get_ETa_data_by_year_and_day():
    try:
        objectid_ = request.args.get('objectid')
        cohortids_ = request.args.getlist('cid')
        # cohortids_ = set(request.args.getlist('cid') )


        # Parse date range of query
        # At the moment, this is not being used

        # start_month = request.args.get('start_month')
        # end_month = request.args.get('end_month')
        # if start_month == "null" or end_month == "null":
        #     start_month = 1
        #     end_month = 12
        # start_year = request.args.get('start_year')
        # end_year = request.args.get('end_year')

        # start = date(year=int(start_year), month=start_month, day=1)
        # end = date(year=int(end_year), month=end_month,
        #            day=get_days_in_month(end_month))

        results = {}

        cohortETadata = ETa.query.filter(ETa.objectid.in_(cohortids_)).with_entities(ETa.date,
            func.avg(ETa._mean), func.stddev(ETa._mean)).group_by(ETa.date).order_by(ETa.date).all()
    
        results["cohort_stats"] = [{"date": e[0], "_mean": e[1], "_stdev": e[2]} for e in cohortETadata]

        yearlyETadata = ETa.query.with_entities(ETa.date, ETa._mean).filter_by(
         objectid=objectid_).order_by(ETa.date).all()
    
        results["field_stats"] = [{ "date" : e[0], "_mean" : e[1] } for e in yearlyETadata]


        return jsonify(results)
        # return jsonify({"field_stats": [{"date": e[0], "_mean": e[1]} for e in yearlyETadata], "cohort_stats": [{"date": e[0], "mean": e[1], "stdev": e[2]} for e in cohortETadata]})
    except Exception as e:
        return (str(e))


@app.route('/api/filter_fields', methods=['POST'])
# @app.cache.cached(timeout=120)
def get_filtered_field_data():
    params = request.json
    data = params["data"]
    time_range = {"start_month": params["start_month"], "start_year": params["start_year"],
                  "end_month": params["end_month"], "end_year": params["end_year"]}
    try:
        allFields = field_query_helper(time_range)

        if len(allFields) > 0:

            filtered_fields = []
            for e in allFields:
                if e.get_id() in data:
                    filtered_fields.append(e)

            alg(filtered_fields)
            return jsonify(field_formatter([e.serialize() for e in filtered_fields]))
        
        else:
            # No data fits within this time range
            # Return 404
            return {}, 404

    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
