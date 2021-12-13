
import json
import pickle
import numpy as np
import pandas as pd
import flask
from flask_cors import CORS, cross_origin

X = pd.read_csv("dummy.csv")

app = flask.Flask(__name__)
CORS(app, support_credentials=True)

__location = None
__data_columns = None
__model = None


def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(X.columns) - 1)
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    answer = round(__model.predict([x])[0],2)
    print(answer)
    return round(answer)

# def get_estimated_price(location,sqft,bath,bhk):    
#     loc_index = np.where(X.columns==location)[0][0]

#     x = np.zeros(len(X.columns))
#     x[0] = sqft
#     x[1] = bath
#     x[2] = bhk
#     if loc_index >= 0:
#         x[loc_index] = 1

#     return __model.predict([x])[0]

def get_Location_names():
    load_saved_artifacts()
    return __location


def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __location
    global __model
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __location = __data_columns[3:]
    with open("banglore_home_prices_model.pickle", 'rb') as file:
        __model = pickle.load(file)


from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/get_location_names")
def get_location_names():
    response = jsonify({"location": get_Location_names()})
    # response.header.add('Access-Control-Allow-Origin','*')

    return response


@app.route("/predict_home_price", methods=["POST"])
@cross_origin(supports_credentials=True)
def predict_home_price():
    total_sqft = float(request.form["total_sqft"])
    location = request.form["location"]
    bhk = int(request.form["bhk"])
    bath = int(request.form["bath"])

    response = jsonify(
        {"estimated_price": get_estimated_price(location, total_sqft, bhk, bath)}
    )
    # response.header.add('Access-Control-Allow-Origin','*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server for House Price Prediction...")
    app.run()
