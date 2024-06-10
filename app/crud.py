from bson import ObjectId
from flask import Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://abhipshabhatta:<@bheeps@123>@uberclone.qqr6qbm.mongodb.net/"
mongo = PyMongo(app)


@app.route('/driver/add', methods=['POST'])
def add_driver():
    drivers = mongo.db.drivers
    driver = {
        'name': request.form.get('name'),
        'license_number': request.form.get('license_number'),
    }
    drivers.insert_one(driver)
    return redirect(url_for('list_drivers'))

@app.route('/drivers')
def list_drivers():
    drivers = mongo.db.drivers.find()
    return jsonify([driver for driver in drivers])


@app.route('/driver/update/<driver_id>', methods=['POST'])
def update_driver(driver_id):
    drivers = mongo.db.drivers
    drivers.update_one({'_id': ObjectId(driver_id)}, {"$set": {
        'name': request.form.get('name'),
        'license_number': request.form.get('license_number'),
    }})
    return redirect(url_for('list_drivers'))

@app.route('/driver/delete/<driver_id>', methods=['GET'])
def delete_driver(driver_id):
    mongo.db.drivers.delete_one({'_id': ObjectId(driver_id)})
    return redirect(url_for('list_drivers'))

if __name__ == '__main__':
    app.run(debug=True)
