import bcrypt
def senha (senha):
    
    bytes = senha.encode('utf-8') #convertendo para bytes 
    salt = bcrypt.gensalt()#gerando o salt 
    hash =  bcrypt.hashpw(bytes,salt)# hash da senha com salt
    return hash
def verificação (userPassword,hash):
    
    userbytes = userPassword.encode('utf-8') #convertendo para bytes
    result = bcrypt.checkpw(userbytes,hash) #checando se bate com a outra senha
    return result
hash_gerado = senha('lucas478')
print('hash > ' ,hash_gerado)
print('senha correta? ', verificação('lucas123',hash_gerado))
