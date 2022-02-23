from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, utils, database
from ..schemas import user_schema

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.UserResponse
)
def create_user(user: user_schema.CreateUserBody, db: Session = Depends(database.get_db)):

    email = db.query(models.User).filter(
        models.User.email == user.email).first()
    if email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"account with email: {user.email} already exixts"
        )

    # hash the password -user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/{id}",
    response_model=user_schema.UserResponse
)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist"
        )
    return user
