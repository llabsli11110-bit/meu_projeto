
from sqlalchemy import Integer, String, create_engine, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship  # atenção: é 'relationship', não 'relationships'

database_url = "mysql+mysqlconnector://root:L14%40cas%242026@localhost:3306/cadastro"

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)  # use nome diferente para a factory
session = Session()  # cria a sessão para usar

Base = declarative_base()

# Aqui você precisa também do modelo User atualizado para o relacionamento funcionar:
class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100), index=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete, delete-orphan")
    
class Task(Base):
    __tablename__ = "tasks"  # plural é melhor para tabelas, mas pode ser singular

    id = Column(Integer, primary_key=True)
    descricao = Column(String(100))  # corrigido typo 'descrisao' para 'descricao'
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # FK para tabela 'usuarios'

    user = relationship("User", back_populates="tasks")  # relacionamento com User


print('Criando tabela')
Base.metadata.create_all(bind=engine)
print('Tabela criada')