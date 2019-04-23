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