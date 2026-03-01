import bcrypt
def hash_senha (senha:str)->str:
    senha_bytes = senha.encode('utf-8') #convertendo para bytes 
    salt = bcrypt.gensalt()#gerando o salt 
    hash_bytes =  bcrypt.hashpw(senha_bytes,salt)# hash da senha com salt
    return hash_bytes.decode('utf-8') #salva como string
def verificação_senha (userPassword,hash):
    
    userbytes = userPassword.encode('utf-8') #convertendo para bytes
    result = bcrypt.checkpw(userbytes,hash) #checando se bate com a outra senha
    return result
