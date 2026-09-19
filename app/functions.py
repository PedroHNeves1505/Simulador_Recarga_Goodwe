import os
import subprocess
import sys
import time as tm
from datetime import time
import sqlite3

def inicializar_banco_de_dados():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()


def apagar_terminal():
	subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def mensagem_entrada():
	apagar_terminal()
	print('Iniciando Sistema HCA G2...')


def entrar_no_sistema():
    print('\n' + ('=~' * 20))
    print('1 - Já possuo uma conta.')
    print('2 - Criar conta.')
    try:
        escolha_usuario = int(input('Escolha a opção: '))
    except ValueError:
        print('Entrada inválida! Digite 1 ou 2.')
        sys.exit()

    while escolha_usuario not in [1, 2]:
        print('Opção inválida!')
        input('Digite qualquer tecla para continuar: ')
        apagar_terminal()
        print('=~' * 20)
        print('1 - Já possuo uma conta.')
        print('2 - Criar conta')
        try:
            escolha_usuario = int(input('Escolha a opção: '))
        except ValueError:
            print('Entrada inválida! Digite 1 ou 2.')
            sys.exit()

    if escolha_usuario == 2:
        print('Antes de iniciar a criação da conta, certifique-se que o PowerGrid esteja conectado a uma rede Wi-Fi!\n')

        apagar_terminal()
        print('PERFIL DO USUÁRIO')
        print('=~' * 20)
        criar_email = input('Digite seu e-mail: ')
        criar_senha = input('Digite a senha: ')
        conf_senha = input('Digite novamente a senha: ')

        if criar_senha != conf_senha:
            while criar_senha != conf_senha:
                print('Senhas diferentes! Corrija.')
                criar_senha = input('Digite a senha: ')
                conf_senha = input('Digite novamente a senha: ')

        try:
            conexao = sqlite3.connect('usuarios.db')
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, senha, endereco, num_serie, cod_verificacao, tipo_estacao)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (criar_email, criar_senha))
            conexao.commit()
            conexao.close()
            print('Conta criada com sucesso!')
            tm.sleep(5)
        except sqlite3.IntegrityError:
            print('Erro: Este e-mail já está cadastrado!')
            tm.sleep(3)
            sys.exit()
    else:
        pass

    entrar = False

    while not entrar:
        apagar_terminal()
        print('Entrar na conta.')
        entrar_email = input('Digite seu e-mail: ')
        entrar_senha = input('Digite a senha: ')

        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT senha FROM usuarios WHERE email = ?', (entrar_email,))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado and resultado[0] == entrar_senha:
            entrar = True
        else:        
            encerrar = False    
            while not encerrar:
                novamente = input('E-mail ou senha incorretas! Deseja tentar novamente (sim, não): ')
                if novamente.lower() == 'sim':
                    break
                elif novamente.lower() == 'não':
                    print('Saindo do sistema.')
                    tm.sleep(5)
                    sys.exit()
                else:
                    print('Resposta não válida, tente novamente.')
                    tm.sleep(1)

    apagar_terminal()
    print('Entrada bem sucedida!')
    tm.sleep(5)


def obter_tipo_fluxo(dia_semana, hora_atual):
	if dia_semana < 5:
		if (hora_atual >= time(22, 0) or hora_atual < time(7, 0)) or (time(9, 0) <= hora_atual < time(11, 0)): return "BAIXA"
		elif (time(7, 0) <= hora_atual < time(9, 0)) or (time(14, 0) <= hora_atual < time(17, 0)): return "MEDIANO"
		elif (time(12, 0) <= hora_atual < time(14, 0)) or (time(17, 0) <= hora_atual < time(21, 0)): return "PICO"
		else: return "REGULAR"
	else:
		if (hora_atual >= time(22, 0) or hora_atual < time(9, 0)): return "BAIXA"
		elif (time(9, 0) <= hora_atual < time(13, 0)) or (time(20, 0) <= hora_atual < time(22, 0)): return "MEDIANO"
		elif (time(14, 0) <= hora_atual < time(20, 0)): return "PICO"
		else: return "REGULAR"


