document.addEventListener('DOMContentLoaded', () => {
    const btnAdicionarCarro = document.getElementById('btn_adicionar_carro');
    const elementoMensagem = document.getElementById('mensagem');

    if (btnAdicionarCarro) {
        btnAdicionarCarro.addEventListener('click', async () => {
            try {
                // Chama a API do Flask que roda gerenciador.adicionar_veiculo()
                const resposta = await fetch('/api/sessoes/adicionar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                const dados = await resposta.json();

                if (resposta.ok && dados.sucesso) {
                    // Exibe a mensagem exigida na tela
                    elementoMensagem.innerText = 'Veículo adicionado ao posto!';
                    elementoMensagem.style.color = '#4CAF50'; // Cor verde de sucesso
                } else {
                    elementoMensagem.innerText = 'Erro ao adicionar veículo.';
                    elementoMensagem.style.color = '#FF5252'; // Cor vermelha de erro
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                elementoMensagem.innerText = 'Erro ao conectar com o servidor.';
                elementoMensagem.style.color = '#FF5252';
            }
        });
    }
});