from user import User
from task import Task
from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))