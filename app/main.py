from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import psycopg2.extras
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


my_posts = [
    {"id": 1, "title": "Post 1 title", "content": "content for post 1"},
    {"id": 2, "title": "Post 2 title", "content": "content for post 2"},
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def read_root():
    return {"Introduction to": "FastAPI"}


@app.get("/posts")
def get_posts():
    # Open a cursor to perform database operations
    cur.execute(""" SELECT * FROM posts """)
    # Retrieve query results
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute(
        """ INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    conn.commit()
    new_post = cur.fetchone()

    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):

    cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cur.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} is not available",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id:{id} is not available"}
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    post = cur.fetchone()
    conn.commit()

    if post == None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cur.execute(
        """ UPDATE posts SET title = %s , content = %s ,published = %s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    post = cur.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    return {"data": post}
