from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"Introduction to": "FastAPI"}


@app.get("/posts")
def get_posts():
    return {"Here are your": "FastAPI posts"}


@app.post("/createpost")
def create_posts(payload: dict=Body(...)):
    print(payload)
    return {"message": f"title {payload['title']} content: {payload['content']}"}