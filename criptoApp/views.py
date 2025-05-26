# Importa a função render para retornar uma resposta com template HTML
from django.shortcuts import render

# Importa as funções utilitárias de criptografia
from .utils import gerar_chave, criptografar, descriptografar

# Importa o erro específico de base64 malformado
from binascii import Error

# Importa módulo base64 para decodificar a chave fornecida pelo usuário
import base64

# Função auxiliar para corrigir o padding da string base64, se necessário
def pad_base64(data):
    # Se o comprimento não for múltiplo de 4, adiciona '=' até completar
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

# View principal da aplicação, que lida com criptografia e descriptografia
def index(request):
    resultado = None            # Armazena o resultado da operação (criptografado/descriptografado)
    mensagem_original = ''      # Armazena a mensagem digitada pelo usuário
    chave_base64 = ''           # Armazena a chave (em base64)
    erro = None                 # Armazena mensagens de erro, se houver

    if request.method == "POST":
        # Captura os dados do formulário
        mensagem_original = request.POST.get("mensagem", "")
        chave_base64 = request.POST.get("chave", "")
        acao = request.POST.get("acao")  # Qual botão foi clicado

        try:
            # Caso o usuário clique em "Gerar Chave"
            if acao == "gerar_chave":
                chave = gerar_chave()  # Gera uma chave aleatória de 32 bytes
                chave_base64 = base64.b64encode(chave).decode()  # Codifica em base64 para exibir no HTML
                resultado = "Nova chave gerada!"  # Mensagem de confirmação
            
            else:
                
                # Se for criptografar ou descriptografar, processa a chave

                if chave_base64:
                    try:
                        # Decodifica a chave da base64 para bytes
                        chave = base64.b64decode(chave_base64)
                    except (Error, ValueError):
                        raise ValueError("Chave inválida.")

                    # Valida se a chave tem exatamente 32 bytes (requisito AES-256)
                    if len(chave) != 32:
                        raise ValueError("A chave deve conter exatamente 32 bytes.")
                else:
                    raise ValueError("Informe uma chave ou gere uma nova.")

                # Criptografa a mensagem fornecida
                if acao == "criptografar":
                    resultado = criptografar(mensagem_original, chave)

                # Descriptografa a mensagem fornecida
                elif acao == "descriptografar":
                    try:
                        mensagem_corrigida = pad_base64(mensagem_original.strip())  # Corrige padding
                        resultado = descriptografar(mensagem_corrigida, chave)
                    except Exception:
                        resultado = "Erro ao descriptografar. Verifique a mensagem e a chave."

        except Exception as e:
            # Captura qualquer erro inesperado e exibe no template
            erro = f"Erro: {str(e)}"

    # Renderiza o template com os dados resultantes
    return render(request, "index.html", {
        "mensagem_original": mensagem_original,
        "resultado": resultado,
        "chave_base64": chave_base64,
        "erro": erro
    })
