from operator import mod
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, utils, database, oauth2
from ..schemas import post_schema


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get(
#     "/",
#     response_model=List[post_schema.PostResponse]
# )
@router.get(
    "/",
    response_model=List[post_schema.MainPostResponse]
)
def get_posts(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=post_schema.PostResponse
)
def create_posts(
    post: post_schema.CreatePostBody,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    new_post = models.Post(owner_id=current_user.id, **
                           post.dict())  # create post

    db.add(new_post)  # add post to db
    db.commit()  # commit changes
    db.refresh(new_post)  # refresh to set new post back to variable new_post

    return new_post


@router.get(
    "/{id}",
    response_model=post_schema.MainPostResponse
)
def get_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    return post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}"
)
def update_post(
    id: int,
    updated_post: post_schema.CreatePostBody,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform requested action"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
