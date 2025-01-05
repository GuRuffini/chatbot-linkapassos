function getCsrfToken() {
    return document.querySelector('meta[name="csrfmiddlewaretoken"]').getAttribute('content');
}


async function enviarMensagem() {
    const input = document.querySelector('#input');
    const chat = document.querySelector('#chat');

    if (!input.value.trim()) return;
    const mensagem = input.value.trim();
    input.value = "";

    const bolhaUsuario = criaBolhaUsuario(mensagem);
    chat.appendChild(bolhaUsuario);

    const bolhaBot = criaBolhaBot('<span class="loading">Pensando...</span>');
    chat.appendChild(bolhaBot);

    chat.scrollTop = chat.scrollHeight;

    const pensandoInterval = startThinkingEffect(bolhaBot.querySelector('.loading'));

    try {
        const resposta = await fetch("/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({
                msg: mensagem,
                communication_id: 1
            }),
        });

        if (!resposta.ok) {
            throw new Error(`Erro: ${resposta.status} ${resposta.statusText}`);
        }

        const dados = await resposta.json();
        clearInterval(pensandoInterval);

        if (dados.resposta) {
            await displayStreamingResponse(bolhaBot, dados.resposta);
        } else {
            bolhaBot.innerHTML = "Nenhuma resposta foi gerada.";
        }
    } catch (erro) {
        console.error("Erro ao enviar mensagem:", erro);
        bolhaBot.innerHTML = "Desculpe, ocorreu um erro. Tente novamente.";
    }

    chat.scrollTop = chat.scrollHeight;
}


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

function startThinkingEffect(loadingElement) {
    let dots = 0;
    return setInterval(() => {
        dots = (dots + 1) % 4;
        loadingElement.innerHTML = "Pensando" + ".".repeat(dots);
    }, 500);
}

async function displayStreamingResponse(bolhaBot, resposta) {
    bolhaBot.innerHTML = "";

    const htmlResposta = marked.parse(resposta);

    const container = document.createElement('div');
    container.innerHTML = htmlResposta;

    const texto = container.textContent || container.innerText || '';

    for (const char of texto) {
        bolhaBot.innerHTML += char;
        await new Promise((resolve) => setTimeout(resolve, 30));

        bolhaBot.scrollIntoView({ behavior: "smooth", block: "end" });
    }
}


document.querySelector('#botao-enviar').addEventListener('click', enviarMensagem);

document.querySelector('#input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        enviarMensagem();
    }
});
