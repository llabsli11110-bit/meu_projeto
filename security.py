import bcrypt
from jose import jwt, JWTError
import os
from dotenv import load_dotenv 
from datetime import datetime, timedelta, timezone
from fastapi import Depends,HTTPException, Header
def hash_senha (senha:str)->str: 
    senha_bytes = senha.encode('utf-8') 
    salt = bcrypt.gensalt(rounds=10) #gerar  salt 
    hash_bytes =  bcrypt.hashpw(senha_bytes,salt)# hash da senha com salt
    return hash_bytes.decode('utf-8') #salva como string
def verificacao_senha(userPassword: str, hash_salvo: str) -> bool:
    userbytes = userPassword.encode('utf-8')       
    hash_bytes = hash_salvo.encode('utf-8')        
    result = bcrypt.checkpw(userbytes, hash_bytes) 
    return result
load_dotenv() # carrega as variáveis de ambiente do .env
secret_key = os.getenv("secret_key") 
Algorithm = os.getenv("algorithm") 
def criar_token(dados:dict) -> str: 
    payload = dados.copy()
    agora = datetime.now(timezone.utc) 
    expiracao = agora + timedelta(minutes=30)
    payload["iat"] = agora #adiciona a data de emissão ao payload
    payload["exp"] = expiracao #adiciona a data de expiração ao payload
    token = jwt.encode(payload, secret_key, algorithm=Algorithm) 
    return token 
def verificar_token(authorization:str = Header(...)):
    try:
        token = authorization.replace("Bearer ","") 
        payload = jwt.decode(token, secret_key, algorithms=[Algorithm]) 
    except JWTError:
        raise HTTPException(status_code=400, detail="token invalido") 