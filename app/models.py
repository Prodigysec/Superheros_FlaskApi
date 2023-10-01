from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'hero'

    serialize_rules = ('-hero_powers.heros', '-hero_powers.powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    super_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    powers = db.relationship('Power', secondary='hero_power', back_populates='hero')
    hero_powers = db.relationship('HeroPower', back_populates='hero')

    def __repr__(self):
        return f'<Hero {self.name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    
    heros = db.relationship('Hero', secondary='hero_power', back_populates='power')
    hero_powers = db.relationship('HeroPower', back_populates='power')

    def __repr__(self):
        return f'<Power {self.name}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    heros = db.relationship('Hero', back_populates='hero_power')
    powers = db.relationship('Power', back_populates='hero_power')

    def __repr__(self):
        return f'<HeroPower {self.hero_id} {self.power_id}>'
