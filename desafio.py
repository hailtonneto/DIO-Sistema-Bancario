import textwrap

def menu():
    menu = """\n
    ========== BANCO ===========
    
    [d]\tDEPOSITAR
    [s]\tSACAR
    [e]\tEXTRATO
    [nc]\tNOVA CONTA
    [lc]\tLISTAR CONTAS
    [nu]\tNOVO USUÁRIO
    [q]\tSAIR
    
    ============================

    ==> """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\tR$ {valor:.2f}\n'
        print('\n=== DEPÓSITO REALIZADO COM SUCESSO! ===')
    
    else:
        print('\n@@@ OPERAÇÃO FALHO! O VALOR INFORMADO É INVÁLIDO. @@@')
        
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numeroSaques, limiteSaques):
    excedeuSaldo = valor > saldo
    excedeuLimite = valor > limite
    execedeuSaque = numeroSaques >= limiteSaques
        
    if excedeuSaldo:
        print('\n@@@ Operação Inválida! Você não tem saldo suficiente. @@@')
        
    elif excedeuLimite:
        print('\n@@@ Operação Inválida! O valor do saque excede o limite. @@@')
        
    elif execedeuSaque:
        print('\n@@@ Operação Inválida! Número máximo de saques excedido. @@@')
        
    elif valor > 0:
        saldo -= valor
        extrato = f'Saque: R$ {valor:.2f}'
        numeroSaques += 1
        print('\n=== SAQUE REALIZADO COM SUCESSO! ===')
            
    else:
        print('\n@@@ Operação Inválida! O valor informado é inválido. @@@')
    
    return saldo, extrato


def exibirExtrato(saldo, /, *, extrato):
    print('\n========== EXTRATO ===========')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'\nSaldo:\t\tR$ {saldo:.2f}')
    print('==============================')


def criarUsuario(usuarios):
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrarUsuario(cpf, usuarios)
    
    if usuario:
        print('\n@@@ Já existe usuário com esse CPF! @@@')
        return

    nome = input('Informe o nome completo: ')
    dataNascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereco (logadouro, nro - bairro - cidade/sigla estado): ')
    
    usuarios.append({'nome': nome, 'dataNascimento': dataNascimento, 'cpf': cpf, 'endereco': endereco})
    
    print('=== USUÁRIO CRIADO COM SUCESSO! ===')


def filtrarUsuario(cpf, usuarios):
    usuariosFiltrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuariosFiltrados[0] if usuariosFiltrados else None


def criarConta(agencia, numeroConta, usuario):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrarUsuario(cpf, usuario)
    
    if usuario:
        print('\n=== CONTA CRIADA COM SUCESSO! ===')
        return {'agencia': agencia, 'numeroConta': numeroConta, 'usuario': usuario}
    
    else:
        print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@')


def listarContas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numeroConta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ''
    numeroSaques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == 'd':
            valor = float(input('Informe o valor do depósito: '))
            
            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == 's':
            valor = float(input('Informe o valor do depósito: '))
            
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numeroSaques=numeroSaques,
                limiteSaques=LIMITE_SAQUES,
            )
        
        elif opcao == 'e':
            exibirExtrato(saldo, extrato=extrato)
            
        elif opcao == 'nu':
            criarUsuario(usuarios)
        
        elif opcao == 'nc':
            numeroConta = len(contas) + 1
            conta = criarConta(AGENCIA, numeroConta, usuarios)
            
            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listarContas(contas)
        
        elif opcao == 'q':
            break
        
        else:
            print('Operação Inválida, por favor selecione novamente a operação desejada.')
    
main()