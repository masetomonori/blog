from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import models, token_man
from schemas import Login
from database import get_db
from sqlalchemy.orm import Session
from hashing import Hash
from passlib.context import CryptContext

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email ==
           request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail = f'Invalid Credentials')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail = f'Incorrect password')

    access_token = token_man.create_access_token(
        data={"sub": user.email, "id" : user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    