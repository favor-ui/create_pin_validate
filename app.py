from flask import Flask, jsonify
import random
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '956une*gj7@'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Register(db.Model):
    __tablename__ = 'register'

    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.Integer, unique=True, nullable=False)
    pin = db.Column(db.String(140), unique=True, nullable=False)
    request_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, sn, pin):
        self.sn = sn
        self.pin = pin

    def __repr__(self):
        return '<pin {}>'.format(self.pin)

def create_rand(x):
    """ A function to generate random 15 digit number. where n is the number of Digits"""
    lower = 10**(x-1)
    upper = 10**x - 1
    return random.randint(lower, upper)


@app.route('/', methods=['GET'])
@app.route('/pin', methods=['GET'])
def index():
    """
    This is the end point for a resource that generates random 15digit pin and serial number when the
    resource is requested.
    it generates 15digits random pin, and verifies that pin does not already exists in the database
    before returning it to the client in JSON format.
    random_digit function is created with random function.
    :return: pin, serial
    """
    # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
    counter = 1
    while counter >= 1:
        pin = create_rand(15)
        sn = random.randrange(100,999)
        pin1 = Register.query.filter_by(pin=str(pin)).all()
        sn1 = Register.query.filter_by(sn=int(sn)).all()
        
        if pin1 or sn1:
            print('again')
            counter = counter + 1
        else:
            print(pin, sn)
            break

    table = Register(sn=int(sn), pin=str(pin))
    db.session.add(table)
    db.session.commit()
    serial_number = sn
    pin1 = pin
    return jsonify({'serial number': serial_number, 'PIN': pin1})

@app.route('/<string:pin>', methods=['GET'])
def check_sn(pin):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    pin = Register.query.filter_by(pin=pin).all()
    if pin:
        return jsonify({'message': 'Valid PIN'})
    return jsonify({'message': 'Invalid PIN !!!'})


if __name__ == '__main__':
    app.run()


"""
the content of this app will not copy into database untill you do the following
* flask db init
*flask db migrate -m 'new table'
*flask db upgrade
ensure all modules are installed and imported
although using pip3, some dependencies require pip packages
"""
