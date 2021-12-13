from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
import psycopg2.extras
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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


@app.get("/")
def read_root():
    return {"Introduction to": "FastAPI"}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cur.execute(
    #     """ INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # conn.commit()
    # new_post = cur.fetchone()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    # cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} is not available",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id:{id} is not available"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # post = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):

    # cur.execute(
    #     """ UPDATE posts SET title = %s , content = %s ,published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # post = cur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    post_query.update(
        updated_post.dict(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,  db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user