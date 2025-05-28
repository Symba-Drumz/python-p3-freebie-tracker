import ipdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///lib/freebies.db')
Session = sessionmaker(bind=engine)
session = Session()


_ = Base
_ = Company
_ = Dev
_ = Freebie


ipdb.set_trace()
