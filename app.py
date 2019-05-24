from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, session, escape, render_template, jsonify, request, redirect, url_for, abort, flash
from flask_restful import Resource, Api
import datetime
import psycopg2
from classes.vas import Vas
from flask_login import LoginManager, login_user, UserMixin
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask.sessions import SessionInterface, SessionMixin
from redis import Redis
from werkzeug.datastructures import CallbackDict
import pickle
from uuid import uuid4

app = Flask(__name__)
# app = Flask(__name__, static_url_path=os.getcwd() + 'static/vendor1')
# Init mail
mail = Mail(app)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
mail = Mail(app)

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
    vehicle_image = db.Column(db.String(255))

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
    description =  db.Column(db.String(255))

class EmergencyAccess(db.Model):
    __tablename__ = "emergency_access"

    id = db.Column(db.Integer, primary_key=True)
    tenant_vehicle_id =  db.Column(db.Integer, db.ForeignKey('tenant_vehicles.id'))
    access_date =  db.Column(db.Date())
    access_time =  db.Column(db.Time())
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))


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
    page_title = "My Vehicles"
    # get all the vehicles that belongs to the login tenant
    # get tenant vehicles
    tenant_id = session['id']
    vehicles =  TenantVehicles.query.filter_by(tenant_id=tenant_id)

    return render_template("setup/tenant_vehicles.html", **locals())

@app.route('/setup/exclusive')
def exclusiveList():
    page_title = "Exclusive List"
    # get all the vehicles that belongs to the login tenant
    # Initialise the Vas class and pass submitted form inputs across
    exclusives = ExclusiveList.query.all()

    return render_template("setup/exclusive_list.html", **locals())

@app.route('/setup/exclusive', methods=['POST'])
def setupexclusiveList():
    reg_prefix = request.form.get('reg_prefix')
    description = request.form.get('description')

    # Create a new exclusive list
    new_exclu = ExclusiveList(reg_prefix=reg_prefix,description=description)

    # Add new record to db
    db.session.add(new_exclu)
    db.session.commit()

    flash("Operation was successful")

    return redirect(url_for('exclusiveList'))

@app.route('/emergency_access')
def emergencyAccess():
    # This method are used when the system seems to be down
    tenant_id = session['id']
    tenant_vehicles = TenantVehicles.query.filter_by(tenant_id=tenant_id)

    return render_template("emergency_access.html", **locals())

@app.route('/emergency_access', methods=['POST'])
def emergencyAccess_post():
    tenant_vehicle_id = request.form.get('tenant_vehicle_id')
    access_date = datetime.now().strftime('%Y-%m-%d')
    access_time = datetime.now().strftime('%H:%M:%S')
    tenant_id = session['id']

    new_access = EmergencyAccess(tenant_vehicle_id=tenant_vehicle_id,access_date=access_date,access_time=access_time,tenant_id=tenant_id)

    # Add new record to db
    db.session.add(new_access)
    db.session.commit()

    # Notify system admins of emergency access
    msg = Message('Emergency Alert', sender='alert@vas.se',
                              recipients=['akinola.paul2009@gmail.com'])
    msg.body = "A tenant just requested an emergency access. You may need to check if there is no system failure at moment."
    mail.send(msg)

    flash("Your request for access has been received. You will be granted access in 60 seconds.")

    return redirect(url_for('home'))

@app.route('/setup/vehicle', methods=['POST'])
def setupTenantVehicle():
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['vehicle_image']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            print(upload_result)

        vehicle_make = request.form.get('vehicle_make')
        vehicle_model = request.form.get('vehicle_model')
        plate_number = request.form.get('plate_number')
        tenant_id = request.form.get('tenant_id')
        vehicle_image = upload_result['secure_url']


        # add vehicle to tenant vehicle table
        new_vehicle = TenantVehicles(vehicle_make=vehicle_make,vehicle_model=vehicle_model,plate_number=plate_number,tenant_id=tenant_id,vehicle_image=vehicle_image)

        # Add new record to db
        db.session.add(new_vehicle)
        db.session.commit()

        flash("Operation was successful")

    return redirect(url_for('tenantVehicles'))

@app.route('/setup/guests')
def tenantGuests():
    # get all the vehicles that belongs to the login tenant
    tenant_id = session['id']
    # get tenant guest
    guests = TenantGuests.query.filter_by(tenant_id=tenant_id).all()

    return render_template("setup/tenant_guests.html", **locals())

@app.route('/setup/delete_guest',  methods=["POST", "GET"])
def deleteGuest():
    vas = Vas(request.args,  connect())
    # Complete delete
    vas.deleteGuest()
    flash("Guest deleted successfully")

    return redirect(url_for('tenantGuests'))

@app.route('/setup/delete_vehicle',  methods=["POST", "GET"])
def deleteVehicle():
    vas = Vas(request.args,  connect())
    # Complete delete
    vas.deleteVehicle()
    flash("Vehicle deleted successfully")

    return redirect(url_for('tenantVehicles'))

@app.route('/setup/delete_exclu',  methods=["POST", "GET"])
def deleteExclu():
    vas = Vas(request.args,  connect())
    # Complete delete
    vas.deleteExclu()
    flash("Reg prefix deleted successfully")

    return redirect(url_for('exclusiveList'))

@app.route('/setup/guest', methods=['POST'])
def setupTenantGuest():
    # Initialise the Vas class and pass submitted form inputs across
    vas = Vas(request.form,  connect())
    # add guest
    vas.addTenantGuest()

    return redirect(url_for('tenantGuests'))

@app.route('/system_check')
def systemCheck():
    page_title = "System Check"
    return render_template("system_check.html", **locals())


if __name__ == '__main__':

    app.run()