from models import Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

engine = create_engine('sqlite:///lib/freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

def test_give_freebie_invalid_dev():
    company = Company(name="TestCo", founding_year=2000)
    session.add(company)
    session.commit()
    # dev is None
    try:
        company.give_freebie(None, "Item", 10)
        assert False, "Expected exception for None dev"
    except Exception:
        pass

def test_oldest_company_empty_db():
    # Clear companies
    session.query(Company).delete()
    session.commit()
    assert Company.oldest_company(session) is None

def test_received_one_no_freebies():
    dev = Dev(name="TestDev")
    session.add(dev)
    session.commit()
    assert not dev.received_one("NonExistentItem")

def test_give_away_not_owned_freebie():
    dev1 = Dev(name="Dev1")
    dev2 = Dev(name="Dev2")
    company = Company(name="TestCo", founding_year=2000)
    freebie = Freebie(item_name="Item", value=10, dev=dev1, company=company)
    session.add_all([dev1, dev2, company, freebie])
    session.commit()
    # dev2 tries to give away freebie not owned by them
    dev2.give_away(dev1, freebie)
    # freebie.dev should remain dev1
    assert freebie.dev == dev1

def test_print_details_missing_relations():
    freebie = Freebie(item_name="Item", value=10, dev=None, company=None)
    # Should not raise exception
    details = freebie.print_details()
    assert "Unknown" in details

if __name__ == "__main__":
    pytest.main()
