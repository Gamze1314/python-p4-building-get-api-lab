#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
import ipdb
from models import db, Bakery, BakedGood
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries')
def bakeries():
    # returns a list of JSON objects for all bakeries in the db.
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Set a breakpoint here
    # ipdb.set_trace()

    # Get bakery by id
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    print(f"Bakery object: {bakery}")
    print(f"Bakery attributes: {bakery.__dict__}")

    # Serialize bakery with baked goods
    serialized_bakery = bakery.to_dict()

    print(f"Serialized bakery: {serialized_bakery}")

    return make_response(jsonify(serialized_bakery), 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # returns a list of baked goods as JSON, sorted by price in descending order
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    baked_goods_list = [bg.to_dict() for bg in baked_goods]

    # Return the result as JSON
    return make_response(jsonify(baked_goods_list), 200)



@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    #returns a single most expensive baked good as JSON.
    #sort the baked goods in desceing order then limit the number of result. limit=1
    most_expensive_bg = BakedGood.query.order_by(desc(BakedGood.price)).first()

    serialized_bg = most_expensive_bg.to_dict()

    return make_response(serialized_bg, 200)



if __name__ == '__main__':
    # ipdb.set_trace()
    app.run(port=5555, debug=True)
