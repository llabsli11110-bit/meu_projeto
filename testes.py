from sqlalchemy import Integer, String, create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse  # Importante para tratar caracteres especiais na senha

# 1. Trate a senha se ela tiver caracteres especiais como @ ou $
password = urllib.parse.quote_plus("L14@cas$2026")
database_url = f"mysql+pymysql://root:{password}@localhost:3306/cadastro"

# 2. Configuração do Engine e Sessão
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# 3. Definição do Modelo
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    email = Column(String(100), index=True)

# 4. Criação das tabelas no banco (Correção do erro de digitação aqui)
Base.metadata.create_all(bind=engine)

print("Tabela criada com sucesso!")