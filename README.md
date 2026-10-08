# API Login/Cadastro

API de integração de login/cadastro com banco de dados.

## Funcionalidades
- Cadastro de usuário
- Login com JWT
- Hash de senha com bcrypt

## Tecnologias usadas
FastAPI, SQLAlchemy, MySQL, bcrypt, Pydantic, JWT (python-jose)

## Como rodar o projeto
1. Clonar o repositório
2. Criar e ativar um ambiente virtual (`.venv`)
3. Instalar as dependências: `pip install -r requirements.txt`
4. Copiar `.env.example` para `.env` e preencher com os dados reais
5. Criar o banco no MySQL (apenas o banco — as tabelas a API cria automaticamente ao iniciar)
6. Rodar: `uvicorn router:app --reload`

## Endpoints disponíveis
- `POST /cadastro` — cria um novo usuário (nome, email, senha) e retorna id/nome/email
- `POST /login` — valida email e senha com base no cadastro, retorna um token JWT

## Estrutura do projeto
- `models.py` — criação do banco de dados, tabelas e colunas configuradas
- `router.py` — execução da API, classes, funções e verificações para cadastro e login
- `security.py` — criação de hash para senhas, verificação de senhas e criação de JWT para login

## Decisões técnicas relevantes
- Senhas salvas em hash (nunca em texto puro) usando bcrypt, para evitar vazamento de dados sensíveis
- JWT assinado com o algoritmo HS256, para autenticação após o login
- Sessão do banco criada por requisição (via `Depends`), em vez de uma sessão global, evitando conflito entre requisições simultâneas
- Coluna `email` com constraint `UNIQUE` no banco, além da verificação no código, como camada extra contra duplicidade
- `.env` no `.gitignore` para evitar vazamento de chaves e senhas; `.env.example` como modelo das variáveis necessárias
