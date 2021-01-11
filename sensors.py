from flask import Flask, request, jsonify, abort
import json
import uuid 
  

app = Flask(__name__)


sensors = {}


@app.route("/sensors", methods=["GET"])
def get_sensors():
    return(jsonify(sensors))


@app.route("/sensors", methods=["POST"])
def post_sensor():
    if not request.json:
        abort(400, message="Please, post the information about sensor.")
    if not "name" in request.json:
        abort(400, message="Please, post the information about sensor.")
    if not "unit" in request.json:
        abort(400, message="Please, post the information about sensor.")

    sensor_id = uuid.uuid4().hex
    sensor = {sensor_id :{"uuid": sensor_id, "name": request.json.get("name", ""),"unit": request.json.get("unit", ""),"value": request.json.get("value", "")}}
    sensors.update(sensor)
    return(jsonify(sensors))


@app.route("/sensors/<string:sensor_uuid>", methods=["GET"])
def get_sensor_by_uuid(sensor_uuid):
    
    if sensor_uuid in sensors:
        return(jsonify(sensors[sensor_uuid]))
    else:
        abort(404)


@app.route("/sensors/<string:sensor_uuid>", methods=["DELETE"])
def delete_sensor_by_uuid(sensor_uuid):
    
    if sensor_uuid in sensors:
        del sensors[sensor_uuid]
        return(jsonify(sensors))
    else:
        abort(404)





if __name__ == "__main__":
    app.run(debug=True)
