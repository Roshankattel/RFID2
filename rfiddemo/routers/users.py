
from fastapi import status, HTTPException, Depends, APIRouter
from database import SessionLocal
import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    # hash the password - user tag data
    # user.tag_data = utils.hash(user.tag_data)
    new_user = models.User(**user.dict())
    SessionLocal.add(new_user)
    SessionLocal.commit()
    SessionLocal.refresh(new_user)
    return new_user

@router.put("/{id}",response_model=schemas.UserResponse)
def update_user(id: int, updated_user: schemas.UserCreate):
    user_query  = SessionLocal.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} does not exit")
    user_query.update(updated_user.dict(),synchronize_session=False)
    SessionLocal.commit()
    return user_query.first()

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int):

    user = SessionLocal.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} was not found")
    return user
