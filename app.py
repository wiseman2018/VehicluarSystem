from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
import datetime
import psycopg2

app = Flask(__name__)
# app = Flask(__name__, static_url_path=os.getcwd() + 'static/vendor1')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    password = db.Column(db.String(128))


class Tenants(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    passcode = db.Column(db.String(128))
    apt_number = db.Column(db.String(128))
    move_in_date = db.Column(db.String(128))


class TenantVehicles(db.Model):
    __tablename__ = "tenant_vehicles"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer)
    plate_number = db.Column(db.String(128))


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        return psycopg2.connect(os.environ['DATABASE_URL'])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    app.run()