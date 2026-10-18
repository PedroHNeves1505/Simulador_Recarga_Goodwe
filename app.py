from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from app.functions import inicializar_banco_de_dados, criar_gerenciador, calcular_tarifa_inteligente
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados e o gerenciador de estações
inicializar_banco_de_dados()
gerenciador = criar_gerenciador()

# Rota para carregar o HTML de login
@app.route('/')
def home():
    return render_template('login.html')

# Rota para carregar o menu principal
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    dados = request.get_json()
    print("DADOS RECEBIDOS NO CADASTRO:", dados)  # <-- Adicione esta linha
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"sucesso": False, "mensagem": "E-mail e senha são obrigatórios!"}), 400

    try:
        # Adicionado timeout=10 para esperar o banco destravar caso haja concorrência
        with sqlite3.connect('usuarios.db', timeout=10) as conexao:
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO usuarios (email, senha) VALUES (?, ?)', (email, senha))
            conexao.commit()
        return jsonify({"sucesso": True, "mensagem": "Conta criada com sucesso!"})
    except sqlite3.IntegrityError:
        return jsonify({"sucesso": False, "mensagem": "Este e-mail já está cadastrado!"}), 400
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro no servidor: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    dados = request.get_json()
    print("DADOS RECEBIDOS NO LOGIN:", dados)
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha e-mail e senha!"}), 400

    try:
        with sqlite3.connect('usuarios.db', timeout=10) as conexao:
            cursor = conexao.cursor()
            cursor.execute('SELECT senha FROM usuarios WHERE email = ?', (email,))
            resultado = cursor.fetchone()

        if resultado and resultado[0] == senha:
            return jsonify({"sucesso": True, "mensagem": "Login bem-sucedido!"})
        return jsonify({"sucesso": False, "mensagem": "E-mail ou senha incorretos."}), 401
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro no servidor: {str(e)}"}), 500

@app.route('/api/sessoes/adicionar', methods=['POST'])
def api_adicionar_veiculo():
    gerenciador.adicionar_veiculo()
    ultimo_id = gerenciador.contador_ids - 1
    carro = gerenciador.sessoes[ultimo_id]
    return jsonify({
        "sucesso": True, 
        "mensagem": f"Veículo {carro.marca} {carro.modelo} conectado na Vaga #{ultimo_id}!"
    })

@app.route('/api/sessoes', methods=['GET'])
def api_listar_sessoes():
    gerenciador.atualizar_todas_as_sessoes()
    sessoes_data = []
    sessoes_ativas = [s for s in gerenciador.sessoes.values() if s.status == "Carregando"]
    potencia_vaga = gerenciador.potencia_maxima_rede / max(len(sessoes_ativas), 1)

    # CORRIGIDO: mudado de .values() para .items() para desemacotar corretamente (id_s, s)
    for id_s, s in gerenciador.sessoes.items():
        if s.status == "Carregando":
            energia_restante = ((100 - s.bateria_atual) / 100) * s.capacidade
            tempo_restante_min = int((energia_restante / potencia_vaga) * 60)
        else:
            tempo_restante_min = 0

        sessoes_data.append({
            "id": s.id_sessao,
            "marca": s.marca,
            "modelo": s.modelo,
            "capacidade": s.capacidade,
            "bateria_atual": round(s.bateria_atual, 1),
            "energia_injetada": round(s.energia_injetada, 2),
            "status": s.status,
            "tempo_restante_min": tempo_restante_min
        })

    return jsonify({"potencia_maxima_rede": gerenciador.potencia_maxima_rede, "sessoes": sessoes_data})
    
@app.route('/monitoramento')
def monitoramento():
    return render_template('monitoramento.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)