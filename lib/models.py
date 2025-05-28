from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company', overlaps="companyfreebies,devs,devfreebies")
    devs = relationship('Dev', secondary='freebies', back_populates='companies', overlaps="companyfreebies,devs,devfreebies,company")

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev', overlaps="devs,companyfreebies,devfreebies")
    companies = relationship('Company', secondary='freebies', back_populates='devs', overlaps="devfreebies,companyfreebies,devs,devfreebies,freebies")

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies', overlaps="devs,devfreebies,companies")
    company = relationship('Company', back_populates='freebies', overlaps="companyfreebies,devs,devfreebies,companies")

    def print_details(self):
        dev_name = self.dev.name if self.dev else "Unknown Dev"
        company_name = self.company.name if self.company else "Unknown Company"
        return f"{dev_name} owns a {self.item_name} from {company_name}"
