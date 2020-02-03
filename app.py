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

def create_pin(x):

    """ This function generates a 15digit pin using the random mudule.
    x is the number of digits reqired"""
    
    lower = 10**(x-1)
    upper = 10**x - 1
    return random.randint(lower, upper)


@app.route('/', methods=['GET'])
@app.route('/pin', methods=['GET'])
def index():
    """
    the endpoint for a resource that generates
    a unique 15digit pin and 3digit serial number on request.
    """
    
    """loop to ensure that created pin doesn't exist in database for easy validation"""
    counter = 1
    while counter >= 1:
        pin = create_pin(15)
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
def validates(pin):
    """
    This endpoint checks to validate or not that the pin
    requested is same with the  stored one in the database.
    """
    pin = Register.query.filter_by(pin=pin).all()
    if pin:
        return jsonify({'message': 'This Pin is Valid'})
    return jsonify({'message': 'This Pin could not be validated!!!'})


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
