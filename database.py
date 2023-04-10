from sqlalchemy import create_engine

DATABASE_URL = "mysql://user:password@localhost/db_name"

engine = create_engine(DATABASE_URL)