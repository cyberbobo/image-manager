# coding=utf-8
from flask import Flask, jsonify, request, render_template, url_for, redirect
from Modules.db_objects.db_objects import Session, engine, Base, UsbDrive, UsbDriveSchema
from Modules.forms.forms import addUsbDriveForm, deleteUsbDriveForm
from Modules.nested_lookup.nested_lookup import nested_lookup
from drives_mgmt import recursive_extraction
import os
from json import dumps
#from psutil import disk_partitions
from platform import system

# creating the Flask application
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

operating_system = system()

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

@app.route('/scandrives', methods=['GET', 'POST'])
def scan_drives():
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

    connected_peripherals = []
    if operating_system == "Linux":
        # lister les périphériques montés (/media)
        medias = os.popen("df | grep \"/media/\"").readlines()  #OK
        mountpoints = []
        for line in medias:
            mountpoints.append(line.split()[0].split("/")[2])
        data = os.popen("lsblk -f -J").read()
        uuid_dict = recursive_extraction(data)
        for i in mountpoints :
            connected_peripherals.append(uuid_dict[i])
        print(connected_peripherals)
    else :
        connected_peripherals.append("erreur")

    return render_template('drives_mgmt.html', connected_peripherals=connected_peripherals, drives=drives, addForm=addForm, delForm=delForm)

@app.route('/config')
def configuration():
    return render_template('config.html')