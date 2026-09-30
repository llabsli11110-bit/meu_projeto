import bcrypt
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
def hash_senha (senha:str)->str: #recebe tipo string e depois -> retorna string
    senha_bytes = senha.encode('utf-8') #convertendo para bytes 
    salt = bcrypt.gensalt(rounds=10)#gerando o salt 
    hash_bytes =  bcrypt.hashpw(senha_bytes,salt)# hash da senha com salt
    return hash_bytes.decode('utf-8') #salva como string
def verificacao_senha(userPassword: str, hash_salvo: str) -> bool:
    userbytes = userPassword.encode('utf-8')       # convertendo senha digitada para bytes
    hash_bytes = hash_salvo.encode('utf-8')        # convertendo hash salvo para bytes
    result = bcrypt.checkpw(userbytes, hash_bytes) # checando
    return result
secret_key = os.getenv("secret_key") #variavel de ambiente para a chave secreta
algorithm = os.getenv("algorithm") #variavel de ambiente para o algoritmo de hash
def criar_token(dados:dict) -> str: #cria token JWT
    payload = dados.copy()#copia do dicionário de dados para o payload do token
    agora = datetime.now(timezone.utc) #obtém a data e hora atual em UTC
    expiracao = agora + timedelta(minutes=30) #token expira em 30 minutos
    payload["iat"] = agora #adiciona a data de emissão ao payload
    payload["exp"] = expiracao #adiciona a data de expiração ao payload
    token = jwt.encode(payload, secret_key, algorithm=algorithm) #gera o token JWT
    return token #retorna o token gerado
