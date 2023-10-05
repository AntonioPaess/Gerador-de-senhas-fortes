# Meu primeiro Projeto
---
## Esse é um projeto de um gerador de senhas fortes
    Antes de mais nada acho que devo fazer um breve resumo do que esse projeto faz.
    Basicamente ele gera senhas fortes e as guardas em um banco de dados para que você possa
    futuramente caso esqueça a senha rever-lá e também você tem a possibilidade de apagar elas
    e gerar novas senhas fortes para suas novas contas.
---
## Esse código basicamente é feito baseado em três bibliotecas do Python sendo elas:
    -> Random
    -> String
    -> Sqlite3
---

# O que eu fiz com essas 3 bibliotecas?
    Basicamente utilizei a String e a random para gerarem as senhas utilizando 
    os comandos:
    string.ascii_letters -> Representa todas as letras maiúsculas e minúsculas;
    string.digits -> Representa todos os dígitos(números); 
    string.punctuation -> Representa dos os caracteres especiais.
    random.shuffle -> Foi usado para embaralhar os caracteres na string;
    random.choice -> Foi usado para escolher aleatoriamente caracteres da lista embaralhada.
---

# A biblioteca Sqlite3:
    Eu realmente não tinha ideia de que era possível realizar a criação de um banco de dados
    utilizando uma biblioteca no Python por isso tive que recorrer ao chatgpt e perguntar
    como criar um banco de dados utilizando Python e assim ele me indicou essa biblioteca
    na qual tive que parar e estudar e ainda tenho que estudar mais pois tiveram muitos 
    erros que o chatgpt me ajudaram. Em resumo o Chat gpt é muito bom para o aprendizado e 
    assim foi minha jornada utilizando essa biblioteca. Agora vou falar o comandos que utilizei dela:
---

    conexao = sqlite3.connect("senhas.db") -> A linha conexao = sqlite3.connect("senhas.db")  está criando uma conexão com um banco de dados SQLite chamado "senhas.db". 
    Vamos analisar o que cada parte dessa linha faz:

    sqlite3: Isso indica que você está usando o módulo sqlite3 em Python. Esse módulo fornece funcionalidades para trabalhar com bancos de dados SQLite.

    .connect("senhas.db"): Este é um método do módulo sqlite3 que cria uma conexão com um banco de dados SQLite. O argumento "senhas.db" 
    especifica o nome do arquivo do banco de dados que será usado para armazenar os dados.

    Portanto, essa linha de código estabelece uma conexão com o banco de dados "senhas.db" e armazena essa conexão na variável conexao.
    A partir desse ponto, você pode usar a variável conexao para executar consultas SQL, inserir dados, atualizar registros e realizar outras operações no banco de dados SQLite. 
