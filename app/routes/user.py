from typing import List
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from .. import utils, models, schemas, database



router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# changed function name get_users to signup for easy understanding
@router.post('/', response_model=List[schemas.UserOutput])
def sign_up(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    # Hash The Password
    hashed_pass = utils.hash_pass(user.password)

    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return [new_user]

@router.get('/{id}', response_model=schemas.UserOutput)
def getoneuser(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} doesnt exist")
    return (user)
