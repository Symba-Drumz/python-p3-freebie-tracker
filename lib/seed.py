from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///lib/freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Use Base to create tables if they don't exist
Base.metadata.create_all(engine)

def seed():
    # Clear existing data
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    # Create companies
    company1 = Company(name="TechCorp", founding_year=1990)
    company2 = Company(name="InnovateLLC", founding_year=1985)
    session.add_all([company1, company2])
    session.commit()

    # Create devs
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")
    session.add_all([dev1, dev2])
    session.commit()

    # Create freebies
    freebie1 = Freebie(item_name="Sticker", value=5, dev=dev1, company=company1)
    freebie2 = Freebie(item_name="T-Shirt", value=20, dev=dev1, company=company2)
    freebie3 = Freebie(item_name="Mug", value=10, dev=dev2, company=company1)
    session.add_all([freebie1, freebie2, freebie3])
    session.commit()

if __name__ == "__main__":
    seed()
