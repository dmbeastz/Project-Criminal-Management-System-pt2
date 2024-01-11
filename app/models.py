from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

import datetime


engine = create_engine('sqlite:///criminals.db')

Base = declarative_base()


class Criminal(Base):
    __tablename__ = 'criminals'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    nationality = Column(String)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String)
    wanted_level = Column(Integer)

    criminal_records = relationship("CriminalRecord", back_populates="criminal")

class CriminalRecord(Base):
    __tablename__ = 'criminal_records'

    id = Column(Integer, primary_key=True)
    criminal_id = Column(Integer, ForeignKey('criminals.id'))
    crime_type = Column(String)
    crime_date = Column(Date)
    description = Column(String)
    sentence = Column(String)

    criminal = relationship("Criminal", back_populates="criminal_records")
    crime_scenes = relationship("CrimeScene", back_populates="criminal_record")

class PoliceOfficer(Base):
    __tablename__ = 'police_officers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    badge_number = Column(String)
    rank = Column(String)
    station = Column(String)

    crime_scenes = relationship("CrimeScene", back_populates="investigating_officer")

class CrimeScene(Base):
    __tablename__ = 'crime_scenes'

    id = Column(Integer, primary_key=True)
    location = Column(String)
    date = Column(Date)
    description = Column(String)
    investigating_officer_id = Column(Integer, ForeignKey('police_officers.id'))
    criminal_record_id = Column(Integer, ForeignKey('criminal_records.id'))

    investigating_officer = relationship("PoliceOfficer", back_populates="crime_scenes")
    criminal_record = relationship("CriminalRecord", back_populates="crime_scenes")
