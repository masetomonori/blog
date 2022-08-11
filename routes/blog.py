from typing import List
from fastapi import APIRouter, Depends, status, Response
from schemas import Blog, ShowBlog, User, ShowUser
from database import get_db
from sqlalchemy.orm import Session
from functions import blog

router = APIRouter(prefix='/blog', tags=['blogs'])

@router.get('/', response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db:Session =  Depends(get_db)):
    return blog.delete(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db:Session =  Depends(get_db)):
    return blog.update(id, request, db)





