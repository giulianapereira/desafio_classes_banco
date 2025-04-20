from abc import ABC, abstractmethod
import textwrap
from datetime import datetime


class Cliente ():
    def __init__(self, endereco, contas):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
       transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Pessoafisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
      super().__init__(endereco)
      self.cpf = cpf
      self.nome = nome
      self.data_nascimento = data_nascimento



class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0 
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() 
    
    @classmethod
    def nova_conta(cls, cliente, numero):  
        return cls(numero, cliente)    

    

    @property
    def saldo (self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    
    @property 
    def cliente (self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print ("\nNão foi possível fazer o Saque! Dinheiro insuficiente!")
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True 
        else:
            print ("Falha no saque! Valor inválido!")
        return False
    
    def depositar(self, valor):
        if valor > 0: 
            self._saldo += valor
            print("Valor depositádo com sucesso!")
            return True
        else: 
            print("O valor informado para depósito é inválido")
        
        return False   

       

class ContaCorrente(Conta):
    def __init__(self, numero,cliente, limite = 500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self, valor):

        numero_saques = len([transacao for transacao in self.historico.
                             transacoes if ['Tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saque

        if excedeu_limite: 
            print("O Valor do Saque exedeu o valor de R$:500 reais!")
        elif excedeu_saque:
            print("Numero maximo de saques diários excedido")

        else:
            return super().sacar(valor)
        return False
        
            
class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass

class Historico ():
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({

            "Tipo": transacao.__class__.__name__,
            "Valor" : transacao.valor,
            "data": datetime.now().strftime ("%d-%m-%Y %H:%M"),
            

        })
    


class Debito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar (self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta,Historico.adicionar_transacao(self)
 

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
        
    def registrar (self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
def menu():
    print("""
    ==================== MENU ====================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair
    ==============================================
    """)
    return int(input("Digite a opção desejada: "))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica (nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1:
            depositar(clientes)

        elif opcao == 2:
            sacar(clientes)

        elif opcao == 3:
            exibir_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 7:
            break

        else:
            print("\n Operação inválida, por favor selecione novamente a operação desejada.")


main()