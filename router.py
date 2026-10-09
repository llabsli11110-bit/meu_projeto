from fastapi import Depends,FastAPI,HTTPException, Header, Request
from pydantic import BaseModel,ConfigDict, EmailStr,Field
from security import verificacao_senha, hash_senha,criar_token 
from models import User,get_db 
from sqlalchemy.orm import  Session
from jose import JWTError, jwt
from security import verificar_token, verificacao_senha, hash_senha, criar_token
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timezone, timedelta
app = FastAPI()
tentativas_login ={}

class Cadastro(BaseModel):
    email:EmailStr 
    senha: str = Field(min_length=8) #garante que a senha tera no minimo 8 digitos
    nome:str
class Resposta(BaseModel): #modelo que sera devolvido na respostas 
    model_config = ConfigDict(from_attributes=True) #configura para pegar atributos do objeto e nao do dicionario
    id:int
    nome:str
    email:EmailStr 
class Login(BaseModel):
    email:EmailStr
    senha:str
limiter = Limiter(key_func=get_remote_address) 
app.state.limiter = limiter

@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, dados: Login, db: Session = Depends(get_db)):
    # --- Rate limit por email ---
    agora = datetime.now(timezone.utc)
    limite = agora - timedelta(minutes=1)
    
    tentativas = tentativas_login.get(dados.email, [])
    tentativas = [t for t in tentativas if t > limite]
    
    if len(tentativas) >= 5:
        raise HTTPException(status_code=429, detail="Muitas tentativas de login. Tente novamente mais tarde.")
    
    tentativas.append(agora)
    tentativas_login[dados.email] = tentativas
    
    # --- Lógica de login original, sem mudanças ---
    user = db.query(User).filter(User.email == dados.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="email ou senha invalidos")
    if not verificacao_senha(dados.senha, user.senha_hash):
        raise HTTPException(status_code=400, detail="email ou senha invalidos")
    token = criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
   
@app.get("/me", response_model=Resposta) #endpoint para pegar dados do usuario logado

def me(payload: dict = Depends(verificar_token), db: Session = Depends(get_db)):
    user =db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="usuario nao encontrado") 
    return user 

@app.post("/cadastro",response_model=Resposta) #endpoint/ filtra dados, da um ".stri()" gera documento Swagger
def cadastro(dados:Cadastro, db: Session = Depends(get_db)):
    user_existe = db.query(User).filter(User.email == dados.email).first()
    #procure na tabela usuarios , filtra onde email = email enviado , peguei o primeiro (firts)
    if user_existe:
        raise HTTPException (status_code= 400,detail="email ja cadastro")# se tiver achado alguem com msm email, retorna erro
    senha_hash = hash_senha(dados.senha) #senha vira bytes, bcryp gera o salt, que tbm gera o hash, hash vira string, retorna string segura
    novo_usuario = User (#cria objetos na memoria 
        nome=dados.nome,
        email = dados.email,
        senha_hash= senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario
