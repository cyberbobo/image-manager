from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields

db_url = 'localhost:3306'
db_name = 'image_mgr'
db_user = 'dba_image-manager'
db_password = 'image-manager'
engine = create_engine(f'mysql+mysqldb://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
    id = Column(Integer, primary_key=True)

class UsbDrive(Entity, Base):
    __tablename__ = "usb_drives"
    serial_no = Column(String)
    def __init__(self, serial_no):
        self.serial_no = serial_no

class UsbDriveSchema(Schema):
    id = fields.Number()
    serial_no = fields.Str()