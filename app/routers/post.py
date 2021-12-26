from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


@router.get("/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


@router.get("/{id}", response_model=schemas.Post)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.Post)
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
