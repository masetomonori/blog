from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import models
from hashing import Hash
from schemas import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail=f'User with the id {id} is not available')
    
    return user

def create_user(request: User, db: Session):

    #new_user = models.User(name = request.name,
    #                       email= request.email,
    #                       password = Hash.bcrypt(request.password))
    new_user = models.User(name = request.name,
                           email= request.email,
                           password = pwd_context.hash(request.password))


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user