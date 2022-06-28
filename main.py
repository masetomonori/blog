from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog
from models import Base
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return "hello"

@app.post('/blog')
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not available')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'detail': f'Blog with the id {id} is not available'}
    return blog

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog:Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.bldy)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db:Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not found')

    #db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    blog.delete(synchronize_session=False)
    db.commit()

    return 'Deletion complete'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
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

