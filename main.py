from fastapi import FastAPI
import os
from sqlalchemy import create_engine
from models import Base
from tasks import tasks

DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///voting.db')
app=FastAPI()
if '+asyncpg' in DATABASE_URL:
    DATABASE_URL=DATABASE_URL.replace('+asyncpg','')
engine=create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

app.include_router(tasks.router)