from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from threading import Timer, Thread, Event

import RPi.GPIO as GPIO
import smbus
import time
import signal

firstevent = False

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT)

# Define some constants from the datasheet

DEVICE     = 35 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def readDevice(addr):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)


class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        
class Light(Resource):
    def get(self):
        lightLevel=readLight()
        # print("Light Level : " + format(lightLevel,'.2f') + " lx")
        return {'lightx': format(lightLevel,'.2f') + " lx"}

class ReadI2CDevice(Resource):
    def get(self, device_address):
        I2CDeviceValue = readDevice(int(device_address))
        return {'i2cdevicevalue': I2CDeviceValue}

class ReadPin(Resource):
    def get(self, pin_number):
        status = GPIO.input(int(pin_number))

        return {'pin_number':pin_number, 'status': status}

class WritePin(Resource):
    def get(self, pin_number,value):
        GPIO.output(int(pin_number),int(value))
        status = GPIO.input(int(pin_number))
        return {'pin_number':pin_number, 'status': status}

class TogglePin(Resource):
    def get(self, pin_number):

        status = GPIO.input(int(pin_number))
        if status == GPIO.HIGH:
            GPIO.output(int(pin_number),GPIO.LOW)
        else:
            GPIO.output(int(pin_number),GPIO.HIGH)

        status = GPIO.input(int(pin_number))
        return {'pin_number':pin_number, 'status': status}


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
api.add_resource(Light, '/light') # Route_4
api.add_resource(ReadI2CDevice, '/readi2cdevice/<device_address>') # Route_4

api.add_resource(ReadPin, '/readpin/<pin_number>') # Route_3
api.add_resource(WritePin, '/writepin/<pin_number>/<value>') # Route_3
api.add_resource(TogglePin, '/togglepin/<pin_number>') # Route_3


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t

def chekLight():
    global firstevent
    lightlevel = readLight()
    if lightlevel < 50:
        print("Light Level : " + format(lightlevel,'.2f') + " lx")
        if not firstevent:
            m = "Alarm! Light Level : " + format(lightlevel,'.2f') + " lx"
            print(m)
            sendEmailMessage("simmaco.ferriero@live.it", "simmaco.ferriero@gmail.com", "Alarm light", m)
            firstevent = True


def sendEmailMessage(f,t,s,m):
    import email
    import smtplib

    msg = email.message_from_string(m)
    msg['From'] = f
    msg['To'] = t
    msg['Subject'] = s

    s = smtplib.SMTP("smtp.live.com",587)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login('simmaco.ferriero@live.it', '<YOUR_PASSWORD>')

    s.sendmail(f, t, msg.as_string())

    s.quit()

set_interval(chekLight,1)



if __name__ == '__main__':
    firstevent = False
    app.run(host='192.168.1.38',port='5002')
