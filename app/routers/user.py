
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.backend.db_depends import get_db
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from slugify import slugify


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    all_usr = db.scalars(select(User)).all()
    if len(all_usr) > 0:
        return all_usr
    else:
        raise HTTPException(status_code=404, detail="No users found")


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalar(select(User).where(user_id == User.id))
    if usr is None:
        raise HTTPException(status_code=404, detail="User not found")
    return usr


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_usr: CreateUser):
    db.execute(insert(User).values(username=create_usr.username,
                                   firstname=create_usr.first_name,
                                   lastname=create_usr.last_name,
                                   age =create_usr.age,
                                   slug=slugify(create_usr.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful', 'message': 'User created successfully'}


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], update_usr: UpdateUser, user_id: int):
    usr = db.scalar(select(User).where(user_id == User.id))
    if usr is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(update(User).where(user_id == User.id).values(firstname=update_usr.first_name,
                                                                lastname=update_usr.last_name,
                                                                age =update_usr.age))
    db.commit()
    return {'status_code': status.HTTP_202_ACCEPTED,
            'transaction': 'Successful', 'message': 'User updated successfully'}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalar(select(User).where(user_id == User.id))
    tasks_delete = db.scalars(select(Task).where(user_id == Task.user_id)).all()
    if usr is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(delete(User).where(user_id == User.id))
    if tasks_delete:
        db.execute(delete(Task).where(user_id == Task.user_id))
    db.commit()
    return {'status_code': status.HTTP_202_ACCEPTED,
                'transaction': 'Successful', 'message': 'User deleted successfully'}

@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(user_id == User.id))
    tasks = db.scalars(select(Task).where(user_id == Task.user_id)).all()
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    return tasks




