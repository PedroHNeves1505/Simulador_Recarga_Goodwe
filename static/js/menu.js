document.addEventListener('DOMContentLoaded', () => {
    const btnAdicionarCarro = document.getElementById('btn_adicionar_carro');
    const btnMonitoramento = document.getElementById('btn_monitoramento');
    const btnOrdenar = document.getElementById('btn_ordenar');
    const elementoMensagem = document.getElementById('mensagem');
    
    let tempoParaSumirAdd = null;
    let tempoParaSumirOrder = null;

    // Opção 1: Adicionar Carro (Exibe por 10 segundos)
    if (btnAdicionarCarro) {
        btnAdicionarCarro.addEventListener('click', async () => {
            try {
                const resposta = await fetch('/api/sessoes/adicionar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    elementoMensagem.innerText = `Veículo adicionado ao posto! (${dados.mensagem})`;
                    elementoMensagem.style.color = '#4CAF50';

                    if (tempoParaSumirAdd) clearTimeout(tempoParaSumirAdd);
                    tempoParaSumirAdd = setTimeout(() => {
                        elementoMensagem.innerText = '';
                    }, 10000); // 10 segundos
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

    // Opção 2: Direcionar para Monitoramento
    if (btnMonitoramento) {
        btnMonitoramento.addEventListener('click', () => {
            window.location.href = '/monitoramento';
        });
    }

    // Opção 3: Ordenar Sessão (Exibe "Sessão organizada" por 5 segundos)
    if (btnOrdenar) {
        btnOrdenar.addEventListener('click', async () => {
            const selectCriterio = document.getElementById('criterio_ordenacao');
            const criterio = selectCriterio ? selectCriterio.value : 'id';

            try {
                const resposta = await fetch('/api/sessoes/ordenar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ criterio: criterio })
                });
                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    elementoMensagem.innerText = 'Sessão organizada';
                    elementoMensagem.style.color = '#4CAF50';

                    if (tempoParaSumirOrder) clearTimeout(tempoParaSumirOrder);
                    tempoParaSumirOrder = setTimeout(() => {
                        elementoMensagem.innerText = '';
                    }, 5000); // 5 segundos
                } else {
                    elementoMensagem.innerText = 'Erro ao ordenar sessões.';
                    elementoMensagem.style.color = '#FF5252';
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                elementoMensagem.innerText = 'Erro ao conectar com o servidor.';
                elementoMensagem.style.color = '#FF5252';
            }
        });
    }
});