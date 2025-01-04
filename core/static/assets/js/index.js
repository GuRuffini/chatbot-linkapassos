// Função para obter o CSRF token do meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrfmiddlewaretoken"]').getAttribute('content');
}

// Adiciona o CSRF token em todas as requisições fetch
async function enviarMensagem() {
    const input = document.querySelector('#input');
    const chat = document.querySelector('#chat');

    if (!input.value.trim()) return; // Impede mensagens vazias
    const mensagem = input.value.trim();
    input.value = "";

    // Adiciona a bolha do usuário no chat
    const bolhaUsuario = criaBolhaUsuario(mensagem);
    chat.appendChild(bolhaUsuario);

    // Adiciona uma bolha "pensando" do bot no chat
    const bolhaBot = criaBolhaBot("Analisando...");
    chat.appendChild(bolhaBot);

    // Envia a mensagem para o backend
    try {
        const resposta = await fetch("http://127.0.0.1:8000/chat/", { // Porta correta: 8000
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({ msg: mensagem }),
        });

        if (!resposta.ok) {
            throw new Error(`Erro: ${resposta.status} ${resposta.statusText}`);
        }

        const dados = await resposta.json();
        bolhaBot.innerHTML = dados.resposta.replace(/\n/g, '<br>');
    } catch (erro) {
        console.error("Erro ao enviar mensagem:", erro);
        bolhaBot.innerHTML = "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.";
    }

    // Rola o chat automaticamente para a última mensagem
    chat.scrollTop = chat.scrollHeight;
}

// Funções auxiliares para criar bolhas no chat
function criaBolhaUsuario(conteudo) {
    const bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    bolha.innerHTML = conteudo;
    return bolha;
}

function criaBolhaBot(conteudo = "") {
    const bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    bolha.innerHTML = conteudo;
    return bolha;
}

// Evento para enviar mensagem ao clicar no botão
document.querySelector('#botao-enviar').addEventListener('click', enviarMensagem);

// Permite enviar mensagem ao pressionar Enter
document.querySelector('#input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        enviarMensagem();
    }
});
