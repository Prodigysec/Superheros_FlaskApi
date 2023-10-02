#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Hero, Power, HeroPower

fake = Faker()

with app.app_context():
    HeroPower.query.delete()
    Power.query.delete()
    Hero.query.delete()

    print("🦸‍♀️ Seeding powers...")
    powers = []
    for i in range(10):
        p = Power(name=fake.first_name(), description=fake.text())
        powers.append(p)

    db.session.add_all(powers)
    db.session.commit()

    print("🦸‍♀️ Seeding heroes...")
    heroes = []
    for i in range(10):
        h = Hero(name=fake.first_name(), super_name=fake.first_name())
        heroes.append(h)

    db.session.add_all(heroes)
    db.session.commit()

    print("🦸‍♀️ Adding powers to heroes...")
    hero_powers = []
    for i in range(10):
        hero = rc(heroes)
        power = rc(powers)
        hp = HeroPower(heros=hero, powers=power, strength=randint(1, 3))
        hero_powers.append(hp)

    db.session.add_all(hero_powers)
    db.session.commit()

    print("🦸‍♀️ Seeding complete!")
