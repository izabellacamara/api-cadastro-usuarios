# api-cadastro-usuarios
# 👤 API de Cadastro de Usuários

Uma API REST desenvolvida em Python para cadastro e gerenciamento de usuários.

O projeto permite criar usuários, realizar login, consultar, editar e excluir usuários, utilizando banco de dados SQLite.

---

## 🚀 Funcionalidades

- 👤 Criar usuário
- 🔐 Login
- 🔒 Armazenamento da senha em formato de hash
- 🔎 Buscar usuário por ID
- 📋 Listar usuários
- ✏️ Editar usuário
- 🗑️ Excluir usuário
- 💾 Banco de dados SQLite

---

## 🛠️ Tecnologias utilizadas

- 🐍 Python
- ⚡ FastAPI
- 🗄️ SQLite
- 🔐 Hashlib
- 📦 Pydantic

---

## 📌 Endpoints

| Método | Endpoint | Função |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| POST | `/usuarios` | Criar usuário |
| POST | `/login` | Realizar login |
| GET | `/usuarios` | Listar usuários |
| GET | `/usuarios/{id}` | Buscar usuário |
| PUT | `/usuarios/{id}` | Editar usuário |
| DELETE | `/usuarios/{id}` | Excluir usuário |

---

## 🔐 Segurança

As senhas não são armazenadas diretamente no banco de dados.

Antes de serem salvas, elas passam por uma função de hash.

> Este projeto foi desenvolvido para fins de estudo e prática de desenvolvimento de APIs.

---

## 📂 Estrutura do projeto

```text
api-cadastro-usuarios/
│
├── main.py
├── usuarios.db
└── README.md