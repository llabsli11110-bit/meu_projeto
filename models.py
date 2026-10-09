
from sqlalchemy import Integer, String, create_engine, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship  
import bcrypt
from dotenv import load_dotenv 
import os
from sqlalchemy.orm import Session
load_dotenv() 

database_url = os.getenv("database_url") 

engine = create_engine(database_url, echo=True)

SessionLocal = sessionmaker(bind=engine)  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100), index=True,unique=True)
    senha_hash = Column(String(255))
    tasks = relationship("Task", back_populates="user", cascade="all, delete, delete-orphan")
    
class Task(Base):
    __tablename__ = "tasks"  

    id = Column(Integer, primary_key=True)
    descricao = Column(String(100))  
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # FK para tabela 'usuarios'
    user = relationship("User", back_populates="tasks")  # relacionamento com User
    
print('Criando tabela')
Base.metadata.create_all(bind=engine)
print('Tabela criada')