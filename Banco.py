import sqlite3

# Função para criar uma conexão com o banco de dados
def conectar_banco():
    return sqlite3.connect("banco.db")

# Função para criar a tabela de contas bancárias
def criar_tabela():
    # Conecta ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()

    # Cria a tabela 'contas' se ela ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            numero_conta INTEGER PRIMARY KEY,
            nome_titular TEXT NOT NULL,
            senha TEXT NOT NULL,
            saldo REAL NOT NULL DEFAULT 0
        )
    """)

    # Salva as alterações no banco de dados e fecha a conexão
    conn.commit()
    conn.close()

# Função para criar uma conta bancária
def criar_conta():
    # Solicita informações do usuário
    nome_titular = input("Digite o nome do titular da conta: ")
    senha = input("Digite a senha: ")

    # Conecta ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()

    # Insere os dados da conta na tabela 'contas'
    cursor.execute("INSERT INTO contas (nome_titular, senha) VALUES (?, ?)", (nome_titular, senha))

    # Salva as alterações no banco de dados e fecha a conexão
    conn.commit()
    conn.close()

# Função para verificar o saldo de uma conta bancária
def verificar_saldo():
    # Solicita informações do usuário
    numero_conta = int(input("Digite o número da conta: "))
    senha = input("Digite a senha: ")

    # Conecta ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()

    # Executa a consulta SQL para obter o saldo da conta
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ? AND senha = ?", (numero_conta, senha))
    saldo = cursor.fetchone()

    # Exibe o saldo ou uma mensagem de erro caso a conta não seja encontrada ou a senha esteja incorreta
    if saldo:
        print(f"Saldo: R$ {saldo[0]:.2f}")
    else:
        print("Conta não encontrada ou senha incorreta.")

    # Fecha a conexão com o banco de dados
    conn.close()

# Função para depositar dinheiro em uma conta bancária
def depositar_dinheiro():
    # Solicita informações do usuário
    numero_conta = int(input("Digite o número da conta: "))
    senha = input("Digite a senha: ")
    valor_deposito = float(input("Digite o valor a ser depositado: "))

    # Conecta ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()

    # Executa a atualização do saldo na tabela 'contas' após o depósito
    cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero_conta = ? AND senha = ?", (valor_deposito, numero_conta, senha))

    # Verifica se a operação foi bem-sucedida e exibe uma mensagem correspondente
    if cursor.rowcount > 0:
        print("Depósito realizado com sucesso.")
    else:
        print("Conta não encontrada ou senha incorreta.")

    # Salva as alterações no banco de dados e fecha a conexão
    conn.commit()
    conn.close()

# Função para sacar dinheiro de uma conta bancária
def sacar_dinheiro():
    # Solicita informações do usuário
    numero_conta = int(input("Digite o número da conta: "))
    senha = input("Digite a senha: ")
    valor_saque = float(input("Digite o valor a ser sacado: "))

    # Conecta ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()

    # Obtém o saldo atual da conta
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ? AND senha = ?", (numero_conta, senha))
    saldo = cursor.fetchone()

    # Verifica se a conta e a senha são válidas e se o saldo é suficiente para o saque
    if saldo:
        saldo_atual = saldo[0]
        if saldo_atual >= valor_saque:
            # Atualiza o saldo na tabela 'contas' após o saque
            cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero_conta = ? AND senha = ?", (valor_saque, numero_conta, senha))
            print("Saque realizado com sucesso.")
        else:
            print("Saldo insuficiente.")
    else:
        print("Conta não encontrada ou senha incorreta.")

    # Salva as alterações no banco de dados e fecha a conexão
    conn.commit()
    conn.close()

# Função para encerrar o programa
def encerrar_atendimento():
    print("Atendimento encerrado.")
    exit()

# Função para exibir o menu
def exibir_menu():
    print("\n===== MENU =====")
    print("1. Criar conta")
    print("2. Verificar saldo")
    print("3. Depositar dinheiro")
    print("4. Sacar dinheiro")
    print("5. Encerrar atendimento")

# Função principal do programa
def main():
    # Cria a tabela de contas bancárias (se ainda não existir)
    criar_tabela()

    # Loop para exibir o menu e executar as operações selecionadas pelo usuário
    while True:
        exibir_menu()
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            criar_conta()
        elif opcao == 2:
            verificar_saldo()
        elif opcao == 3:
            depositar_dinheiro()
        elif opcao == 4:
            sacar_dinheiro()
        elif opcao == 5:
            encerrar_atendimento()
        else:
            print("Opção inválida. Digite um número entre 1 e 5.")

if _name_ == "_main_":
    main()
