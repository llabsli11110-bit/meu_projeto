from sqlalchemy import Integer, String, create_engine,Column
# Função que cria conexão com o banco de dados por meio da criação de um engine (objeto de configuração e gerenciador de conexões)
# Column define colunas da tabela no modelo ORM (estrutura da tabela) e também define restrições (constraints)
# Integer define o tipo da coluna como inteiro
# String define o tipo da coluna para armazenamento de texto (similar a VARCHAR)
from sqlalchemy.orm import sessionmaker,declarative_base
# sessionmaker configura como as sessões serão criadas; a Session resultante executa operações CRUD e controla transações
# declarative_base cria a classe base para modelos ORM, permitindo definir tabelas como classes Python
database_url = "mysql+mysqlconnector://root:L14%40cas%242026@localhost:3306/cadastro"
# URL de conexão com o banco de dados MySQL, contendo usuário, senha, host, porta e nome do banco
engine = create_engine(database_url)
# Criação do engine com base no banco de dados definido na URL
session = sessionmaker (bind=engine)
# Fábrica para criar sessões ligadas ao engine criado
session = session()
#cria uma sessão pronto pra trabalha com o bd naquele momento , usado para interagir com o bd, para executar opeações
#a partir da fábrica sessionmaker que você definiu antes com session = sessionmaker(bind=engine)
Base = declarative_base()
# Criação da base para declaração dos modelos ORM
class User(Base):
    # Definição da classe que representa a tabela no banco de dados
    __tablename__ = "usuarios"
    # Nome da tabela no banco de dados
    id = Column(Integer,primary_key=True)
    # Coluna 'id' do tipo inteiro, chave primária
    nome = Column(String(100))
    # Coluna 'nome' do tipo texto com tamanho máximo 100
    email = Column(String(100),index=True)
    # Coluna 'email' do tipo texto com índice para otimizar buscas
Base.metadata.create_all(bind=engine)# Cria todas as tabelas declaradas
#no banco de dados conforme os modelos definidos
# Para executar o script, use no terminal: python nome_arquivo.py
