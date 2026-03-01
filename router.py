from fastapi import FastAPI,HTTPException# retorna erro do http personalizado
from pydantic import BaseModel, EmailStr,Field
from security import verificação_senha, hash_senha #importação do codigo hash
from models import User,session #model do SQLAlchemy ., session conxeão ativa com bd
app = FastAPI() #chama a API

class cadastro(BaseModel):#baseModel cria um modelo de dados usando Pydantic , valida dados automaticamente, gera doc automatica 
    #do Swagger , retorna 422 se algo tiver errado
    email:EmailStr #garante que um email seja email
    senha: str = Field(min_length=8) #garante que a senha tera no minimo 8 digitos
    name:str
class Resposta(BaseModel): #modelo que sera devolvido na respostas 
    id:int
    nome:str
    Email:EmailStr #sem senha
class configuracao :  
    from_attributes = True  #fastAPI converte automaticamente objeto para JSON
@app.post("/cadastro",response_model=Resposta) #endpoint/ filtra dados, da um ".stri()" gera documento Swagger
def cadastro(dados:cadastro): 
    user_existe = session.query(User).filter(User.email == dados.email).first()
    #procure na tabela usuarios , filtra onde email = email enviado , peguei o primeiro (firts)
    if user_existe:
        raise HTTPException (status_code= 400,detail="email ja cadastro")# se tiver achado alguem com msm email, retorna erro
    senha_hash = hash_senha(dados.senha) #senha vira bytes, bcryp gera o salt, que tbm gera o hash, hash vira string, retorna string segura
    novo_usuario = User (#cria objetos na memoria 
        nome=dados.nome,
        email = dados.email,
        senha_hash= senha_hash
    )
    session.add(novo_usuario)#colcoa objeto na sessão
    session.commit()#insert no bd 
    session.refresh(novo_usuario)#atualiza o objeto com o bd 
    return novo_usuario