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

def depositar(saldo_total, valor_depositado, extrato, /):
    saldo_total += valor_depositado
    print(f'Você depositou R${valor_depositado:.2f} com sucesso!')
    extrato += f'Depósito: R${valor_depositado:.2f}\n'
    
    return saldo_total, extrato
    
def sacar(*, saldo_total, valor_sacado, extrato, limite, num_saques, limite_saques):
    if num_saques < limite_saques:
        if valor_sacado > saldo_total:
            print("Você não tem saldo suficiente para realizar este saque.")
        elif valor_sacado > limite:
            print(f"Você não pode sacar mais que R${limite:.2f} por transação.")
        else:
            saldo_total -= valor_sacado
            num_saques += 1
            print(f'Você sacou R${valor_sacado:.2f} com sucesso! Seu saldo atual é de R${saldo_total:.2f}')
            extrato += f'Saque: R${valor_sacado:.2f}\n'
    else:
        print("Número máximo de saques excedidos.")
            
    return (saldo_total, num_saques, extrato)

def extratos(saldo_total, num_saques, /, *, extrato):
    print("===============EXTRATO===============")
    print("\nNão foram realizadas movimentações." if not extrato else extrato)
    print(f'Seu saldo atual é de R${saldo_total:.2f}')
    print(f'Você já realizou {num_saques} saques hoje.\n')

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("Já existe um usuário com esse CPF!")
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, num - bairro - cidade/sigla estado): ")
    
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    
    print("Usuário criado com sucesso!")
    
def filtrar_usuario(cpf, usuarios):
    usuario_existe = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_existe[0] if usuario_existe else None

def criar_conta(agencia, num_contas, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso")
        return ({'agencia': agencia, 'num_contas': num_contas, 'usuario': usuario})
    print('Usuário não encontrado, criação de conta encerrada')

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência: {conta['agencia']}
        C/C: {conta['num_contas']}
        Titular: {conta['usuario']['nome']}
        """
        print("==========================================")
        print(linha)

def main():
    saldo_total = 0
    limite = 500
    num_saques = 0
    LIMITE_SAQUES = 3
    extrato = ''
    AGENCIA = '0001'
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == '1':
            valor_depositado = -1
            while valor_depositado < 0:
                valor_depositado = float(input('Digite o valor que deseja depositar em sua conta: '))
                if valor_depositado < 0:
                    print("Você não pode depositar um valor negativo.")
                else:
                    saldo_total, extrato = depositar(saldo_total, valor_depositado, extrato)             
        elif opcao == '2':
            
            valor_sacado = float(input("Digite o valor para sacar: "))
            
            saldo_total, num_saques, extrato = sacar(
                saldo_total = saldo_total,
                valor_sacado = valor_sacado,
                extrato = extrato,
                limite = limite,
                num_saques = num_saques,
                limite_saques = LIMITE_SAQUES
            )          
        elif opcao == '3':
            extratos(saldo_total, num_saques, extrato = extrato)
        elif opcao == '4':
            criar_usuario(usuarios)         
        elif opcao == '5':
            num_contas = len(contas) + 1
            conta = criar_conta(AGENCIA, num_contas, usuarios)
            
            if conta:
                contas.append(conta)         
        elif opcao == '6':
            listar_contas(contas)          
        elif opcao == '0':
            print("Saindo do sistema, até logo e volte sempre!")
            break
        else:
            print("Opção invalida, digite outro número")
            
main()