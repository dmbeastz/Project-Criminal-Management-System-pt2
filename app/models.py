import click
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import date

engine = create_engine('sqlite:///criminals.db')
Base = declarative_base()
Base.metadata.bind = engine

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


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--first-name', prompt='First Name', help='First name of the criminal.')
@click.option('--last-name', prompt='Last Name', help='Last name of the criminal.')
@click.option('--date-of-birth', prompt='Date of Birth', type=click.DateTime(formats=['%Y-%m-%d']), help='Date of birth of the criminal (YYYY-MM-DD).')
@click.option('--gender', prompt='Gender', help='Gender of the criminal.')
@click.option('--nationality', prompt='Nationality', help='Nationality of the criminal.')
@click.option('--address', prompt='Address', help='Address of the criminal.')
@click.option('--phone-number', prompt='Phone Number', help='Phone number of the criminal.')
@click.option('--email', prompt='Email', help='Email address of the criminal.')
@click.option('--wanted-level', prompt='Wanted Level', type=int, help='Wanted level of the criminal.')
def add_criminal(first_name, last_name, date_of_birth, gender, nationality, address, phone_number, email, wanted_level):
    criminal = Criminal(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        nationality=nationality,
        address=address,
        phone_number=phone_number,
        email=email,
        wanted_level=wanted_level
    )
    session.add(criminal)
    session.commit()
    click.echo(f"Criminal {first_name} {last_name} added successfully.")

@cli.command()
@click.option('--id', prompt='Criminal ID', type=int, help='ID of the criminal to delete.')
def delete_criminal(id):
    criminal = session.query(Criminal).get(id)
    if criminal:
        session.delete(criminal)
        session.commit()
        click.echo(f"Criminal with ID {id} deleted successfully.")
    else:
        click.echo(f"No criminal found with ID {id}.")

@cli.command()
def list_criminals():
    criminals = session.query(Criminal).all()
    if criminals:
        click.echo("List of Criminals:")
        for criminal in criminals:
            click.echo(f"{criminal.id}. {criminal.first_name} {criminal.last_name}")
    else:
        click.echo("No criminals found.")
    

@cli.command()
@click.option('--criminal-id', prompt='Criminal ID', type=int, help='ID of the criminal for whom the record is added.')
@click.option('--crime-type', prompt='Crime Type', help='Type of crime.')
@click.option('--crime-date', prompt='Crime Date', type=click.DateTime(formats=['%Y-%m-%d']), help='Date of the crime (YYYY-MM-DD).')
@click.option('--description', prompt='Description', help='Description of the crime.')
@click.option('--sentence', prompt='Sentence', help='Sentence for the crime.')
def add_criminal_record(criminal_id, crime_type, crime_date, description, sentence):
    criminal = session.query(Criminal).get(criminal_id)
    if criminal:
        criminal_record = CriminalRecord(
            criminal=criminal,
            crime_type=crime_type,
            crime_date=crime_date,
            description=description,
            sentence=sentence
        )
        session.add(criminal_record)
        session.commit()
        click.echo(f"Criminal Record added successfully.")
    else:
        click.echo(f"No criminal found with ID {criminal_id}. Please check and try again.")

@cli.command()
@click.option('--id', prompt='Criminal Record ID', type=int, help='ID of the criminal record to delete.')
def delete_criminal_record(id):
    criminal_record = session.query(CriminalRecord).get(id)
    if criminal_record:
        session.delete(criminal_record)
        session.commit()
        click.echo(f"Criminal Record with ID {id} deleted successfully.")
    else:
        click.echo(f"No criminal record found with ID {id}.")


@cli.command()
def list_criminal_records():
    criminal_records = session.query(CriminalRecord).all()
    if criminal_records:
        click.echo("List of Criminal Records:")
        for record in criminal_records:
            click.echo(f"{record.id}. {record.criminal.first_name} {record.criminal.last_name}: {record.crime_type}")
    else:
        click.echo("No criminal records found.")

@cli.command()
@click.option('--first-name', prompt='First Name', help='First name of the police officer.')
@click.option('--last-name', prompt='Last Name', help='Last name of the police officer.')
@click.option('--badge-number', prompt='Badge Number', help='Badge number of the police officer.')
@click.option('--rank', prompt='Rank', help='Rank of the police officer.')
@click.option('--station', prompt='Station', help='Police station of the officer.')
def add_police_officer(first_name, last_name, badge_number, rank, station):
    police_officer = PoliceOfficer(
        first_name=first_name,
        last_name=last_name,
        badge_number=badge_number,
        rank=rank,
        station=station
    )
    session.add(police_officer)
    session.commit()
    click.echo(f"Police Officer {first_name} {last_name} added successfully.")

@cli.command()
@click.option('--id', prompt='Police Officer ID', type=int, help='ID of the police officer to delete.')
def delete_police_officer(id):
    police_officer = session.query(PoliceOfficer).get(id)
    if police_officer:
        session.delete(police_officer)
        session.commit()
        click.echo(f"Police Officer with ID {id} deleted successfully.")
    else:
        click.echo(f"No police officer found with ID {id}.")

@cli.command()
def list_police_officers():
    police_officers = session.query(PoliceOfficer).all()
    if police_officers:
        click.echo("List of Police Officers:")
        for officer in police_officers:
            click.echo(f"{officer.id}. {officer.first_name} {officer.last_name}, Badge Number: {officer.badge_number}")
    else:
        click.echo("No police officers found.")


@cli.command()
@click.option('--location', prompt='Location', help='Location of the crime scene.')
@click.option('--date', prompt='Date', type=click.DateTime(formats=['%Y-%m-%d']), help='Date of the crime scene (YYYY-MM-DD).')
@click.option('--description', prompt='Description', help='Description of the crime scene.')
@click.option('--investigating-officer-id', prompt='Investigating Officer ID', type=int, help='ID of the investigating police officer.')
@click.option('--criminal-record-id', prompt='Criminal Record ID', type=int, help='ID of the related criminal record.')
def add_crime_scene(location, date, description, investigating_officer_id, criminal_record_id):
    investigating_officer = session.query(PoliceOfficer).get(investigating_officer_id)
    criminal_record = session.query(CriminalRecord).get(criminal_record_id)

    if investigating_officer and criminal_record:
        crime_scene = CrimeScene(
            location=location,
            date=date,
            description=description,
            investigating_officer=investigating_officer,
            criminal_record=criminal_record
        )
        session.add(crime_scene)
        session.commit()
        click.echo(f"Crime Scene added successfully.")
    else:
        click.echo("Invalid Investigating Officer ID or Criminal Record ID. Please check and try again.")

@cli.command()
@click.option('--id', prompt='Crime Scene ID', type=int, help='ID of the crime scene to delete.')
def delete_crime_scene(id):
    crime_scene = session.query(CrimeScene).get(id)
    if crime_scene:
        session.delete(crime_scene)
        session.commit()
        click.echo(f"Crime Scene with ID {id} deleted successfully.")
    else:
        click.echo(f"No crime scene found with ID {id}.")

@cli.command()
def list_crime_scenes():
    crime_scenes = session.query(CrimeScene).all()
    if crime_scenes:
        click.echo("List of Crime Scenes:")
        for scene in crime_scenes:
            click.echo(f"{scene.id}. Location: {scene.location}, Date: {scene.date}, Description: {scene.description}")
    else:
        click.echo("No crime scenes found.")

if __name__ == '__main__':
    cli()
