# Modelagem de sistema bancário usando POO
# Adicionar classes para cliente e as operações bancárias depósito e saque
# Dados de clientes e contas bancárias devem ser armazenados em objetos, e não em dicionários
# Após concluir a modelagem das classes e criação dos métodos, atualizar o método menu() para funcionar com as classes modeladas

from abc import ABC, abstractmethod
from datetime import datetime

class Conta:

    def __init__(self, cliente, numero=numero_conta):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Saldo insuficiente para esta operação.")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("O valor informado para saque é inválido. Tente novamente.")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de {valor} realizado com sucesso. Seu saldo atual é de {self.saldo}.")
            return True
        else:
            print("O valor informado para depósito é inválido. Tente novamente.")
        
        return False


class ContaCorrente(Conta):

    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_saques = 3

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if numero_saques > self.limite_saques:
            print("Operação não permitida: Número máximo de saques excedido.")
        elif valor > self.limite:
            print("Operação não permitida: Valor excede o limite por saque.")
        else:
            super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
                Agência:\t{self.agencia}
                C/C:\t{self.numero}
                Titular:\t{self.cliente.nome}"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor":transacao.valor, 
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento


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

def main():
    clientes = []
    contas = []
    numero_conta = 1

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