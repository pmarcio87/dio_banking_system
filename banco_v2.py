# Criar funções para as funções de depósito, saque e extrato
# Criar nova função para cadastrar usuário (cliente)
# Criar nova função para cadastrar conta bancária
# Função saque deve receber os argumentos apenas pelo nome
# Função depósito deve receber os argumentos apenas por posição
# Função extrato deve receber os argumentos por posição e nome - argumentos posicionais: saldo / argumentos nomeados: extrato
# Função de criar usuário deve armazenar usuários em uma lista, contendo nome (string), DOB(string), CPF(string - não pode ser repetido) e endereço (string no formato "logradouro - nro - bairro - cidade/sigla estado")
# Função criar conta deve armazenar contas em uma lista. Uma conta é composta por agência (número fixo: "0001"), número da conta (sequencial iniciando em 1) e usuário (pode ter mais de uma conta, porém cada conta pertence a somente 1 usuário).

import textwrap

def menu():
    word = 'MENU'
    print(f"\n{word.center(21, '=')}")
    menu = """
    [n] Cadastrar Novo Cliente
    [c] Cadastrar Nova Conta
    [lc] Listar Contas
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    return input(textwrap.dedent(menu))


def sacar(*, saque, conta):

    conta["saldo"] -= saque
    print(f"Saque de R${saque:.2f} realizado. Seu saldo atual é de R${conta["saldo"]:.2f}.")
    conta["extrato"].append(f"Saque de R${saque:.2f}")
    conta["num_saques"] += 1


def depositar(deposito, conta, /):
    
    conta["saldo"] += deposito
    print(f"Depósito realizado. Seu saldo atual é de R${conta["saldo"]:.2f}")
    conta["extrato"].append(f"Depósito de R${deposito:.2f}")    


def extrato(conta):

    word = 'EXTRATO'
    print(f"\n{word.center(21, '=')}")
    if len(conta["extrato"]) == 0:
        print("Não foram realizadas operações")
    else:
        num_operacao = 1
        for operacao in conta["extrato"]:
            print(f"Operação {num_operacao}: {operacao}")
            num_operacao +=1
            
    print(f"\n\nSeu saldo é de R${conta["saldo"]:.2f}")
    print("="*21)


def criar_cliente(nome, dob, cpf, end):

    cliente = {}
    cliente["nome"] = nome
    cliente["dob"] = dob
    cliente["cpf"] = cpf
    cliente["endereco"] = end
    cliente["contas"] = []

    return cliente


def criar_conta(num_conta, cpf, agencia):

    conta = {}
    conta["agencia"] = agencia
    conta["numero"] = num_conta
    conta["cpf_cliente"] = cpf
    conta["saldo"] = 0
    conta["extrato"] = []
    conta["num_saques"] = 0

    return conta
    

def main():
    LIMITE_SAQUES = 3
    LIMTIE_POR_SAQUE = 500
    AGENCIA = "0001"

    clientes = []
    contas = []
    cpf_clientes = []
    num_conta = 1


    while True:

        opcao = menu()

        if opcao == "n":
            cpf = input("Digite o CPF (apenas números, sem pontos ou traço): ")

            if cpf in cpf_clientes:
                print("Cliente já cadastrado")
                continue
            
            nome = input("Digite o nome completo: ")
            dob = input("Digite a data de nascimento (formato DD/MM/YY): ")
            logradouro = input("Digite a rua da residência: ")
            nro_end = input("Digite o número da residência: ")
            bairro = input("Digite o bairro: ")
            cidade = input("Digite a cidade: ")
            estado = input("Digite a sigla do estado: ")

            endereco = f"{logradouro} - {nro_end} - {bairro} - {cidade}/{estado}"

            novoCliente = criar_cliente(nome=nome, dob=dob, cpf=cpf, end=endereco)
            
            cpf_clientes.append(cpf)
            clientes.append(novoCliente)

            print(f"Cadastro de {nome} concluído com sucesso")

        elif opcao == "lc":
            for conta in contas:
                print(conta)

        elif opcao == "c":
            cpf = input("Digite o CPF (apenas números, sem ponto ou traço): ")

            if cpf not in cpf_clientes:
                print("Cliente não cadastrado. Selecione N para cadastrar novo cliente")
                continue

            novaConta = criar_conta(num_conta=num_conta, cpf=cpf, agencia=AGENCIA)
            
            for cliente in clientes:
                if cliente["cpf"] == cpf:
                    cliente["contas"].append(num_conta)

            contas.append(novaConta)
            num_conta += 1
            print(f"Conta cadastrada com sucesso")
     
        elif opcao == "d":
            nro_conta = int(input("Digite o número da conta bancária: "))
            saldo = 0

            if nro_conta > num_conta:
                print("Conta não cadastrada")
                continue

            deposito_check = True
            while deposito_check:

                deposito = int(input("Digite o valor que deseja depositar: "))

                if deposito <= 0:
                    print("Digite um valor inteiro maior que zero")
                    continue

                for conta in contas:
                    if conta["numero"] == nro_conta:
                        depositar(deposito, conta)
                
                deposito_check = False

        elif opcao == "s":
            nro_conta = int(input("Digite o número da conta bancária: "))

            if nro_conta > num_conta:
                print("Conta não cadastrada")
                continue
                        
            saque_check = True
            while saque_check:

                for conta in contas:
                    if conta["numero"] == nro_conta:
                        if conta["num_saques"] >= LIMITE_SAQUES:
                            print("Número máximo de saques diários atingido. Volte amanhã!")
                            saque_check = False
                            break
                        else:
                            valor_saque = float(input("Digite o valor que deseja sacar: "))

                            if valor_saque > 500:
                                print("Valor máximo de R$500.00 por saque excedido. Favor escolher um novo valor para sacar")
                                continue

                            elif valor_saque > conta["saldo"]:
                                print("Você não possui saldo suficiente para esta operação. Favor escolher um novo valor para sacar")
                                continue

                            else:
                                sacar(saque=valor_saque, conta=conta)
                                saque_check = False

        elif opcao == "e":
            nro_conta = int(input("Digite o número da conta bancária: "))

            if nro_conta > num_conta:
                print("Conta não cadastrada")
                continue

            for conta in contas:
                if conta["numero"] == nro_conta:         
                    extrato(conta)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()