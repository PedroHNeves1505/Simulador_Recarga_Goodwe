from app.functions import inicializar_banco_de_dados, mensagem_entrada, entrar_no_sistema, criar_gerenciador, rodar_sistema
from app.classes import SessaoRecarga

def run():
    inicializar_banco_de_dados()
    mensagem_entrada()
    entrar_no_sistema()
    gerenciador = criar_gerenciador()
    rodar_sistema(gerenciador)

if __name__ == '__main__':
    run()