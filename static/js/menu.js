document.addEventListener('DOMContentLoaded', () => {
    const btnAdicionarCarro = document.getElementById('btn_adicionar_carro');
    const btnMonitoramento = document.getElementById('btn_monitoramento');
    const btnOrdenar = document.getElementById('btn_ordenar');
    const btnBuscar = document.getElementById('btn_buscar');
    const inputVaga = document.getElementById('input_vaga_busca');
    const elementoMensagem = document.getElementById('mensagem');
    const containerResultado = document.getElementById('container_resultado_busca');

    let tempoParaSumirAdd = null;
    let tempoParaSumirOrder = null;

    // Opção 1: Adicionar Carro
    if (btnAdicionarCarro) {
        btnAdicionarCarro.addEventListener('click', async () => {
            try {
                const resposta = await fetch('/api/sessoes/adicionar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    if (elementoMensagem) {
                        elementoMensagem.innerText = `Veículo adicionado ao posto! (${dados.mensagem})`;
                        elementoMensagem.style.color = '#4CAF50';
                    }

                    if (tempoParaSumirAdd) clearTimeout(tempoParaSumirAdd);
                    tempoParaSumirAdd = setTimeout(() => {
                        if (elementoMensagem) elementoMensagem.innerText = '';
                    }, 10000);
                } else {
                    if (elementoMensagem) {
                        elementoMensagem.innerText = 'Erro ao adicionar veículo.';
                        elementoMensagem.style.color = '#FF5252';
                    }
                }
            } catch (erro) {
                console.error('Erro:', erro);
            }
        });
    }

    // Opção 2: Monitoramento
    if (btnMonitoramento) {
        btnMonitoramento.addEventListener('click', () => {
            window.location.href = '/monitoramento';
        });
    }

    // Opção 3: Ordenar
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
                    if (elementoMensagem) {
                        elementoMensagem.innerText = 'Sessão organizada';
                        elementoMensagem.style.color = '#4CAF50';
                    }

                    if (tempoParaSumirOrder) clearTimeout(tempoParaSumirOrder);
                    tempoParaSumirOrder = setTimeout(() => {
                        if (elementoMensagem) elementoMensagem.innerText = '';
                    }, 5000);
                }
            } catch (erro) {
                console.error('Erro:', erro);
            }
        });
    }

    // Opção 4: Buscar Sessão por Vaga
    if (btnBuscar) {
        btnBuscar.addEventListener('click', async () => {
            const idVaga = inputVaga ? inputVaga.value.trim() : '';

            if (!idVaga) {
                if (elementoMensagem) {
                    elementoMensagem.innerText = 'Informe o número da vaga para buscar.';
                    elementoMensagem.style.color = '#FF9800';
                }
                if (containerResultado) containerResultado.innerHTML = '';
                return;
            }

            try {
                const resposta = await fetch(`/api/sessoes/buscar/${idVaga}`);
                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    if (elementoMensagem) elementoMensagem.innerText = '';
                    const s = dados.sessao;

                    if (containerResultado) {
                        containerResultado.innerHTML = `
                            <div class="card-vaga">
                                <div class="card-header">
                                    <span class="vaga-badge">Vaga #${s.id}</span>
                                    <span class="status-badge ${s.status.toLowerCase()}">${s.status}</span>
                                </div>
                                <h3 class="carro-nome">${s.marca} ${s.modelo}</h3>
                                <div class="bateria-info">
                                    <span>Bateria: ${s.bateria_atual}%</span>
                                    <span>Capacidade: ${s.capacidade} kWh</span>
                                </div>
                                <div class="progress-bar-bg">
                                    <div class="progress-bar-fill" style="width: ${s.bateria_atual}%;"></div>
                                </div>
                                <div class="card-detalhes">
                                    <p>⚡ Energia Injetada: <strong>${s.energia_injetada} kWh</strong></p>
                                    <p>⏱️ Tempo Estimado: <strong>${s.tempo_restante_min} min</strong></p>
                                </div>
                            </div>
                        `;
                    }
                } else {
                    if (elementoMensagem) {
                        elementoMensagem.innerText = dados.mensagem || 'Vaga não encontrada.';
                        elementoMensagem.style.color = '#FF5252';
                    }
                    if (containerResultado) containerResultado.innerHTML = '';
                }
            } catch (erro) {
                console.error('Erro na busca:', erro);
            }
        });
    }
});