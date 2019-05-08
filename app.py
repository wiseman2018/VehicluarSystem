from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, session, escape, render_template, jsonify, request, redirect, url_for, abort, flash
from flask_restful import Resource, Api
import datetime
import psycopg2
from classes.vas import Vas
from flask_login import LoginManager, login_user, UserMixin

app = Flask(__name__)
# app = Flask(__name__, static_url_path=os.getcwd() + 'static/vendor1')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    password = db.Column(db.String(128))


class Tenants(db.Model, UserMixin):
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
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    plate_number = db.Column(db.String(128))
    vehicle_make = db.Column(db.String(128))
    vehicle_model = db.Column(db.String(128))

class TenantGuests(db.Model):
    __tablename__ = "tenant_guests"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    guest_name =  db.Column(db.String(128))
    plate_number = db.Column(db.String(128))
    arrival_date =  db.Column(db.Date())
    arrival_time =  db.Column(db.Time())
    vehicle_make = db.Column(db.String(128))
    vehicle_model = db.Column(db.String(128))

class ExclusiveList(db.Model):
    __tablename__ = "exclusive_list"

    id = db.Column(db.Integer, primary_key=True)
    reg_prefix =  db.Column(db.String(128))


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


# Application Routes
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login')
def login1():
    return render_template("login.html")

    
@app.route('/setup')
def setup():
    return render_template("setup.html")

@app.route('/home')
def home():
    tenant_id = session['id']
    vehicles = TenantVehicles.query.count()
    guests = TenantGuests.query.filter_by(tenant_id=tenant_id).count()
    return render_template("home.html", **locals())

@app.route('/about')
def aboout():
    # display the about page
    return render_template("about.html")

@app.route('/doSetUp', methods=['POST'])
def doSetUp():
    # Initialise the Vas class and pass submitted form inputs across
    vas = Vas(request.form,  connect())
    # Complete signup
    vas.signUp()
    
    # redirect to login page
    return redirect(url_for('login'))

@app.route('/doLogin', methods=['POST'])
def doLogin():
    # Initialise the Vas class and pass submitted form inputs across
    vas = Vas(request.form,  connect())
    # Complete login
    userInfo = vas.login()

    print(userInfo)

    return_route = "login"
    if (len(userInfo) > 0):
        # Set session vars
        session['id'] = userInfo[0][0]
        session['first_name'] = userInfo[0][1]
        session['last_name'] = userInfo[0][2]
        session['email'] = userInfo[0][3]
        session['phone'] = userInfo[0][4]
        return_route = "home"
    else:
        abort(401)

    # redirect to needed page
    return redirect(url_for(return_route))

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('email', None)
    session.pop('phone', None)

    return redirect(url_for('login'))

@app.route('/setup/vehicles')
def tenantVehicles():
    # get all the vehicles that belongs to the login tenant
    # get tenant vehicles
    vehicles = TenantVehicles.query.all()

    return render_template("setup/tenant_vehicles.html", **locals())

@app.route('/setup/exclusive')
def exclusiveList():
    # get all the vehicles that belongs to the login tenant
    # Initialise the Vas class and pass submitted form inputs across
    exclusives = ExclusiveList.query.all()

    return render_template("setup/exclusive_list.html", **locals())

@app.route('/setup/exclusive', methods=['POST'])
def setupexclusiveList():
    reg_prefix = request.form.get('reg_prefix')

    # Create a new exclusive list
    new_exclu = ExclusiveList(reg_prefix=reg_prefix)

    # Add new record to db
    db.session.add(new_exclu)
    db.session.commit()

    flash("Operation was successful")

    return redirect(url_for('exclusiveList'))

@app.route('/setup/vehicle', methods=['POST'])
def setupTenantVehicle():
    # Initialise the Vas class and pass submitted form inputs across
    vas = Vas(request.form,  connect())
    # get tenant vehicles
    vas.addTenantVehicle()

    return redirect(url_for('tenantVehicles'))

@app.route('/setup/guests')
def tenantGuests():
    # get all the vehicles that belongs to the login tenant
    tenant_id = session['id']
    # get tenant guest
    guests = TenantGuests.query.filter_by(tenant_id=tenant_id).all()

    return render_template("setup/tenant_guests.html", **locals())

@app.route('/setup/guest', methods=['POST'])
def setupTenantGuest():
    # Initialise the Vas class and pass submitted form inputs across
    vas = Vas(request.form,  connect())
    # add guest
    vas.addTenantGuest()

    return redirect(url_for('tenantGuests'))


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = os.urandom(24)

    app.run()