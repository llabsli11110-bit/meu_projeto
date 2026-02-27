from fastapi import FastAPI
from pydantic import BaseModel, EmailStr,Field
from security import verificação, senha #importação do codigo hash
app = FastAPI()
class User (BaseModel):
    name:str
class cadastro(BaseModel):#baseModel cria um modelo de dados usando Pydantic , valida dados automaticamente, gera doc automatica 
    #do Swagger , retorna 422 se algo tiver errado
    email:EmailStr #garante que um email seja email
    senha: str = Field(min_length=8) #garante que a senha tera no minimo 8 digitos
# 1. Rota Raiz (Boas-vindas)
@app.get("/")
def root():
    return {"message": "Hello World"}

# 2. Rota de Saúde (Health Check)
# Importante para servidores saberem se sua API está "viva"
@app.get("/health")
def health():
    return {"status": "online", "user": "Lucas"}

# 3. Rota de Teste (POST com Parâmetro)
@app.post("/login")
def login(dados:cadastro):
    return {
        "email_recebido":dados.email,
        "mensagem":"Login sucesso"
    }