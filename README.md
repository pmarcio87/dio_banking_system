Projeto de sistema bancário em Python como parte da trilha de aprendizado Python Developer na plataforma DIO.

**Versão 1**:
Sistema desenvolvido com base em apenas um cliente, contendo operações de depósito, saque e extrato de acordo com as seguintes premissas:

- Depósito deve ser positivo e inteiro, sistema não deve permitir valores negativos
- Saque deve permitir até 3 saques diários com limite máximo de 500 reais. Caso não tenha saldo, sistema deve informar ao usuário que não há saldo disponível
- Extrato - deve listar todos os depósitos e saques realizados, no fim exibindo o saldo final no formato R$ xxx.xx

**Versão 2**:
Refatoramento do código para incluir funções para cada operação. Além disso, duas novas funções foram criadas para cadastrar clientes e cadastrar conta bancária. Sistema desenvolvido seguindo as especificações abaixo, em adição às da primeira versão:

- Função saque deve receber os argumentos apenas pelo nome
- Função depósito deve receber os argumentos apenas por posição
- Função extrato deve receber os argumentos por posição e nome - argumentos posicionais: saldo / argumentos nomeados: extrato
- Função de criar usuário deve armazenar usuários em uma lista, contendo nome (string), DOB(string), CPF(string - não pode ser repetido) e endereço (string no formato "logradouro - nro - bairro - cidade/sigla estado")
- Função criar conta deve armazenar contas em uma lista. Uma conta é composta por agência (número fixo: "0001"), número da conta (sequencial iniciando em 1) e usuário (pode ter mais de uma conta, porém cada conta pertence a somente 1 usuário).
