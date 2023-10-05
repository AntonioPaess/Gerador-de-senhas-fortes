import random
import string
import sqlite3

# Saber se você quer consultar o banco de dados ou se você quer adicionar uma nova senha
entrada = int(input("Você deseja:\n[1] Gerar uma senha\n[2] Consultar suas senhas\n[3] Apagar senha\n=> "))

# Definir todos os caracteres especiais
caracteres = string.ascii_letters + string.digits + string.punctuation

#Embaralhar esses caracteres
caracteres_embaralhados = list(caracteres)
random.shuffle(caracteres_embaralhados)

# Criando a senha aleatoria
senha_gerada = "".join(random.choice(caracteres_embaralhados)for _ in range(26))

# Conectar ao banco de dados ou criar um se não existe
conexao = sqlite3.connect("senhas.db")

# Criar uma tabela para armazenar senhas
cursor = conexao.cursor()
cursor.execute("""
     CREATE TABLE IF NOT EXISTS senhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200) NOT NULL,
        senha TEXT NOT NULL
 )
              """)

# Inserir uma senha no banco de dados
def inserir_senha(nome, senha):
    cursor.execute("INSERT INTO senhas (nome, senha) VALUES (?,?)", (nome, senha))
    conexao.commit()

# Função para apagar todas as senhas antigas no banco de dados
def apagar_senha_por_id(id_senha):
    cursor.execute("DELETE FROM senhas WHERE id = ?", (id_senha,))
    conexao.commit()

# Consultar senhas no banco de dados
def consultar_senha():
    cursor.execute("SELECT * FROM senhas")
    return cursor.fetchall()

# Inserir uma senha nova
if entrada == 1:
    nome = input("Digite o site no qual deseja adicionar: ").title()
    inserir_senha(nome, senha_gerada)
    senhas = consultar_senha()
    print(f"Senha: {senha_gerada}")
elif entrada == 2: # Consultar senhas
    senhas = consultar_senha()
    for senha in senhas:
        print(f"ID: {senha[0]}, Site: {senha[1]}, Senha: {senha[2]}")
else: # Apagar senha
    senhas = consultar_senha()
    for senha in senhas:
        print(f"ID: {senha[0]}, Site: {senha[1]}, Senha: {senha[2]}")
    
    Id_a_apagar = int(input("Digite o ID da senha que deseja apagar: "))
    apagar_senha_por_id(Id_a_apagar)

    senha_atualizadas = consultar_senha()
    for senha in senha_atualizadas:
        print(f"ID: {senha[0]}, Site: {senha[1]}, Senha: {senha[2]}")



# Fechar conexão com o banco de dados quando terminar
conexao.close()


