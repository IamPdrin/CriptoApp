# Importa as classes e funções necessárias para criptografia simétrica (AES) com modo CBC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Importa funções para adicionar/remover padding (PKCS7) — necessário para AES funcionar corretamente com tamanhos variados
from cryptography.hazmat.primitives import padding

# Fornece um backend padrão seguro e compatível com os algoritmos utilizados
from cryptography.hazmat.backends import default_backend

# Importa bibliotecas padrão do Python
import os        # Para gerar bytes aleatórios (usado em IV e chave)
import base64    # Para codificar e decodificar dados em Base64 (facilita o envio e armazenamento)


# -------------------------------------------------------------------------------------
# Função que gera uma chave de 32 bytes (256 bits) para uso com AES-256
def gerar_chave():
    return os.urandom(32)  # Gera 32 bytes aleatórios (256 bits)


# -------------------------------------------------------------------------------------
# Função para criptografar uma mensagem de texto com AES-256 no modo CBC
def criptografar(mensagem, chave):
    iv = os.urandom(16)  # Gera um IV (vetor de inicialização) de 16 bytes para o modo CBC

    # Prepara o padding da mensagem usando PKCS7 para garantir múltiplos de 16 bytes
    padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes (bloco AES)
    mensagem_padded = padder.update(mensagem.encode()) + padder.finalize()  # Adiciona o padding na mensagem

    # Cria o objeto de cifra AES-256 com modo CBC e o IV gerado
    cipher = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend()) # Default backend é seguro e compatível (motor do Cipher, SSL, etc.)
    encryptor = cipher.encryptor()  # Cria o "cifrador"

    # Criptografa a mensagem com padding
    ciphertext = encryptor.update(mensagem_padded) + encryptor.finalize()

    # Retorna o IV + ciphertext codificados em Base64 (para fácil transporte/armazenamento)
    return base64.b64encode(iv + ciphertext).decode() # retorna o ciphertext_b64 como string (resultado da criptografia)


# -------------------------------------------------------------------------------------
# Função para descriptografar a mensagem cifrada (em base64), usando a mesma chave AES
def descriptografar(ciphertext_b64, chave):
    dados = base64.b64decode(ciphertext_b64)  # Decodifica os dados de Base64 para bytes
    iv = dados[:16]           # Extrai os primeiros 16 bytes como IV
    ciphertext = dados[16:]   # O restante são os dados criptografados (ciphertext)

    # Cria o objeto de cifra com a mesma chave e IV para descriptografar
    cipher = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()  # Cria o "decifrador"

    # Descriptografa e obtém os dados com padding
    mensagem_padded = decryptor.update(ciphertext) + decryptor.finalize() #update() aplica a descriptografia e finalize() completa o processo
    # O resultado é a mensagem com padding aplicado, que precisa ser removido

    # Remove o padding para recuperar a mensagem original
    unpadder = padding.PKCS7(128).unpadder() #unpadder() prepara para remover o padding
    mensagem = unpadder.update(mensagem_padded) + unpadder.finalize() #update() aplica a remoção do padding e finalize() completa o processo

    return mensagem.decode()  # Retorna a mensagem original como string

#O Criptography utiliza um padrão para todas funções de criptografia, update e finalize, o que muda mesmo é o tipo de função que você está chamando (encryptor ou decryptor).

# O que é AES?
# AES (Advanced Encryption Standard) é um algoritmo de criptografia simétrica que opera com blocos de 128 bits.
# Aqui usamos AES-256, ou seja, uma chave de 256 bits (32 bytes), garantindo alto nível de segurança.

# O que é CBC?
# CBC (Cipher Block Chaining) é um modo de operação onde cada bloco é criptografado após ser combinado (XOR) com o bloco anterior.
# O primeiro bloco usa um IV (Initialization Vector).

# Por que usar CBC?
# CBC é seguro e mais resistente a padrões repetidos do que ECB. É simples e eficaz para dados genéricos.
# Outros modos:
# - ECB: inseguro, repete blocos idênticos.
# - CFB/OFB: transforma AES em cifrador de fluxo.
# - GCM: além de criptografar, autentica (segurança extra).

# O que é PKCS7?
# PKCS7 é um esquema de padding usado para preencher os blocos que não são múltiplos de 16 bytes (128 bits), exigência do AES.

# O que é o Cipher?
# É o objeto central da criptografia, que junta: algoritmo (AES), modo (CBC), chave e IV.
# Ele cria o encryptor (para criptografar) e decryptor (para descriptografar).

# O que é o encryptor?
# É o "motor" que aplica a criptografia nos dados. Ele recebe os dados com padding e retorna os blocos criptografados.

# Como funciona a função gerar_chave?
# Gera 32 bytes aleatórios com segurança criptográfica — isso é a chave AES-256.

# Como funciona criptografar()?
# Adiciona padding à mensagem, cria o objeto Cipher com a chave e IV, criptografa, junta IV + ciphertext e retorna em base64.

# Como funciona descriptografar()?
# Separa IV do ciphertext, recria o Cipher com a chave e IV, descriptografa, remove padding e retorna a mensagem original.

# Possível pergunta: por que base64?
# Porque o ciphertext e IV são bytes, e o base64 converte isso para uma string segura para exibir, armazenar ou enviar em HTML.

# Possível pergunta: o que acontece se a chave estiver errada?
# A descriptografia vai falhar e gerar exceção — pois o padding será inválido ou a mensagem será ilegível.

# Possível pergunta: qual a importância do IV?
# Ele impede que mensagens iguais resultem em ciphertexts iguais, protegendo contra análise de padrões.

