from abc import ABC, abstractmethod
import datetime


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
        self._agencia = 0001
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
        




