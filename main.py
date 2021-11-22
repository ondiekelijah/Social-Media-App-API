from fastapi import FastAPI,Response,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"id": 1,"title": "Post 1 title", "content": "content for post 1"},
    {"id": 2,"title": "Post 2 title", "content": "content for post 2"},
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
def read_root():
    return {"Introduction to": "FastAPI"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int,response:Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message":f"post with id:{id} is not available"}
    return {"data": post}