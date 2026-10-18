document.addEventListener('DOMContentLoaded', () => {
    // Botões de alternar abas
    const btnShowSignin = document.getElementById('show_signin');
    const btnShowSignup = document.getElementById('show_signup');
    
    // Caixas de formulário
    const boxSignin = document.getElementById('box_signin');
    const boxSignup = document.getElementById('box_signup');

    // Botões de envio
    const btnSignin = document.getElementById('btn_signin');
    const btnSignup = document.getElementById('btn_signup');

    // Alternar para a aba de Sign In
    if (btnShowSignin && boxSignin && boxSignup) {
        btnShowSignin.addEventListener('click', () => {
            boxSignin.classList.remove('hidden');
            boxSignup.classList.add('hidden');
        });
    }

    // Alternar para a aba de Sign Up
    if (btnShowSignup && boxSignin && boxSignup) {
        btnShowSignup.addEventListener('click', () => {
            boxSignup.classList.remove('hidden');
            boxSignin.classList.add('hidden');
        });
    }

    // Ação do botão ENVIAR do SIGN IN (Login)
    if (btnSignin) {
        btnSignin.addEventListener('click', async () => {
            const email = document.getElementById('signin_email').value.trim();
            const senha = document.getElementById('signin_senha').value.trim();

            if (!email || !senha) {
                alert('Preencha o e-mail e a senha para entrar!');
                return;
            }

            try {
                const resposta = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, senha })
                });

                const dados = await resposta.json();
                if (resposta.ok && dados.sucesso) {
                    alert(dados.mensagem);
                    window.location.href = '/menu'; // Redireciona para o menu
                } else {
                    alert(dados.mensagem || 'E-mail ou senha incorretos.');
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                alert('Erro ao conectar com o servidor.');
            }
        });
    }

    // Ação do botão ENVIAR do SIGN UP (Cadastro)
    if (btnSignup) {
        btnSignup.addEventListener('click', async () => {
            const email = document.getElementById('signup_email').value.trim();
            const senha = document.getElementById('signup_senha').value.trim();
            const confirmSenha = document.getElementById('signup_confirm_senha').value.trim();

            if (!email || !senha || !confirmSenha) {
                alert('Preencha todos os campos do cadastro!');
                return;
            }

            if (senha !== confirmSenha) {
                alert('As senhas não coincidem!');
                return;
            }

            try {
                const resposta = await fetch('/api/cadastro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, senha })
                });

                const dados = await resposta.json();
                if (resposta.ok && dados.sucesso) {
                    alert(dados.mensagem);
                    // Limpa os campos e muda para a aba de login
                    document.getElementById('signup_email').value = '';
                    document.getElementById('signup_senha').value = '';
                    document.getElementById('signup_confirm_senha').value = '';
                    boxSignin.classList.remove('hidden');
                    boxSignup.classList.add('hidden');
                } else {
                    alert(dados.mensagem || 'Erro ao realizar o cadastro.');
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                alert('Erro ao conectar com o servidor.');
            }
        });
    }
});