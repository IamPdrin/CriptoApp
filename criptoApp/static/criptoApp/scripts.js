function copiarChave() {
    const campo = document.getElementById("campoChave");
    campo.select();
    campo.setSelectionRange(0, 99999);

    try {
        document.execCommand("copy");
        alert("🔑 Chave copiada!");
    } catch (err) {
        alert("Erro ao copiar a chave.");
    }
}

function copiarResultado() {
    const campo = document.getElementById("campoResultado");
    const texto = campo.innerText;

    const tempInput = document.createElement("textarea");
    tempInput.value = texto;
    document.body.appendChild(tempInput);
    tempInput.select();
    tempInput.setSelectionRange(0, 99999);

    try {
        document.execCommand("copy");
        alert("📋 Resultado copiado!");
    } catch (err) {
        alert("Erro ao copiar o resultado.");
    }

    document.body.removeChild(tempInput);
}
