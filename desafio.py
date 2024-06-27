menu = """
    ========== BANCO ===========
    
    [d] DEPOSITAR
    [s] SACAR
    [e] EXTRATO
    [q] SAIR
    
    ============================

    ==> """

saldo = 0
limite = 500
extrato = ''
numeroSaques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    print()
    
    if opcao == 'd':
        valor = float(input('Informe o valor do depósito: '))
        
        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f}\n'
            
        else:
            print('Operação Inválida! O valor informado é inválido.')
    
    elif opcao == 's':
        valor = float(input('Informe o valor do depósito: '))
        
        excedeuSaldo = valor > saldo
        excedeuLimite = valor > limite
        execedeuSaque = numeroSaques >= LIMITE_SAQUES
        
        if excedeuSaldo:
            print('Operação Inválida! Você não tem saldo suficiente.')
        
        elif excedeuLimite:
            print('Operação Inválida! O valor do saque excede o limite.')
        
        elif execedeuSaque:
            print('Operação Inválida! Número máximo de saques excedido.')
        
        elif valor > 0:
            saldo -= valor
            extrato = f'Saque: R$ {valor:.2f}'
            numeroSaques += 1
            
        else:
            print('Operação Inválida! O valor informado é inválido.')
        
    elif opcao == 'e':
        print('========== EXTRATO ===========')
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'Saldo: R$ {saldo:.2f}')
        print('==============================')
        
    elif opcao == 'q':
        break
    
    else:
        print('Operação Inválida, por favor selecione novamente a operação desejada.')