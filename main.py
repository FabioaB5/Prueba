from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId, DBRef
from bson.json_util import dumps


MONGO_STRING_CONNECTION: str = "mongodb+srv://admin-staging:J3QUMICMQE9T3vnl@dropshipping-staging.6meionj.mongodb.net/mongo-dropshipping-staging?authSource=admin&replicaSet=atlas-s8w3w5-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
DATABASE = "mongo-dropshipping-staging"

client = MongoClient(MONGO_STRING_CONNECTION)
database = client.get_database(DATABASE)
collection = database.get_collection("shippingOrders")

app = Flask(__name__)


def _fill_db_ref_obj_id(document):
    for key, value in document.items():
        if value and isinstance(value, DBRef):
            related = collection.find_one({
                "_id": value
            })
            document[key] = related
            if related and isinstance(related, dict):
                _fill_db_ref_obj_id(related)
        if value and isinstance(value, ObjectId):
            document[key] = str(value)


@app.route('/find/<string:guide>', methods=["GET"])
def get_element(guide):
    try:
        element = collection.find_one({
            'guides': guide
        })
        if element is None:
            return jsonify({
                "message": f"No se ha encontrado el elemento {guide}"
            })
        _fill_db_ref_obj_id(element)
        return jsonify({
            "data": element
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@app.route('/find-all', methods=["GET"])
def get_elements():
    try:
        elements = []
        for element in collection.find():
            _fill_db_ref_obj_id(element)
            elements.append(element)
        return jsonify({
            "data": elements
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@app.route('/update/<string:guide>', methods=["PUT"])
def update_element(guide):
    try:
        body = request.get_json()
        element = collection.find_one({
            'guides': guide
        })
        if element is None:
            return jsonify({
                "message": f"No se ha encontrado el elemento {guide}"
            })

        collection.update_one({
            'guides': guide
        }, {
            "$set": body
        })
        _fill_db_ref_obj_id(element)
        element['status'] = body['status']
        return jsonify({
            "message": "El elemento fue actualizado satisfactoriamente",
            "data": element
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=7777)
