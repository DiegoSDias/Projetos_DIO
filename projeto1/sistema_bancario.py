cabecalho = 'MENU'
menu = f"""
{cabecalho.center(20, "=")}

1 - Depositar
2 - Sacar
3 - Extrato
0 - Sair
"""

saldo_total = 0
limite = 500
num_saques = 0
LIMITE_SAQUES = 3
extrato = ''

while True:
    
    print(menu)
    opcao = (input('Escolha uma opção: '))
    
    if opcao == '1':
        valor_depositado = -1
        while valor_depositado < 0:
            valor_depositado = float(input('Digite o valor que deseja depositar em sua conta: '))
            if valor_depositado < 0:
                print("Você não pode depositar um valor negativo.")
            else:
                saldo_total += valor_depositado
                print(f'Você depositou R${valor_depositado:.2f} com sucesso!')
                extrato += f'Depósito: R${valor_depositado:.2f}\n'
            
    elif opcao == '2':
        
        if num_saques >= LIMITE_SAQUES:
            print(f"Você já realizou os {LIMITE_SAQUES} saques por diários.")
            continue
        
        valor_sacado = float(input("Digite o valor para sacar: "))
        
        if valor_sacado > saldo_total:
            print("Você não tem saldo suficiente para realizar este saque.")
        elif valor_sacado > limite:
            print(f"Você não pode sacar mais que R${limite:.2f} por transação.")
        else:
            saldo_total -= valor_sacado
            num_saques += 1
            print(f'Você sacou R${valor_sacado:.2f} com sucesso! Seu saldo atual é de R${saldo_total:.2f}')
            extrato += f'Saque: R${valor_sacado:.2f}\n'
        
    elif opcao == '3':
        EXTRATO = 'EXTRATO'
        print(f'\n{EXTRATO.center(20, "=")}')
        print("\nNão foram realizadas movimentações." if not extrato else extrato)
        print(f'Seu saldo atual é de R${saldo_total:.2f}')
        print(f'Você já realizou {num_saques} saques hoje.\n')
        
    elif opcao == '0':
        print("Saindo do sistema, até logo e volte sempre!")
        break
    
    else:
        print("Opção invalida, digite outro número")