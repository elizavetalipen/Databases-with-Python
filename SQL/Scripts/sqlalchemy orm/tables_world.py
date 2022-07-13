from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.orm import backref
from datetime import datetime
from sqlalchemy import select
import pymysql 

Base = declarative_base()

metadata = MetaData()

class City(Base):
    __tablename__ = 'city'
     
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(35), nullable=False)
    countrycode = Column("countrycode", String(3), ForeignKey('country.code'), nullable=False)
    district = Column("district", String(20), nullable=False)
    population = Column("population", Integer, nullable=False)

    sells_sell = relationship("Country", back_populates="sell_sells")

    def __repr__(self):
        return "<City(id ='%s', name ='%s', countrycode='%s', district='%s', population='%s')>" \
            % (self.id, self.name, self.countrycode, self.district, self.population)


class CountryLanguage(Base):
    __tablename__ = 'countrylanguage'
     
    countrycode = Column("countrycode", String(3), ForeignKey('country.code'), nullable=False)
    language = Column("language", String(30), primary_key=True)
    isofficial = Column("isofficial", String(1), nullable=False)
    percentage = Column("percentage", Float(4,1), nullable=False)

    pr_des = relationship("Country", back_populates="des_pr", cascade="all, delete, delete-orphan",single_parent=True)
     
    def __repr__(self):
        return "<CountryLanguage(countrycode ='%s', language ='%s', isofficial='%s', percentage='%s')>" \
            % (self.countrycode, self.language, self.isofficial, self.percentage)


class Country(Base):
    __tablename__ = 'country'
     
    code = Column("code", String(3), primary_key=True)
    name = Column("name", String(52), nullable=False)
    continent = Column("continent", String(20), nullable=False)
    region = Column("region", String(26), nullable=False)
    surfacearea = Column("surfacearea", Float(10,2), nullable=False)
    indepyear = Column("indepyear", Float(1,6), nullable=False)
    population = Column("population", Integer, nullable=False)
    lifeexpectancy = Column("lifeexpectancy", Float(3,1), nullable=False)
    gnp = Column("gnp", Float(10,2), nullable=False)
    gnpold = Column("gnpold", Float(10,2), nullable=False)
    localname = Column("localname", String(45), nullable=False)
    governmentform = Column("governmentform", String(45), nullable=False)
    headofstate = Column("headofstate", String(60), nullable=False)
    capital = Column("capital", Integer, nullable=False)
    code2 = Column("code2", String(2), nullable=False)

    sell_sells= relationship("City", back_populates="sells_sell", cascade="all, delete, delete-orphan")
    des_pr = relationship("CountryLanguage", back_populates='pr_des', cascade="all, delete, delete-orphan", uselist=False)
     
    def __repr__(self):
        return "<Country(code ='%s', name ='%s', continent ='%s', region ='%s', surfacearea ='%s', indepyear ='%s', population ='%s', lifeexpectancy ='%s', gnp ='%s', gnpold ='%s', localname ='%s', governmentform ='%s', headofstate ='%s', capital ='%s', code2 ='%s')>" \
            % (self.code, self.name, self.continent, self.region, self.surfacearea, self.indepyear, self.population, self.lifeexpectancy, self.gnp, self.gnpold, self.localname, self.governmentform, self.headofstate, self.capital, self.code2)

