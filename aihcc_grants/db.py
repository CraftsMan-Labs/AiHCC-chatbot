from sqlalchemy import create_engine, Column, String, Integer, Text, Table, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Grant(Base):
    __tablename__ = 'grants'
    id = Column(Integer, primary_key=True)
    grant_name = Column(String, nullable=False)
    grant_url = Column(String, nullable=True)
    grant_amount = Column(String, nullable=True)
    submission_timeline = Column(String, nullable=True)
    application_process = Column(Text, nullable=True)
    grant_category = Column(String, nullable=True)
    sponsor = Column(String, nullable=True)
    additional_info = Column(Text, nullable=True)
    domain = Column(String, nullable=True)
    
    conditions = Column(Text, nullable=True)
    eligibility_criteria = Column(Text, nullable=True)
    unusual_conditions = Column(Text, nullable=True)

# Create an SQLite database
engine = create_engine('sqlite:///grants.db')
Base.metadata.create_all(engine)