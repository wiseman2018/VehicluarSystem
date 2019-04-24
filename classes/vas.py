import datetime

class Vas:
    def __init__(self, param, conn):
        self.param = param
        self.conn = conn
        self.cur = conn.cursor()

    def login(self):
        access_code = self.param['access_code']

        self.cur.execute(
            'SELECT * FROM tenants WHERE passcode = %s', [access_code])
        return self.cur.fetchall()

    def signUp(self):
        first_name = self.param['first_name']
        last_name = self.param['last_name']
        email = self.param['email']
        phone = self.param['phone']
        passcode = self.param['access_code1']
        apt_number = self.param['apt_number']
        move_in_date = self.param['move_in_date']

        print(first_name, last_name, email, phone, passcode)

        # insert record
        self.cur.execute('INSERT INTO tenants (first_name, last_name, email, phone, passcode, apt_number, move_in_date ) values (%s, %s, %s, %s, %s, %s, %s )', [
                         first_name, last_name, email, phone, passcode, apt_number, move_in_date])
        self.conn.commit()
        return self.conn.commit()

    
    def getTenantVehicle(self):
        tenant_id = self.param['id']

        self.cur.execute(
            'SELECT * FROM tenant_vehicles WHERE tenant_id = %s', [tenant_id])
        return self.cur.fetchall()


    def addTenantVehicle(self):
        vehicle_make = self.param['vehicle_make']
        vehicle_model = self.param['vehicle_model']
        plate_number = self.param['plate_number']
        tenant_id = self.param['tenant_id']

        print(tenant_id, plate_number)

        # insert record
        self.cur.execute('INSERT INTO tenant_vehicles (tenant_id, plate_number, vehicle_make, vehicle_model ) values (%s, %s, %s, %s )', [
                         tenant_id, plate_number, vehicle_make, vehicle_model])
        return self.conn.commit()
    
    def getTenantGuest(self):
        tenant_id = self.param['id']

        self.cur.execute(
            'SELECT * FROM tenant_guests WHERE tenant_id = %s', [tenant_id])
        return self.cur.fetchall()


    def addTenantGuest(self):
        guest_name = self.param['guest_name']
        arrival_date = self.param['arrival_date']
        plate_number = self.param['plate_number']
        arrival_time = self.param['arrival_time']
        vehicle_make = self.param['vehicle_make']
        vehicle_model = self.param['vehicle_model']
        tenant_id = self.param['tenant_id']

        # insert record
        self.cur.execute('INSERT INTO tenant_guests (tenant_id, guest_name, plate_number, arrival_date, arrival_time, vehicle_make, vehicle_model ) values (%s, %s, %s, %s, %s, %s, %s )', [
                         tenant_id, guest_name, plate_number, arrival_date, arrival_time, vehicle_make, vehicle_model])
        return self.conn.commit()

