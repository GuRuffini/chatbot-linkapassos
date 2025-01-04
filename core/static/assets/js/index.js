// Função para obter o CSRF token do meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrfmiddlewaretoken"]').getAttribute('content');
}

// Adiciona o CSRF token em todas as requisições fetch
async function enviarMensagem() {
    let input = document.querySelector('#input');
    let chat = document.querySelector('#chat');

    if (!input.value.trim()) return;
    let mensagem = input.value.trim();
    input.value = "";

    // Cria e adiciona a bolha do usuário no chat
    let novaBolhaUsuario = criaBolhaUsuario();
    novaBolhaUsuario.innerHTML = mensagem;
    chat.appendChild(novaBolhaUsuario);

    // Cria e adiciona a bolha do bot no chat
    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    novaBolhaBot.innerHTML = "Analisando...";
    
    try {
        const resposta = await fetch("/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(), // Inclui o token CSRF
            },
            body: JSON.stringify({ msg: mensagem }),
        });

        if (!resposta.ok) {
            throw new Error(`Erro: ${resposta.status} ${resposta.statusText}`);
        }

        const dados = await resposta.json();
        novaBolhaBot.innerHTML = dados.resposta.replace(/\n/g, '<br>');
    } catch (erro) {
        console.error("Erro ao enviar mensagem:", erro);
        novaBolhaBot.innerHTML = "Ocorreu um erro ao processar sua mensagem. Tente novamente.";
    }
}

// Funções auxiliares para criar bolhas no chat
function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

document.querySelector('#botao-enviar').addEventListener('click', enviarMensagem);
