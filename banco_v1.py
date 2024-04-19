# Operações

# depósito = deve ser positivo e inteiro, sistema não deve permitir valores negativos
# saque - permitir até 3 saques diários com limite máximo de 500 reais. Caso não tenha saldo, sistema deve informar ao usuário que não há saldo disponível
# extrato - deve listar todos os depósitos e saques realizados, no fim exibindo o saldo final no formato R$ xxx.xx

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
num_oper = 0
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        num_oper += 1
        deposito_void = True
        while deposito_void:
            deposito = int(input("Digite o valor que deseja depositar: "))
            if deposito <= 0:
                print("Digite um valor inteiro maior que zero")
                continue
            else:
                deposito_void = False
        
        saldo += deposito
        print(f"Depósito realizado. Seu saldo atual é de R${saldo:.2f}")
        extrato.append(f'Operação {num_oper}: Depósito de R${deposito:.2f}')


    elif opcao == "s":
        num_oper += 1
        numero_saques += 1

        if numero_saques > LIMITE_SAQUES:
            print("Número máximo de saques diários atingido. Volte amanhã!")
            continue

        saque_void = True

        while saque_void:
            saque = float(input("Digite o valor que deseja sacar: "))

            if saque > 500:
                print("Valor máximo de R$500.00 por saque excedido. Favor escolher um novo valor para sacar")
                continue
            elif saque > saldo:
                print("Você não possui saldo suficiente para esta operação. Favor escolher um novo valor para sacar")
                continue
            else:
                saque_void = False

        saldo -= saque
        print(f"Saque de R${saque:.2f} realizado. Seu saldo atual é de R${saldo:.2f}.")
        extrato.append(f"Operação {num_oper}: Saque de R${saque:.2f}")

    elif opcao == "e":
        word = 'EXTRATO'
        print(f"\n{word.center(21, '=')}")
        if len(extrato) == 0:
            print("Não foram realizadas operações")
        else:
            for operacao in extrato:
                print(operacao)
        print(f"\n\nSeu saldo é de R${saldo:.2f}")
        print("="*21)

    elif opcao == "q":
        print("Obrigado por usar nosso sistema")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")