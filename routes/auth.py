from fastapi import APIRouter, Depends, status, HTTPException
import models
from schemas import Login
from database import get_db
from sqlalchemy.orm import Session
from hashing import Hash
from passlib.context import CryptContext

router = APIRouter(tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/login')
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email ==
           request.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail = f'Invalid Credentials')
    
    #if not Hash.verify(user.password, request.password):
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail = f'Incorrect password')
       
    return user