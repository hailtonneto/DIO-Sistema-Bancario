import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizarTransacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionarConta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, dataNascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dataNascimento = dataNascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def novaConta(cls, cliente, numero):
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
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.sacar
        excedeuSaldo = valor > saldo
        
        if excedeuSaldo:
            print('\n@@@ Operação Inválida! Você não tem saldo suficiente. @@@')
            
        elif valor > 0:
            self._saldo -= valor
            print('\n=== SAQUE REALIZADO COM SUCESSO! ===')
            return True
        
        else:
            print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n=== DEPÓSITO REALIZADO COM SUCESSO! ===')
        
        else:
            print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
            
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limiteSaques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limiteSaques = limiteSaques
        
    def sacar(self, valor):
        numeroSaques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        
        excedeuLimite = valor > self.limite
        execedeuSaques = numeroSaques >= self.limiteSaques
        
        if excedeuLimite:
            print('\n@@@ Operação Inválida! O valor do saque excede o limite. @@@')
        
        elif execedeuSaques:
            print('\n@@@ Operação Inválida! Número máximo de saques excedido. @@@')
            
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
        
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionarTransacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%s'),
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucessoTransacao = conta.sacar(self.valor)
        
        if sucessoTransacao:
            conta.historico.adicionarTransacao(self)
            

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        sucessoTransacao = conta.depositar(self.valor)
            
        if sucessoTransacao:
            conta.historico.adicionarTransacao(self)


def menu():
    menu = """\n
    ========== BANCO ===========
    
    [D]\tDEPOSITAR
    [S]\tSACAR
    [E]\tEXTRATO
    [C]\tNOVA CONTA
    [L]\tLISTAR CONTAS
    [U]\tNOVO USUÁRIO
    [F]\tFINALIZAR
    
    ============================

    ==> """
    return input(textwrap.dedent(menu))


def filtrarCliente(cpf, clientes):
    clientesFiltrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientesFiltrados[0] if clientesFiltrados else None


def recuperarContaCliente(cliente):
    if not cliente.contas:
        print('\n@@@ Cliente não possui conta! @@@')
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrarCliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)
    
    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)


def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrarCliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)
    
    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)


def exibirExtrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrarCliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    print('\n========== EXTRATO ===========')
    transacoes = conta.historico.transacoes
    
    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'
            
    print(extrato)
    print(f'\nSaldo:\t\tR$ {conta.saldo:.2f}')
    print('==============================')


def criarCliente(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrarCliente(cpf, clientes)
    
    if cliente:
        print('\n@@@ Já existe cliente com esse CPF! @@@')
        return

    nome = input('Informe o nome completo: ')
    dataNascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereco (logadouro, nro - bairro - cidade/sigla estado): ')
    
    cliente = PessoaFisica(nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    
    print('=== CLIENTE CRIADO COM SUCESSO! ===')


def criarConta(numeroConta, clientes, contas):
    cpf = input('Informe o CPF do usuário: ')
    cliente = filtrarCliente(cpf, clientes)
    
    if not clientes:
        print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@')
        return
    
    conta = ContaCorrente.novaConta(cliente=cliente, numero=numeroConta)
    contas.append(conta)
    clientes.contas.append(conta)
    
    print('\n=== CONTA CRIADA COM SUCESSO! ===')


def listarContas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == 'D':
            depositar(clientes)
            
        elif opcao == 'S':
            sacar(clientes)
        
        elif opcao == 'E':
            exibirExtrato(clientes)
            
        elif opcao == 'U':
            criarCliente(clientes)
        
        elif opcao == 'C':
            numeroConta = len(contas) + 1
            criarConta(numeroConta, clientes, contas)
        
        elif opcao == 'L':
            listarContas(contas)
        
        elif opcao == 'F':
            break
        
        else:
            print('Operação Inválida, por favor selecione novamente a operação desejada.')


main()