def calcular_tarifa_inteligente(data_hora, preco_base_kwh=1.50):
	dia_semana = data_hora.weekday()
	hora_atual = data_hora.time()
	fluxo = obter_tipo_fluxo(dia_semana, hora_atual)
	is_janela_goodwe = time(10, 0) <= hora_atual <= time(14, 0)
	if fluxo == "PICO": fator = 1.25 if is_janela_goodwe else 1.40
	elif fluxo == "MEDIANO": fator = 0.85 if is_janela_goodwe else 1.00
	elif fluxo == "BAIXA": fator = 0.70 if is_janela_goodwe else 0.90
	else: fator = 0.85 if is_janela_goodwe else 1.00
	return {"fluxo": fluxo, "geracao_solar": is_janela_goodwe, "preco_final_kwh": round(preco_base_kwh * fator, 2)}


def criar_gerenciador():
	from app.classes import GerenciadorEstacoes
	gerenciador = GerenciadorEstacoes(potencia_maxima_rede=40.0)
	return gerenciador

def rodar_sistema(gerenciador):
    while True:
        apagar_terminal()
        print("="*15 + " PANEL CONTROL HCA G2 " + "="*15)
        print("1. Conectar/Simular Entrada de Carro")
        print("2. Ver Carregamento em Tempo Real (Monitoramento)")
        print("3. Ordenar Sessão")
        print("4. Buscar Sessão")
        print("5. Exibir o Relatório e Sair do Sistema")
        print("="*52)
        
        opcao = input("Escolha a opção: ")
        if opcao == "1":
            gerenciador.adicionar_veiculo()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "2":
            gerenciador.monitorar_tempo_real()
        elif opcao == "3":
            gerenciador.ordenar_sessao()
        elif opcao == '4':
            gerenciador.buscar_sessao()
        elif opcao == "5":
            gerar_relatorio(gerenciador)
            print("Encerrando aplicação...")
            tm.sleep(5)
            apagar_terminal()
            break
        else:
            print("Opção inválida! Escolha de 1 a 5.")
            tm.sleep(1)

def bubble_sort(lista_sessoes, chave):
    n = len(lista_sessoes)
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            val1 = getattr(lista_sessoes[j], chave, 0)
            val2 = getattr(lista_sessoes[j + 1], chave, 0)

            val1 = 0 if val1 is None else val1
            val2 = 0 if val2 is None else val2

            if val1 > val2:
                lista_sessoes[j], lista_sessoes[j + 1] = lista_sessoes[j + 1], lista_sessoes[j]
                trocou = True
        if not trocou:
            break

def busca_sequencial(vagas, vaga_procurada):
    for i in range(len(vagas)):
        if vagas[i].id_sessao == vaga_procurada:
            return i

    return -1

def gerar_relatorio(gerenciador):
    apagar_terminal()

    sessoes = list(gerenciador.sessoes.values())
    
    total_sessoes = len(sessoes)
    
    if total_sessoes == 0:
        print('========= ESTATÍSTICAS =========\n')
        print('Nenhuma sessão registrada para gerar estatísticas.')
        input('\nPressione Enter para voltar ao menu...')
        return

    energia_total = 0.0
    faturamento_total = 0.0
    maior_consumo = float('-inf')
    menor_consumo = float('inf')

    for sessao in sessoes:
        energia = getattr(sessao, 'energia_injetada', 0.0)
        energia_total += energia

        try:
            dados_tarifa = calcular_tarifa_inteligente(time.now())
            preco_kwh = dados_tarifa['preco_final_kwh']
        except:
            preco_kwh = 1.0  

        custo_sessao = energia * preco_kwh
        faturamento_total += custo_sessao

        if energia > maior_consumo:
            maior_consumo = energia
        if energia < menor_consumo:
            menor_consumo = energia

    ticket_medio = faturamento_total / total_sessoes if total_sessoes > 0 else 0.0

    if maior_consumo == float('-inf'):
        maior_consumo = 0.0
    if menor_consumo == float('inf'):
        menor_consumo = 0.0

    print('========= ESTATÍSTICAS =========')
    print(f'Sessões realizadas: {total_sessoes}')
    print(f'Energia Fornecida:  {energia_total:.2f} kWh')
    print(f'Faturamento:        R$ {faturamento_total:.2f}')
    print(f'Ticket médio:       R$ {ticket_medio:.2f}')
    print(f'Maior consumo:      {maior_consumo:.2f} kWh')
    print(f'Menor consumo:      {menor_consumo:.2f} kWh')
    print('================================')
    
    input('\nPressione Enter para encerrar o programa...')