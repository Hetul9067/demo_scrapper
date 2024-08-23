from app import app
from model.building_data_model import building_data_model
from flask import request

obj = building_data_model()

@app.route("/scrape/building_data")
def scrape_data_controller():
    return obj.scrape_data_model()

@app.route("/scrape/dashboard")
def get_properties_controller() :

    # fetch parameters from the request
    lowest_price = request.args.get('lowest_price')
    recently_built = request.args.get('recently_built')
    style = request.args.get('style')



    return obj.get_properties_model(lowest_price, recently_built, style)

@app.route("/scrape/delete", methods=["DELETE"])
def properties_del_controller() :
    return obj.properties_del_model()