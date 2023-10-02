#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the Superhero API!'


@app.route('/heroes', methods=['GET', 'POST'])
def heroes():
    if request.method == 'GET':
        heroes = []
        for hero in Hero.query.all():
            hero_dict = {
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [power.name for power in hero.powers]
            }
            heroes.append(hero_dict)
        return jsonify(heroes)

    elif request.method == 'POST':
        data = request.get_json()
        name = data['name']
        super_name = data['super_name']

        hero = Hero(name=name, super_name=super_name)
        db.session.add(hero)
        db.session.commit()

        return make_response(
            jsonify({
                "message": f"Successfully created hero {hero.name} with id {hero.id}"
            }),
            201
        )


@app.route('/heroes/<int:hero_id>', methods=['GET', 'DELETE'])
def hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return make_response(
            jsonify({"error": "Not found"}),
            404
        )

    if request.method == 'GET':
        hero_dict = {
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [power.name for power in hero.powers]
        }
        return jsonify(hero_dict)

    elif request.method == 'DELETE':
        db.session.delete(hero)
        db.session.commit()

        return make_response(
            jsonify({
                "message": f"Successfully deleted hero {hero.name} with id {hero.id}"
            }),
            200
        )


@app.route('/powers', methods=['GET', 'POST'])
def powers():
    if request.method == 'GET':
        powers = []
        for power in Power.query.all():
            power_dict = {
                "name": power.name,
                "description": power.description,
                "heroes": [hero.name for hero in power.heroes]
            }
            powers.append(power_dict)
        return jsonify(powers)

    elif request.method == 'POST':
        data = request.get_json()
        name = data['name']
        description = data['description']

        power = Power(name=name, description=description)
        db.session.add(power)
        db.session.commit()

        return make_response(
            jsonify({
                "message": f"Successfully created power {power.name} with id {power.id}"
            }),
            201
        )


@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return make_response(
            jsonify({"error": "Not found"}),
            404
        )

    if request.method == 'GET':
        power_dict = {
            "name": power.name,
            "description": power.description,
            "heroes": [hero.name for hero in power.heroes]
        }
        return jsonify(power_dict)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        description = data['description']

        power.description = description
        db.session.commit()

        return make_response(
            jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
                }),
            200
        )



@app.route('/heropowers', methods=['POST'])
def hero_powers():
    if request.method == 'POST':
        data = request.get_json()
        hero_id = data['hero_id']
        power_id = data['power_id']
        strength = data['strength']

        hero_power.strength = strength
        hero_power.power_id = power_id
        hero_power.hero_id = hero_id

        db.session.commit()

        hero = Hero.query.get(hero_power.hero_id)

        return make_response(
            jsonify({
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [power.name for power in hero.powers]
                }),
            200
        )


if __name__ == '__main__':
    app.run(port=5555)
