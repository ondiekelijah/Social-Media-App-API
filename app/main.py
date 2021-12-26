from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
import psycopg2.extras
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="ondie",
        )
        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("Connected to a database!")
        break

    except Exception as error:
        print("Error connecting to the database")
        print("Error ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)




@app.get("/")
def read_root():
    return {"Introduction to": "FastAPI"}





