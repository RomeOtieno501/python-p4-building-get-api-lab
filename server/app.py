#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([{
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": [
            {
                "id": good.id,
                "name": good.name,
                "price": good.price,
                "created_at": good.created_at,
                "updated_at": good.updated_at,
                "bakery_id": good.bakery_id
            } for good in bakery.baked_goods
        ]
    } for bakery in bakeries])

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify({
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": [
            {
                "id": good.id,
                "name": good.name,
                "price": good.price,
                "created_at": good.created_at,
                "updated_at": good.updated_at,
                "bakery_id": good.bakery_id
            } for good in bakery.baked_goods
        ]
    })

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([{
        "id": good.id,
        "name": good.name,
        "price": good.price,
        "created_at": good.created_at,
        "updated_at": good.updated_at,
        "bakery_id": good.bakery_id,
        "bakery": {
            "id": good.bakery.id,
            "name": good.bakery.name,
            "created_at": good.bakery.created_at,
            "updated_at": good.bakery.updated_at
        }
    } for good in baked_goods])

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        return jsonify({"error": "No baked goods found"}), 404
    return jsonify({
        "id": most_expensive.id,
        "name": most_expensive.name,
        "price": most_expensive.price,
        "created_at": most_expensive.created_at,
        "updated_at": most_expensive.updated_at,
        "bakery_id": most_expensive.bakery_id,
        "bakery": {
            "id": most_expensive.bakery.id,
            "name": most_expensive.bakery.name,
            "created_at": most_expensive.bakery.created_at,
            "updated_at": most_expensive.bakery.updated_at
        }
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
