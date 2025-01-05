document.getElementById("loginForm").addEventListener("submit", function (e) {
    const username = document.getElementById("id_username").value.trim();
    const password = document.getElementById("id_password").value.trim();
    const usernamePattern = /^[a-zA-Z0-9_.@-]{3,50}$/;
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/;

    if (!username || !usernamePattern.test(username)) {
        e.preventDefault();
        alert("Usuário inválido. Somente caracteres válidos são permitidos.");
        return;
    }

    if (!password || !passwordPattern.test(password)) {
        e.preventDefault();
        alert("Senha inválida. Ela deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial.");
        return;
    }
});
