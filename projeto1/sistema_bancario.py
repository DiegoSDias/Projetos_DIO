from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._historico = Historico()
           
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
            
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        
        else:
            print("\nOperação falhou! Valor informado inválido.")
        
        return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("\nOperação falhou! Valor informado inválido.") 
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
        
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self._historico.
             transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque >= self.limite_saque
 
        if excedeu_limite:
            print("\nOperação falhou! Valor do saque ultrapassou valor limite.")
            
        elif excedeu_saques:
            print("\nOperação falhou! Número de saques ultrapassou o limite.")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self._numero}
            Titular:\t{self.cliente.nome}
        """
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("\nOperação falhou! Valor informado inválido.") 
     
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def historico(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

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
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.transacao.adicionar_transacao(self)

def menu():
    
    menu = f"""\n
    ===============MENU===============
    1 - Depositar
    2 - Sacar
    3 - Extrato
    4 - Novo Usuário
    5 - Nova Conta
    6 - Listar Contas
    0 - Sair
    """
    

    print(menu)
    opcao = (input('Escolha uma opção: '))
    
    return opcao

def filtrar_usuario(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf  = input("Informe o seu CPF: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("informe o valor de depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf  = input("Informe o seu CPF: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("informe o valor de saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def extratos(clientes):
    cpf  = input("Informe o seu CPF: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=========== EXTRATO ===========")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
            
    print(extrato)
    print(f"\nSaldo:\n\t {conta.saldo:.2f}")
    print("===============================")
        
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, clientes)
    
    if usuario:
        print("Já existe um usuário com esse CPF!")
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, num - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print("Cliente criado com sucesso!")
    
def criar_conta(numero_conta, contas, clientes):
    cpf  = input("Informe o seu CPF: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado! Fluxo de criaçao de conta encerrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\nConta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
       print('=' * 100)
       print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == '1':
            depositar(clientes)  
                       
        elif opcao == '2':
            sacar(clientes)
            
        elif opcao == '3':
            extratos(clientes)
            
        elif opcao == '4':
            criar_cliente(clientes)
                     
        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, contas, clientes)
                   
        elif opcao == '6':
            listar_contas(contas)   
                   
        elif opcao == '0':
            print("Saindo do sistema, até logo e volte sempre!")
            break
        else:
            print("Opção invalida, digite outro número")
            
main()