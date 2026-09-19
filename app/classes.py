from datetime import datetime
import random
import json
import time as tm
from app.functions import calcular_tarifa_inteligente, apagar_terminal, bubble_sort, busca_sequencial

class SessaoRecarga:
	def __init__(self, id_sessao, veiculo, bateria_inicial):
		self.id_sessao = id_sessao
		self.marca = veiculo['marca']
		self.modelo = veiculo['modelo']
		self.capacidade = veiculo['capacidade_bateria_kwh']
		self.bateria_atual = float(bateria_inicial)
		self.energia_injetada = 0.0
		self.status = "Carregando"
		self.energia_restante = ((100 - self.bateria_atual) / 100) * self.capacidade
		self.ultima_atualizacao = datetime.now() 

	def atualizar_acumulado(self, potencia_limite):
		if self.status != "Carregando":
			return

		agora = datetime.now()
		segundos_passados = (agora - self.ultima_atualizacao).total_seconds()
		self.ultima_atualizacao = agora

		if segundos_passados <= 0:
			return

		for _ in range(int(segundos_passados)):
			if self.bateria_atual >= 100.0:
				self.status = "Concluído"
				break

			tensao = random.uniform(212, 220) if random.random() < 0.95 else random.uniform(200, 211)
			corrente = random.uniform(31.5, 32.5) if tensao >= 212 else random.uniform(32.6, 40.0)
			potencia_kw = min((tensao * corrente) / 1000, potencia_limite)

			energia_ganha = potencia_kw / 3600
			self.energia_injetada += energia_ganha
			self.bateria_atual = min(100.0, self.bateria_atual + ((energia_ganha / self.capacidade) * 100))

class GerenciadorEstacoes:
	def __init__(self, potencia_maxima_rede=40.0):
		self.sessoes = {}
		self.potencia_maxima_rede = potencia_maxima_rede
		self.contador_ids = 1
		with open('app/veiculos.json', 'r', encoding='utf-8') as arquivo:
			self.lista_veiculos = json.load(arquivo)

	def adicionar_veiculo(self):
		veiculo = random.choice(self.lista_veiculos)
		bateria_init = random.randint(15, 70)
		nova_sessao = SessaoRecarga(self.contador_ids, veiculo, bateria_init)
		self.sessoes[self.contador_ids] = nova_sessao
		print(f"\n🚗 {nova_sessao.marca} {nova_sessao.modelo} conectado na Vaga #{self.contador_ids}!")
		self.contador_ids += 1

	def atualizar_todas_as_sessoes(self):
		sessoes_ativas = [s for s in self.sessoes.values() if s.status == "Carregando"]
		if not sessoes_ativas: return
		potencia_por_carro = self.potencia_maxima_rede / len(sessoes_ativas)
		for sessao in self.sessoes.values():
			sessao.atualizar_acumulado(potencia_por_carro)

	def monitorar_tempo_real(self):
		"""CRITÉRIO 6: Visualização dinâmica em tempo real com opção de voltar"""
		try:
			while True:
				apagar_terminal()
				self.atualizar_todas_as_sessoes() 
				
				sessoes_ativas = [s for s in self.sessoes.values() if s.status == "Carregando"]
				potencia_vaga = self.potencia_maxima_rede / max(len(sessoes_ativas), 1)

				print("=== 🔋 MONITORAMENTO EM TEMPO REAL (Pressione Ctrl+C para Voltar) ===")
				if not self.sessoes:
					print("\nNenhum veículo carregando no momento.")
				
				for id_s, s in self.sessoes.items():
					if s.status == "Carregando":
						energia_restante = ((100 - s.bateria_atual) / 100) * s.capacidade
						tempo_restante_horas = energia_restante / potencia_vaga
						tempo_str = f"{int(tempo_restante_horas * 60)} min restantes"
					else:
						tempo_str = "Pronto!"

					barra = "█" * int(s.bateria_atual / 10) + "-" * (10 - int(s.bateria_atual / 10))
					print(f"\nVaga #{id_s}: {s.marca} {s.modelo}")
					print(f"  [{barra}] {s.bateria_atual:.1f}% | Status: {s.status} | Est: {tempo_str}")
				
				tm.sleep(1) 
		except KeyboardInterrupt:
			print("\nRetornando ao menu principal...")
			tm.sleep(1)

	def enviar_log_ocpp(self, tipo_mensagem, payload):
		mensagem = {
				"Protocol": "OCPP-J 1.6",
				"MessageType": "CALL",
				"Action": tipo_mensagem,
				"Timestamp": datetime.now().isoformat(),
				"Payload": payload
		}
		print(f"\n⚡ [OCPP OUT] {json.dumps(mensagem, ensure_ascii=False, indent=2)}")
		print("🔌 [OCPP IN] Confirmação recebida: [3, \"SUCCESS\"]")

	def ordenar_sessao(self):
		apagar_terminal()
		print('Qual críterio você deseja usar para ordenar a sessão?')
		print('1. Vaga')
		print('2. Bateria atual')
		print('3. Status')
		print('4. Tempo restante de carregamento')
		fator_ordenar = input('==> ').lower()
		lista = list(self.sessoes.values())

		chave_ordenacao = None

		match fator_ordenar:
			case '1' | 'vaga':
				chave_ordenacao = 'id_sessao' 
			case '2' | 'bateria atual' | 'bateria':
				chave_ordenacao = 'bateria_atual'
			case '3' | 'status':
				chave_ordenacao = 'status'
			case '4' | 'tempo restante de carregamento' | 'tempo' | 'energia restante':
				chave_ordenacao = 'energia_restante'
			case _:
				print('Opção inválida!')
				return

		bubble_sort(lista, chave_ordenacao)
		self.sessoes = {s.id_sessao: s for s in lista}
		print('\nSessões ordenadas com sucesso!')

	def buscar_sessao(self):
			apagar_terminal()
			lista = list(self.sessoes.values())
			
			if not lista:
				print("\n❌ Não há sessões ativas no momento.")
				input("\nPressione Enter para voltar...")
				return

			print('Qual vaga você deseja procurar?')
			vaga_procurada = int(input('==> '))

			posicao = busca_sequencial(lista, vaga_procurada)

			if posicao == -1 or posicao is None:
				print("\n❌ Vaga não encontrada!")
				input("\nPressione Enter para voltar...")
				return

			vaga = lista[posicao]

			potencia_vaga = self.potencia_maxima_rede / max(len(lista), 1)
		
			if vaga.status == "Carregando":
				energia_restante = ((100 - vaga.bateria_atual) / 100) * vaga.capacidade
				tempo_restante_horas = energia_restante / potencia_vaga
				tempo_str = f"{int(tempo_restante_horas * 60)} min restantes"
			else:
				tempo_str = "Pronto!"
			
			barra = "█" * int(vaga.bateria_atual / 10) + "-" * (10 - int(vaga.bateria_atual / 10))
			
			print(f"\nVaga #{vaga.id_sessao}: {vaga.marca} {vaga.modelo}")
			print(f"  [{barra}] {vaga.bateria_atual:.1f}% | Status: {vaga.status} | Est: {tempo_str}")
			
			input("\nPressione Enter para voltar ao menu...")