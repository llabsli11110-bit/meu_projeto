from fastapi import FastAPI,HTTPException# retorna erro do http personalizado
from pydantic import BaseModel,ConfigDict, EmailStr,Field
from security import verificacao_senha, hash_senha,criar_token #importação do codigo hash
from models import User,session #model do SQLAlchemy ., session conxeão ativa com bd
app = FastAPI() #chama a API

class Cadastro(BaseModel):#baseModel cria um modelo de dados usando Pydantic , valida dados automaticamente, gera doc automatica 
    #do Swagger , retorna 422 se algo tiver errado
    email:EmailStr #garante que um email seja email
    senha: str = Field(min_length=8) #garante que a senha tera no minimo 8 digitos
    nome:str
class Resposta(BaseModel): #modelo que sera devolvido na respostas 
    model_config = ConfigDict(from_attributes=True) #configura para pegar atributos do objeto e nao do dicionario
    id:int
    nome:str
    email:EmailStr #sem senha
class Login(BaseModel):
    email:EmailStr
    senha:str
@app.post("/login") #endpoint de login
def login(dados:Login):
    user = session.query(User).filter(User.email == dados.email).first() #procura usuario com email enviado
    if not user:
        raise HTTPException(status_code=400, detail="email ou senha invalidos") #se nao achar, retorna erro
    if not verificacao_senha(dados.senha, user.senha_hash): #verifica se senha digitada bate com hash salvo
        raise HTTPException(status_code=400, detail="email ou senha invalidos") #se nao bater, retorna erro
    token = criar_token({"sub":user.email}) #cria token JWT com email do usuario como assunto (sub)
    return {"access_token": token, "token_type": "bearer"} #retorna o token para o cliente
  
@app.post("/cadastro",response_model=Resposta) #endpoint/ filtra dados, da um ".stri()" gera documento Swagger
def cadastro(dados:Cadastro): 
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