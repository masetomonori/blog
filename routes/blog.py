from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog, User, ShowUser
from database import get_db
import models
from sqlalchemy.orm import Session

router = APIRouter(prefix='/blog', tags=['blogs'])




@router.get('/', response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not available')
    return blog

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog:Blog, db: Session = Depends(get_db)):
    # user_idをハードコーディング
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id="1")
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db:Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return 'Deletion complete'

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db:Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not found')

    # orm_mode = True が効いていない
    #db.query(models.Blog).filter(models.Blog.id == id).update(request)
    blog.update(request.dict())
    db.commit()

    return 'Update completed'





