document.addEventListener('DOMContentLoaded', () => {
    const btnAdicionarCarro = document.getElementById('btn_adicionar_carro');
    const btnMonitoramento = document.getElementById('btn_monitoramento');
    const elementoMensagem = document.getElementById('mensagem');

    // Botão 1: Adicionar carro
    if (btnAdicionarCarro) {
        btnAdicionarCarro.addEventListener('click', async () => {
            try {
                const resposta = await fetch('/api/sessoes/adicionar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    elementoMensagem.innerText = 'Veículo adicionado ao posto!';
                    elementoMensagem.style.color = '#4CAF50';
                } else {
                    elementoMensagem.innerText = 'Erro ao adicionar veículo.';
                    elementoMensagem.style.color = '#FF5252';
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                elementoMensagem.innerText = 'Erro ao conectar com o servidor.';
                elementoMensagem.style.color = '#FF5252';
            }
        });
    }

    // Botão 2: Ver Carregamento em Tempo Real
    if (btnMonitoramento) {
        btnMonitoramento.addEventListener('click', () => {
            window.location.href = '/monitoramento';
        });
    }
});