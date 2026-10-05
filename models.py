
from sqlalchemy import Integer, String, create_engine, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship  # atenção: é 'relationship', não 'relationships'
import bcrypt
from dotenv import load_dotenv #biblioteca para ler variaveis de ambiente do .env
import os
from sqlalchemy.orm import Session
load_dotenv() #carrega as variaveis de ambiente do .env para o ambiente de execução do Python, permitindo acessar as variaveis usando os.getenv()

database_url = os.getenv("database_url") #variavel de ambiente para a url do banco de dados

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)  # use nome diferente para a factory

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

# Aqui você precisa também do modelo User atualizado para o relacionamento funcionar:
class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100), index=True,unique=True)
    senha_hash = Column(String(255))
    tasks = relationship("Task", back_populates="user", cascade="all, delete, delete-orphan")
    
class Task(Base):
    __tablename__ = "tasks"  # plural é melhor para tabelas, mas pode ser singular

    id = Column(Integer, primary_key=True)
    descricao = Column(String(100))  
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # FK para tabela 'usuarios'
    user = relationship("User", back_populates="tasks")  # relacionamento com User
    
print('Criando tabela')
Base.metadata.create_all(bind=engine)
print('Tabela criada')