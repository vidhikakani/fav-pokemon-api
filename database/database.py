import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/edvora"
# DATABASE_URL = "postgresql://njyhztdsfgdunn:d8742da6d677874b3e51d43e254a05aefd44732e3c191c308edb5c57e8e06788@ec2-34-236-87-247.compute-1.amazonaws.com:5432/dd7c4nddvif0ca"
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()