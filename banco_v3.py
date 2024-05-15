# Modelagem de sistema bancário usando POO
# Adicionar classes para cliente e as operações bancárias depósito e saque
# Dados de clientes e contas bancárias devem ser armazenados em objetos, e não em dicionários
# Após concluir a modelagem das classes e criação dos métodos, atualizar o método menu() e demais métodos para funcionar com as classes modeladas

import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Conta:

    def __init__(self, cliente, numero):
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
        saldo = self._saldo

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

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if numero_saques >= self.limite_saques:
            print("Operação não permitida: Número máximo de saques excedido.")
        elif valor > self.limite:
            print("Operação não permitida: Valor excede o limite por saque.")
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\n
                Agência:\t{self.agencia}
                C/C:\t{self.numero}
                Titular:\t{self.cliente.nome}\n"""


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
            "data": datetime.now().strftime("%D-%m-%Y %H:%M:%S1")
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
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

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf_cliente, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf_cliente
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf


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

def filtro_cliente(cpf, clientes):
    filtrar_cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    cliente = filtrar_cliente[0]

    return cliente

def filtro_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta cadastrada")
        return None
    
    return cliente.contas[0]

def deposito(cpf, clientes):

    cliente = filtro_cliente(cpf, clientes)
    conta = filtro_conta(cliente)
    if cliente is None or conta is None:
        print("Não foi possível completar a operação")
        return

    valor = float(input("Digite o valor do depósito: R$"))
    operacao = Deposito(valor)

    cliente.realizar_transacao(conta, operacao)

def saque(cpf, clientes):

    cliente = filtro_cliente(cpf, clientes)
    conta = filtro_conta(cliente)
    if cliente is None or conta is None:
        print("Não foi possível completar a operação")
        return

    valor = float(input("Digite o valor do saque: R$"))
    operacao = Saque(valor)

    cliente.realizar_transacao(conta, operacao)

def exibir_extrato(cpf, clientes):
    
    conta = filtro_conta(filtro_cliente(cpf, clientes))
    if filtro_conta is None:
        print("Não foi possível completar a operação")
        return

    word = 'EXTRATO'
    print(f"\n{word.center(21, '=')}\n")
    print(conta)
    
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    word = 'FIM DO EXTRATO'
    print(f"\n{word.center(21, '=')}\n")

def main():
    cpf_clientes = []
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

            novo_cliente = PessoaFisica(nome=nome, data_nascimento=dob, cpf_cliente=cpf, endereco=endereco)
            
            cpf_clientes.append(novo_cliente.cpf)
            clientes.append(novo_cliente)

            print(f"Cadastro de {novo_cliente.nome} concluído com sucesso")

        elif opcao == "lc":
            for conta in contas:
                print(textwrap.dedent(str(conta)))

        elif opcao == "cpfs":
            print(cpf_clientes)

        elif opcao == "c":
            cpf = input("Digite o CPF do cliente (apenas números, sem ponto ou traço): ")

            if cpf not in cpf_clientes:
                print("Cliente não cadastrado. Selecione N para cadastrar novo cliente")
                continue

            filtro_cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
            cliente = filtro_cliente[0]

            nova_conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)

            contas.append(nova_conta)
            cliente.adicionar_conta(nova_conta)
            numero_conta += 1
            print(f"Conta cadastrada com sucesso")
     
        elif opcao == "d":
            cpf = input("Digite o CPF do cliente (apenas números, sem ponto ou traço): ")
            
            if cpf not in cpf_clientes:
                print("Cliente não cadastrado. Selecione N para cadastrar novo cliente")
                continue

            deposito(cpf, clientes)

        elif opcao == "s":
            cpf = input("Digite o CPF do cliente (apenas números, sem ponto ou traço): ")
            
            if cpf not in cpf_clientes:
                print("Cliente não cadastrado. Selecione N para cadastrar novo cliente")
                continue

            saque(cpf, clientes)

        elif opcao == "e":
            cpf = input("Digite o CPF do cliente (apenas números, sem ponto ou traço): ")
            
            if cpf not in cpf_clientes:
                print("Cliente não cadastrado. Selecione N para cadastrar novo cliente")
                continue

            exibir_extrato(cpf, clientes)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()