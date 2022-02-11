# coding=utf-8
from flask import Flask, jsonify, request, render_template, url_for, redirect
from Modules.db_objects.db_objects import Session, engine, Base, UsbDrive, UsbDriveSchema, Target, TargetSchema, Tool, ToolSchema
from Modules.forms.forms import addUsbDriveForm, deleteUsbDriveForm, addTargetForm, deleteTargetForm, addToolForm, deleteToolForm
from Modules.nested_lookup.nested_lookup import nested_lookup
from drives_mgmt import recursive_extraction
import os
from json import dumps
from platform import system
from sqlalchemy.exc import SQLAlchemyError
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# creating the Flask application
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

operating_system = system()

# generate database schema
Base.metadata.create_all(engine)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/new_save', methods=['GET'])
def new_save():
    #popup : relou
    # juste faire un file explorer : https://github.com/ergoithz/browsepy ?
    # tkinter = file explorer
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    return render_template('main.html')

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
        try :
            session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("erreur "+error)
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
        try :
            usbdrive = session.query(UsbDrive).filter_by(serial_no=delForm.serial_no.data).first()
            session.delete(usbdrive)
            session.commit()
        except SQLAlchemyError as e:
            print("exception")
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

@app.route('/targets', methods=['GET', 'POST'])
def manage_targets():
    # fetching from the database
    session = Session()
    target_objects = session.query(Target).all()

    # transforming into JSON-serializable objects
    schema = TargetSchema(many=True)
    targets = schema.dump(target_objects)

    # serializing as JSON
    session.close()

    addForm = addTargetForm()
    delForm = deleteTargetForm()

    return render_template('targets_mgmt.html', targets=targets, addForm=addForm, delForm=delForm)

@app.route('/addtarget', methods=['GET', 'POST'])
def add_targets():
    # fetching from the database
    session = Session()
    target_objects = session.query(Target).all()

    # transforming into JSON-serializable objects
    schema = TargetSchema(many=True)
    targets = schema.dump(target_objects)

    # serializing as JSON
    session.close()

    addForm = addTargetForm()
    delForm = deleteTargetForm()

    if addForm.validate_on_submit():
        target = Target(addForm.name.data, addForm.tgt_type.data, addForm.recommended_save_freq.data)
        session = Session()
        session.add(target)
        try :
            session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("erreur "+error)
        session.close()
        return redirect(url_for('manage_targets'))
    else:
        print(addForm.errors)

    return render_template('targets_mgmt.html', targets=targets, addForm=addForm, delForm=delForm)

@app.route('/deltarget', methods=['GET', 'POST'])
def del_targets():
    # fetching from the database
    session = Session()
    target_objects = session.query(Target).all()

    # transforming into JSON-serializable objects
    schema = TargetSchema(many=True)
    targets = schema.dump(target_objects)

    # serializing as JSON
    session.close()

    addForm = addTargetForm()
    delForm = deleteTargetForm()

    if delForm.validate_on_submit():
        session = Session()
        try :
            target = session.query(Target).filter_by(name=delForm.name.data).first()
            session.delete(target)
            session.commit()
        except SQLAlchemyError as e:
            print("exception")
        session.close()
        return redirect(url_for('manage_targets'))
    else:
        print(delForm.errors)

    return render_template('targets_mgmt.html', targets=targets, addForm=addForm, delForm=delForm)

@app.route('/tools', methods=['GET', 'POST'])
def manage_tools():
    # fetching from the database
    session = Session()
    tool_objects = session.query(Tool).all()

    # transforming into JSON-serializable objects
    schema = ToolSchema(many=True)
    tools = schema.dump(tool_objects)

    # serializing as JSON
    session.close()

    addForm = addToolForm()
    delForm = deleteToolForm()

    return render_template('tools_mgmt.html', tools=tools, addForm=addForm, delForm=delForm)

@app.route('/addtool', methods=['GET', 'POST'])
def add_tools():
    # fetching from the database
    session = Session()
    tool_objects = session.query(Tool).all()

    # transforming into JSON-serializable objects
    schema = ToolSchema(many=True)
    tools = schema.dump(tool_objects)

    # serializing as JSON
    session.close()

    addForm = addToolForm()
    delForm = deleteToolForm()

    if addForm.validate_on_submit():
        tool = Tool(addForm.tool.data, addForm.version.data)
        session = Session()
        session.add(tool)
        try :
            session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("erreur "+error)
        session.close()
        return redirect(url_for('manage_tools'))
    else:
        print(addForm.errors)

    return render_template('tools_mgmt.html', tools=tools, addForm=addForm, delForm=delForm)

@app.route('/deltool', methods=['GET', 'POST'])
def del_tools():
    # fetching from the database
    session = Session()
    tool_objects = session.query(Tool).all()

    # transforming into JSON-serializable objects
    schema = ToolSchema(many=True)
    tools = schema.dump(tool_objects)

    # serializing as JSON
    session.close()

    addForm = addToolForm()
    delForm = deleteToolForm()

    if delForm.validate_on_submit():
        session = Session()
        try :
            tool = session.query(Tool).filter_by(tool=delForm.tool.data, version=delForm.version.data).first()
            session.delete(tool)
            session.commit()
        except SQLAlchemyError as e:
            print("exception")
        session.close()
        return redirect(url_for('manage_tools'))
    else:
        print(delForm.errors)

    return render_template('tools_mgmt.html', tools=tools, addForm=addForm, delForm=delForm)

@app.route('/config')
def configuration():
    return render_template('config.html')