import random
import string
import sqlite3
import bcrypt

# Conectar ao novo banco de dados para usuários
conn = sqlite3.connect("seubanco.db")
cursor = conn.cursor()

# Criação de tabela do usuário no banco de dados
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_usuario VARCHAR(150) NOT NULL,
               pin_hash TEXT NOT NULL
)
               """)
conn.commit()
conn.close()

# Função para registrar um novo usuário com o PIN
def registrar_usuario(nome_usuario, pin):
    conn = sqlite3.connect('seubanco.db')
    cursor = conn.cursor()

    # Crie um hash do PIN usando bcrypt
    pin_hash = bcrypt.hashpw(pin.encode(), bcrypt.gensalt())

    # Insira o novo usuário e o hash do PIN no banco de dados
    cursor.execute("INSERT INTO usuarios (nome_usuario, pin_hash) VALUES (?, ?)", (nome_usuario, pin_hash))

    conn.commit()
    conn.close()

# Função para verificar o PIN de um usuário
def verificar_pin(nome_usuario, pin):
    conn = sqlite3.connect('seubanco.db')
    cursor = conn.cursor()

   # Dentro da função verificar_pin, antes de verificar o PIN
    cursor.execute("SELECT pin_hash, id FROM usuarios WHERE nome_usuario = ?", (nome_usuario,))
    resultado = cursor.fetchone()

    if resultado is not None:
        pin_hash = resultado[0]  # Obtenha o hash do PIN do banco de dados
        return resultado[1]  # Retorna o ID do usuário se o PIN estiver correto
    else:
        print("PIN incorreto. Acesso negado.")
        return None  # Retorna None se o PIN estiver incorreto

conn.close()
   

# Definir todos os caracteres especiais
caracteres = string.ascii_letters + string.digits + string.punctuation

#Embaralhar esses caracteres
caracteres_embaralhados = list(caracteres)
random.shuffle(caracteres_embaralhados)

# Criando a senha aleatoria
senha_gerada = "".join(random.choice(caracteres_embaralhados)for _ in range(26))

# Conectar ao banco de dados ou criar um se não existe
conexao = sqlite3.connect("senhas.db")

# Criar uma tabela para armazenar senhas (se não existir)
cursor = conexao.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS senhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200) NOT NULL,
        senha TEXT NOT NULL
    )
""")

# Verificar se a coluna id_usuario existe
cursor.execute("PRAGMA table_info(senhas)")
columns = [column[1] for column in cursor.fetchall()]

if "id_usuario" not in columns:
    # A coluna id_usuario não existe, então adicione-a
    cursor.execute("ALTER TABLE senhas ADD COLUMN id_usuario INTEGER")


# Inserir uma senha no banco de dados
def inserir_senha(id_usuario, nome, senha):
    cursor.execute("INSERT INTO senhas (id_usuario, nome, senha) VALUES (?, ?, ?)", (id_usuario, nome, senha))
    conexao.commit()

# Função para apagar todas as senhas antigas no banco de dados
def apagar_senha_por_id(id_senha):
    cursor.execute("DELETE FROM senhas WHERE id = ?", (id_senha,))
    conexao.commit()

# Consultar senhas no banco de dados
def consultar_senha():
    cursor.execute("SELECT * FROM senhas")
    return cursor.fetchall()

# Função para listar senhas por usuário
def listar_senhas_por_usuario(id_usuario):
    conn = sqlite3.connect("senhas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM senhas WHERE id_usuario = ?", (id_usuario,))
    senhas = cursor.fetchall()

    conn.close()

    return senhas

# Menu principal
while True:
    print("Bem-vindo ao seu gerenciador de senhas!")
    print("[1] Registrar um novo usuário")
    print("[2] Entrar com um usuário existente")
    print("[3] Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome_usuario = input("Digite um nome de usuário: ")
        pin = input("Digite um PIN: ")

        # Registrar o novo usuário
        registrar_usuario(nome_usuario, pin)
        print("Usuário registrado com sucesso!")

    elif escolha == "2":
        nome_usuario = input("Digite seu nome de usuário: ")
        pin = input("Digite seu PIN: ")

        # Verificar o PIN do usuário
        id_usuario = verificar_pin(nome_usuario, pin)

        if id_usuario is not None:
                # Loop do menu do usuário
            while True:
                print("Menu do usuário:")
                print("[1] Gerar uma senha")
                print("[2] Consultar suas senhas")
                print("[3] Apagar senha")                    
                print("[4] Sair do menu do usuário")

                escolha_usuario = input("Escolha uma opção: ")

                if escolha_usuario == "1":
                    if id_usuario is not None:
                        nome = input("Digite o site no qual deseja adicionar: ").title()
                        inserir_senha(id_usuario, nome, senha_gerada)  # Passe o id_usuario como o primeiro argumento
                        print(f"Senha gerada: {senha_gerada} e associada ao site: {nome}")
                    else:
                        print("Acesso negado. PIN incorreto ou usuário não encontrado.")
                elif escolha_usuario == "2": # Consultar senhas
                    senhas = listar_senhas_por_usuario(id_usuario)  # Use id_usuario em vez de nome_usuario
                    for senha in senhas:
                            print(f"ID: {senha[0]}, Site: {senha[2]}, Senha: {senha[3]}")
                elif escolha_usuario == "3":  # Apagar senha
                    senhas = listar_senhas_por_usuario(id_usuario)  # Use id_usuario em vez de nome_usuario
                    for senha in senhas:
                        print(f"ID: {senha[0]}, Site: {senha[2]}, Senha: {senha[3]}")

                        Id_a_apagar = int(input("Digite o ID da senha que deseja apagar: "))
                        apagar_senha_por_id(Id_a_apagar)
                elif escolha_usuario == "4":
                    break  # Sair do menu do usuário
                else:
                    print("Escolha inválida. Tente novamente.")
    elif escolha == "3":
        print("Obrigado por usar o gerenciador de senhas!")
        break
    else:
        print("Escolha inválida. Tente novamente.")

# Fechar conexão com o banco de dados quando terminar
conexao.close()


