from typing import Union
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model= List[schemas.PostOut])
def root(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Union[str, None] = ""):
    

    posts = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True
    ).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    new_post = models.Posts(**post.dict(), owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True
    ).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'post with id {id} not found'
        )
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unauthorised")
    
    post_query.delete()
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    old_post = post_query.first()

    if old_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'post with id {id} not found'
        )

    if old_post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unauthorised")

    post_query.update(post.dict())
    db.commit()

    return post_query.first()