---
    cursor = conexao.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS senhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200) NOT NULL,
        senha TEXT NOT NULL
 )
    """) -> Essas linhas de código estão sendo usadas para criar uma tabela chamada "senhas" no banco de dados SQLite, caso ela não exista. 
            Vamos analisar cada parte:

cursor = conexao.cursor(): Aqui, você está criando um objeto de cursor que permite executar comandos SQL no banco de dados. 
O cursor é uma parte essencial ao trabalhar com bancos de dados SQLite, 
pois você o utiliza para enviar consultas e comandos para o banco de dados.

cursor.execute(...):

O método execute é chamado no objeto de cursor.
Dentro do método execute, você fornece uma string SQL que contém a instrução de criação da tabela. 
Essa string é definida em várias linhas para facilitar a leitura e a manutenção do código.
A instrução SQL em si faz o seguinte:

CREATE TABLE IF NOT EXISTS senhas: Isso cria uma tabela chamada "senhas" se ela ainda não existir. 
O IF NOT EXISTS garante que a tabela só será criada se ainda não estiver presente no banco de dados.

(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(200) NOT NULL, senha TEXT NOT NULL): 
Essa parte define a estrutura da tabela. Ela consiste em três colunas:

id: É uma coluna do tipo INTEGER que será a chave primária da tabela. A cláusula PRIMARY KEY indica que esta coluna será usada como chave primária, 
garantindo que cada registro tenha um valor de ID exclusivo. O AUTOINCREMENT significa que o 
ID será gerado automaticamente com um valor único para cada novo registro inserido na tabela.
nome: É uma coluna do tipo VARCHAR(200), que pode armazenar strings de até 200 caracteres. 
A cláusula NOT NULL indica que esta coluna não pode conter valores nulos (ou seja, sempre deve ter um valor).
senha: É uma coluna do tipo TEXT, que pode armazenar strings mais longas, como senhas. Também possui a cláusula NOT NULL.
Portanto, essas linhas de código criam a estrutura da tabela "senhas" no banco de dados SQLite, com colunas para ID, nome e senha. 
Se a tabela já existir, o comando CREATE TABLE IF NOT EXISTS garante que nenhuma alteração seja feita na estrutura existente.

---

def inserir_senha(nome, senha):

    cursor.execute("INSERT INTO senhas (nome, senha) VALUES (?,?)", (nome, senha))

    conexao.commit()

def apagar_senha_por_id(id_senha):

    cursor.execute("DELETE FROM senhas WHERE id = ?", (id_senha,))

    conexao.commit()

def consultar_senha():

    cursor.execute("SELECT * FROM senhas")

    return cursor.fetchall()
    
    
## Essas linhas de código definem três funções que operam no banco de dados SQLite. Vamos descrever cada função individualmente:

    inserir_senha(nome, senha): Esta função é responsável por inserir uma nova senha no banco de dados. 
    Ela recebe dois argumentos: nome (que representa o nome/site/conta) e senha (que representa a senha a ser inserida).

    cursor.execute("INSERT INTO senhas (nome, senha) VALUES (?, ?)", (nome, senha)): Isso executa uma instrução SQL para inserir um novo registro na tabela "senhas". 
    Ele insere os valores nome e senha nas colunas correspondentes. O uso de placeholders ? é uma forma segura de evitar ataques de SQL Injection.

    conexao.commit(): Após a execução da instrução SQL, você chama commit() na conexão para confirmar a transação no banco de dados. 
    Isso garante que a nova senha seja realmente inserida no banco de dados.

    apagar_senha_por_id(id_senha): Esta função é responsável por apagar uma senha específica com base no seu ID. 
    Ela recebe um argumento id_senha, que é o ID da senha que você deseja excluir.

    cursor.execute("DELETE FROM senhas WHERE id = ?", (id_senha,)): 
    Isso executa uma instrução SQL que exclui a senha com o ID correspondente da tabela "senhas".

    conexao.commit(): Assim como na função inserir_senha, 
    você chama commit() para confirmar a exclusão no banco de dados.

    consultar_senha(): Esta função é responsável por consultar 
    todas as senhas no banco de dados e retorná-las como uma lista de tuplas.

    cursor.execute("SELECT * FROM senhas"): Isso executa uma instrução 
    SQL que seleciona todos os registros da tabela "senhas".

    cursor.fetchall(): Isso recupera todas as linhas resultantes da consulta e 
    retorna uma lista de tuplas, onde cada tupla representa um registro da tabela.

    Essas funções juntas permitem que você insira novas senhas, apague senhas existentes com base em seus 
    IDs e consulte todas as senhas armazenadas no banco de dados SQLite. Elas são úteis para gerenciar as operações de CRUD 
    (Criar, Ler, Atualizar e Deletar) em um banco de dados de senhas.

---

    conexao.close() -> A linha de código conexao.close() é responsável por fechar a conexão com o banco de dados SQLite. 
    Ela é importante por vários motivos:

    Liberação de Recursos: Quando você abre uma conexão com um banco de dados, ela consome recursos do sistema, como memória e CPU. 
    Fechar a conexão permite que esses recursos sejam liberados, evitando o uso desnecessário de recursos do sistema.

    Consistência de Dados: Fechar a conexão garante que todas as transações pendentes sejam concluídas e confirmadas no banco de dados. 
    Isso ajuda a manter a consistência dos dados no banco de dados.

    Evitar Bloqueio de Recursos: Em alguns sistemas de gerenciamento de banco de dados, manter uma conexão aberta por um longo período pode 
    levar ao bloqueio de recursos, impedindo que outros processos ou aplicativos acessem o banco de dados. Fechando a conexão quando não 
    é mais necessária, você evita bloqueios de recursos.

    Boa Prática de Programação: É uma boa prática de programação fechar todas as conexões 
    com bancos de dados ou recursos externos quando você terminar de usá-los. 
    Isso ajuda a evitar vazamentos de recursos e problemas de desempenho.

    Se você não fechar a conexão com o banco de dados, algumas consequências podem ocorrer:

    Vazamento de Recursos: A conexão permanecerá aberta e consumindo recursos do sistema, 
    o que pode levar a problemas de desempenho e recursos esgotados.

    Possíveis Problemas de Bloqueio: Em sistemas de gerenciamento de banco de dados mais complexos, 
    a conexão não fechada pode bloquear recursos, impedindo o acesso de outros processos 
    ou aplicativos ao banco de dados.

    Instabilidade: Se o seu programa mantiver muitas conexões abertas ao longo do tempo sem fechá-las, 
    isso pode levar a problemas de estabilidade e desempenho do seu aplicativo.

    Portanto, é altamente recomendável sempre fechar a conexão com o banco de dados (ou qualquer recurso externo) 
    quando você terminar de usá-lo para garantir que seus recursos sejam liberados e que seu 
    programa funcione de maneira eficiente e consistente.
--- 

## Basicamente é isso! Caso queiram ajudar fiquem a vontade sou iniciante ainda em Python e estou treinando, queria transformar isso em um aplicativo porém ainda não tenho conhecimento no momento. Obrigado desde já a todos que decidirem me ajudar para atualizar esse gerador de senhas para sua versão 2.0





