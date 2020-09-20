# coding=utf-8
from flask import Flask, jsonify, request, render_template, url_for, redirect
from Modules.db_objects.db_objects import Session, engine, Base, UsbDrive, UsbDriveSchema
from Modules.forms.forms import addUsbDriveForm, deleteUsbDriveForm
import os

# creating the Flask application
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# generate database schema
Base.metadata.create_all(engine)
"""
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
"""

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/drives', methods=['GET', 'POST'])
def manage_usbdrives():
    # fetching from the database
    session = Session()
    drive_objects = session.query(UsbDrive).all()

    # transforming into JSON-serializable objects
    schema = UsbDriveSchema(many=True)
    drives = schema.dump(drive_objects)

    # serializing as JSON
    session.close()

    addForm = addUsbDriveForm()
    delForm = deleteUsbDriveForm()

    return render_template('drives_mgmt.html', drives=drives, addForm=addForm, delForm=delForm)

@app.route('/adddrive', methods=['GET', 'POST'])
def add_usbdrive():
    # fetching from the database
    session = Session()
    drive_objects = session.query(UsbDrive).all()

    # transforming into JSON-serializable objects
    schema = UsbDriveSchema(many=True)
    drives = schema.dump(drive_objects)

    # serializing as JSON
    session.close()

    addForm = addUsbDriveForm()
    delForm = deleteUsbDriveForm()

    if addForm.validate_on_submit():
        usbdrive = UsbDrive(addForm.serial_no.data)
        session = Session()
        session.add(usbdrive)
        session.commit()
        session.close()
        return redirect(url_for('manage_usbdrives'))
    else:
        print(addForm.errors)

    return render_template('drives_mgmt.html', drives=drives, addForm=addForm, delForm=delForm)

@app.route('/deldrive', methods=['GET', 'POST'])
def del_usbdrive():
    # fetching from the database
    session = Session()
    drive_objects = session.query(UsbDrive).all()

    # transforming into JSON-serializable objects
    schema = UsbDriveSchema(many=True)
    drives = schema.dump(drive_objects)

    # serializing as JSON
    session.close()

    addForm = addUsbDriveForm()
    delForm = deleteUsbDriveForm()

    if delForm.validate_on_submit():
        session = Session()
        usbdrive = session.query(UsbDrive).filter_by(serial_no=delForm.serial_no.data).first()
        session.delete(usbdrive)
        session.commit()
        session.close()
        return redirect(url_for('manage_usbdrives'))
    else:
        print(delForm.errors)

    return render_template('drives_mgmt.html', drives=drives, addForm=addForm, delForm=delForm)

"""
# A SUPPRIMER
def get_usbdrives():
    # fetching from the database
    session = Session()
    drive_objects = session.query(UsbDrive).all()

    # transforming into JSON-serializable objects
    schema = UsbDriveSchema(many=True)
    drives = schema.dump(drive_objects)

    # serializing as JSON
    session.close()
    return render_template('test_drives.html', drives=drives)
"""

@app.route('/config')
def configuration():
    return render_template('config.html')

"""
@app.route('/bidon')
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
"""