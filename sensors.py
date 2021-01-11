from flask import Flask, request, jsonify, abort
import json
import uuid
import re
  

app = Flask(__name__)


sensors = {}


@app.route("/sensors", methods=["GET"])
def get_sensors():
    if "name" in request.args:
        sensor = [sensor for sensor in sensors.values() if re.match(str(request.args.get("name")), sensor["name"], re.IGNORECASE)]
        return jsonify(sensor)

    return(jsonify([sensor for sensor in sensors.values()]))


@app.route("/sensors", methods=["POST"])
def post_sensor():
    if not request.json:
        abort(400)
    if not "name" in request.json:
        abort(400)
    if not "unit" in request.json:
        abort(400)

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


@app.route("/sensors/<string:sensor_uuid>", methods=["PATCH"])
def patch_sensor_by_uuid(sensor_uuid):
    if sensor_uuid in sensors:
        if not "value" in request.json:
            abort(400)
        else:
            sensors[sensor_uuid]["value"] = request.json.get("value", "")
            return(jsonify(sensors))
    else:
        abort(404)




if __name__ == "__main__":
    app.run(debug=True)
