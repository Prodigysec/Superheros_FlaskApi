from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-heros.powers', '-powers.heros',)

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    heros = db.relationship('Hero', back_populates='hero_powers')
    powers = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self,key,strength):
        allowed_strengths = ['Strong', 'Weak','Average']
        if strength not in allowed_strengths:
            raise ValueError(f"strength must be one of {','.join(allowed_strengths)}")
        return strength


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heros'

    serialize_rules = ('-hero_powers.powers', '-powers.heros',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    super_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes')
    hero_powers = db.relationship('HeroPower', back_populates='heros')



class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-heros.powers', '-hero_powers.heros',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    
    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers')
    hero_powers = db.relationship('HeroPower', back_populates='powers')

    @validates('description')
    def validate_description(self, key,description):
        if len(description) < 20:
            raise ValueError('description must be 20 characters long')
        else:
            return description





