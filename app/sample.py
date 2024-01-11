from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Criminal, CriminalRecord, PoliceOfficer, CrimeScene
from datetime import datetime, date

def seed_data():
    # Create an SQLite database engine
    engine = create_engine('sqlite:///criminals.db')

    # Bind the engine to the Base class
    Base.metadata.bind = engine

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Sample Criminals
    criminal1 = Criminal(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        gender="Male",
        nationality="US",
        address="123 Main St, City",
        phone_number="555-1234",
        email="john.doe@example.com",
        wanted_level=3
    )

    criminal2 = Criminal(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1985, 5, 15),
        gender="Female",
        nationality="UK",
        address="456 Oak St, Town",
        phone_number="555-5678",
        email="jane.smith@example.com",
        wanted_level=5
    )

    session.add_all([criminal1, criminal2])
    session.commit()

    # Sample Criminal Records
    criminal_record1 = CriminalRecord(
        criminal=criminal1,
        crime_type="Robbery",
        crime_date=date(2020, 3, 10),
        description="Armed robbery at a convenience store",
        sentence="5 years imprisonment"
    )

    criminal_record2 = CriminalRecord(
        criminal=criminal2,
        crime_type="Fraud",
        crime_date=date(2019, 8, 20),
        description="Financial fraud scheme",
        sentence="3 years probation"
    )

    session.add_all([criminal_record1, criminal_record2])
    session.commit()

    # Sample Police Officers
    police_officer1 = PoliceOfficer(
        first_name="Officer",
        last_name="Johnson",
        badge_number="12345",
        rank="Detective",
        station="City Police Department"
    )

    police_officer2 = PoliceOfficer(
        first_name="Officer",
        last_name="Smith",
        badge_number="54321",
        rank="Sergeant",
        station="Town Police Department"
    )

    session.add_all([police_officer1, police_officer2])
    session.commit()

    # Sample Crime Scenes
    crime_scene1 = CrimeScene(
        location="Main Street",
        date=date(2020, 3, 10),
        description="Crime scene related to the robbery",
        investigating_officer=police_officer1,
        criminal_record=criminal_record1
    )

    crime_scene2 = CrimeScene(
        location="Oak Street",
        date=date(2019, 8, 20),
        description="Crime scene related to the fraud case",
        investigating_officer=police_officer2,
        criminal_record=criminal_record2
    )

    session.add_all([crime_scene1, crime_scene2])
    session.commit()

    print("Sample data added to the database.")

if __name__ == "__main__":
    seed_data()
