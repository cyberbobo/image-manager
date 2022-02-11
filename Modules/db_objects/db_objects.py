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

class Target(Entity, Base):
    __tablename__ = "target_machines"
    name = Column(String)
    tgt_type = Column(String)
    recommended_save_freq = Column(Integer)
    def __init__(self, name, tgt_type, recommended_save_freq):
        self.name = name
        self.tgt_type = tgt_type
        self.recommended_save_freq = recommended_save_freq

class TargetSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    tgt_type = fields.Str()
    recommended_save_freq = fields.Number()

class Tool(Entity, Base):
    __tablename__ = "saving_tools"
    tool = Column(String)
    version = Column(String)
    def __init__(self, tool, version):
        self.tool = tool
        self.version = version

class ToolSchema(Schema):
    id = fields.Number()
    tool = fields.Str()
    version = fields.Str()