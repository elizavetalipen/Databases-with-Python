# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.orm import backref
from datetime import datetime
from sqlalchemy import select
import pymysql 

Base = declarative_base()

class Organisation(Base):
     __tablename__ = 'organisations'
     
     idd = Column("org_id", Integer, primary_key=True)
     name = Column("org_name", String, nullable=False)
     purpose = Column("org_purpose", String, nullable=False)
     start_date = Column("start_date", DateTime, nullable=False)
     end_date = Column("end_date", DateTime, nullable=False)
     contr_type = Column("contr_type", String, nullable=True)
     
     def __repr__(self):
         return "<Organisation(id ='%s', name='%s', purpose='%s', start_date='%s', end_date='%s', contract='%s')>" \
             % (self.idd, self.name, self.purpose, self.start_date,self.end_date,self.contr_type)
    
class Department(Base):
     __tablename__ = 'deps'
     
     idd = Column("dep_id", Integer, primary_key=True)
     name = Column("dep_name", String, nullable=False)
     worker = relationship("Worker",back_populates="rel_department",cascade="all, delete, delete-orphan")
     
     def __repr__(self):
         return "<Department(id ='%s', name='%s')>" % (self.idd, self.name)
 
class LiveBlock(Base):
     __tablename__ = 'live_blocks'
     
     idd = Column("block_id", Integer, primary_key=True)
     people = Column("block_people", Integer)
     rooms = Column("block_rooms", Integer, nullable=False)
     worker = relationship("Worker", back_populates="rel_block",cascade="all, delete, delete-orphan")
     
     def __repr__(self):
         return "<LiveBlock(id ='%s', people='%s', rooms='%s')>" % (self.idd, self.people, self.rooms)
     
class Supplies(Base):
    __tablename__ = 'worker_supplies'
    
    worker_id = Column("ref_worker_id", Integer,ForeignKey('workers.worker_id'), primary_key = True)
    block = Column("ref_block_id", Integer)
    shower = Column("shower_time", Integer)
    water = Column("water_vol", Integer)
    food = Column("food_portions", Integer)
    gym = Column("gym", Integer)
    
    worker = relationship("Worker", back_populates="supplies",\
                          cascade="all, delete, delete-orphan",single_parent=True)
    def __repr__(self):
        return "<Supplies(worker_id ='%s', block_id='%s', shower_time = '%s',\
                water = '%s',food='%s', gym = '%s')>" % (self.worker_id, self.block,\
    self.shower, self.water, self.food, self.gym)
     
        
class Worker(Base):
    __tablename__ = 'workers'
    
    idd = Column("worker_id", Integer, primary_key=True)
    name = Column("worker_name", String)
    position = Column("worker_position", String)
    department = Column("ref_dep_id", Integer, ForeignKey('deps.dep_id'))
    block = Column("ref_block_id", Integer, ForeignKey('live_blocks.block_id'))
    
    # один-работник-ко-многим-отделам
    rel_block = relationship("LiveBlock", back_populates="worker")
    rel_department = relationship("Department", back_populates="worker")
    # один-к-одному
    contract = relationship("Contract", back_populates='worker',\
                             cascade="all, delete, delete-orphan", uselist=False)
    supplies = relationship("Supplies", back_populates='worker',\
                              cascade="all, delete, delete-orphan", uselist=False)
        
    def __repr__(self):
        return "<Worker(id ='%s', name='%s', position='%s', department='%s',block='%s')>"\
            % (self.idd, self.name, self.position, self.department, self.block)
   
class Medcard(Base):
     __tablename__ = 'medcard'
     
     idd = Column("card_id", Integer, primary_key=True)
     gender = Column("gender", String)
     birthday = Column("birthday", DateTime)
     age = Column("age", Integer)
     height = Column("height", Float)
     weight = Column("weight", Float)
     imt = Column("imt",Float)
     sugar = Column("sugar", Float)
     satur = Column("satur",Integer)
     temper = Column("temper",String)
     health = Column("health_points",Integer)
     
    
     def __repr__(self):
         return "<Medcard(id ='%s', gender='%s', birthday='%s', age='%s',Height='%s', Weight='%s', IMT='%s', Sugar='%s', Saturation='%s', Temper='%s',Health_Points='%s')>" \
             % (self.idd, self.gender, self.birthday, self.age,self.height,self.weight,\
                self.imt,self.sugar,self.satur,self.temper,self.health)
                 
class Contract(Base):
     __tablename__ = 'contracts'
     
     idd = Column("contr_id", Integer,ForeignKey('workers.worker_id'),primary_key=True)
     start_date = Column("start_date", DateTime)
     end_date = Column("end_date", DateTime)
     duration = Column("duration", Integer)
     contract = Column("contr_type", String)
     salary = Column("salary",Integer)
     ref_org = Column("ref_org_id",Integer)
     isOver = Column("isOver",Boolean)
     presentQ = Column("presentQ", Boolean)
     
     # relationships
     worker = relationship("Worker", back_populates="contract",\
                           cascade="all, delete, delete-orphan",single_parent=True)

     # representation
     def __repr__(self):
         return '''<Contract(id ='%s', start_date='%s', end_date='%s', duration='%s',type='%s', salary='%s', Organisation ='%s', OverQ = '%s', PresentQ = '%s' )>'''\
             % (self.idd, self.start_date,self.end_date,self.duration,\
                self.contract, self.salary, self.ref_org,self.isOver,self.presentQ)

             
