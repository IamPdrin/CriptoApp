
# 🔐 Projeto Django - Criptografia AES-256

Este é um projeto web criado com Django que permite criptografar e descriptografar mensagens usando o algoritmo AES-256 no modo CBC.

---

## 🚀 Tecnologias utilizadas

- Python 3.10+
- Django 5+
- Cryptography (biblioteca de criptografia)
- Bootstrap 5 (via CDN)
- HTML + JavaScript (para copiar mensagens)

---

## 🧰 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/IamPdrin/CriptoApp.git
```

---

### 2. Crie e ative o ambiente virtual

```cmd
python -m venv venv
```

#### • Windows:

```cmd
venv\Scripts\activate
```

#### • Mac/Linux:

```cmd
source venv/bin/activate
```

---

### 3. Instale as dependências

```cmd
pip install django
pip install cryptography
```

---

### 4. Rode o servidor Django

```cmd
python manage.py runserver
```

---

### 5. Acesse no navegador

```
http://127.0.0.1:8000/
```

---

## 📄 Observação

Esse projeto usa uma chave AES de 32 bytes (256 bits), modo CBC, IV aleatório e padding PKCS7.  
A interface foi construída com Django + Bootstrap 5 e possui botões para copiar os resultados com JavaScript.

---

## 📄 Licença

Projeto livre para fins educacionais. 😄
