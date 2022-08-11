from schemas import Blog
import models
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(blog:Blog, db: Session):
    # user_idをハードコーディング
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id="1")
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id: int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return 'Deletion complete'

def update(id, request: Blog, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not found')

    # orm_mode = True が効いていない
    #db.query(models.Blog).filter(models.Blog.id == id).update(request)
    blog.update(request.dict())
    db.commit()

    return 'Update completed'

#def show(id: int, response: Response):
def show(id: int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
              detail=f'Blog with the id {id} is not available')
    return blog


