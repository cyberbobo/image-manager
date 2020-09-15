# coding=utf-8
from flask import Flask, jsonify, request
from Modules.db_objects.db_objects import Session, engine, Base, UsbDrive, UsbDriveSchema

# creating the Flask application
app = Flask(__name__)

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
drives = session.query(UsbDrive).all()

if len(drives) == 0:
    # create and persist dummy drive
    python_drive = UsbDrive("123456789012345678901234")
    session.add(python_drive)
    python_drive = UsbDrive("01234567890123456789012")
    session.add(python_drive)
    python_drive = UsbDrive("666")
    session.add(python_drive)
    session.commit()
    session.close()

    # reload drives
    drives = session.query(UsbDrive).all()

# show existing drives
print('### Drives:')
for drive in drives:
    print(f'({drive.id}) {drive.serial_no}')

@app.route('/drives')
def get_usbdrives():
    # fetching from the database
    session = Session()
    drive_objects = session.query(UsbDrive).all()

    # transforming into JSON-serializable objects
    schema = UsbDriveSchema(many=True)
    drives = schema.dump(drive_objects)

    # serializing as JSON
    session.close()
    return jsonify(drives)

@app.route('/drives', methods=['POST'])
def add_usbdrive():
    # mount drive object
    posted_usbdrive = UsbDriveSchema(only=('id', 'serial_no'))\
        .load(request.get_json())

    usbdrive = UsbDrive(**posted_usbdrive)

    # persist usbdrive
    session = Session()
    session.add(usbdrive)
    session.commit()

    # return created usbdrive
    new_usbdrive = UsbDriveSchema().dump(usbdrive)
    session.close()
    return jsonify(new_usbdrive), 201