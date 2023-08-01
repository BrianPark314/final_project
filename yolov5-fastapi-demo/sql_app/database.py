from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:////Users/Shark/Projects/final_project/yolov5-fastapi-demo/sql_app/db/pill_data.db" #set db url
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#create sqlalchemy engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#create the database class only, but not create instance
Base = declarative_base()