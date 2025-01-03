from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    all_tsk = db.scalars(select(Task)).all()
    if len(all_tsk) > 0:
        return all_tsk
    else:
        raise HTTPException(status_code=404, detail="No tasks found")



@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    tsk = db.scalar(select(Task).where(task_id == Task.id))
    if tsk is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return tsk


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task_: CreateTask, user_id: int):
    usr = db.scalar(select(User).where(user_id == User.id))
    if usr is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(insert(Task).values(title=create_task_.title,
                                   content=create_task_.content,
                                   priority=create_task_.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task_.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful', 'message': 'Task created successfully'}


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], update_tsk: UpdateTask, task_id: int):
    tsk = db.scalar(select(Task).where(task_id == Task.id))
    if tsk is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute(update(Task).where(task_id == Task.id).values(title=update_tsk.title,
                                                             content=update_tsk.content,
                                                             priority=update_tsk.priority))
    return {'status_code': status.HTTP_202_ACCEPTED,
            'transaction': 'Successful', 'message': 'Task updated successfully'}


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tsk = db.scalar(select(Task).where(task_id == Task.id))
    if tsk is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute(delete(Task).where(task_id == Task.id))
    db.commit()
    return {'status_code': status.HTTP_202_ACCEPTED,
                'transaction': 'Successful', 'message': 'Task deleted successfully'}
