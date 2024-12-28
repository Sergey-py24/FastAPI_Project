from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.backend.db import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    priority = 0
    completed = False
    user_id = Column(Integer, ForeignKey('users.id'))
    slug = Column(String, unique=True, index=True)
    user = relationship('User', back_populates='tasks')
