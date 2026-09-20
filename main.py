from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib

app = FastAPI()


# =========================
# BANCO DE DADOS
# =========================

conexao = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

conexao.commit()


# =========================
# MODELOS
# =========================

class Usuario(BaseModel):
    nome: str
    email: str
    senha: str


class Login(BaseModel):
    email: str
    senha: str


# =========================
# FUNÇÃO PARA CRIPTOGRAFAR
# =========================

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# =========================
# INÍCIO DA API
# =========================

@app.get("/")
def inicio():
    return {
        "mensagem": "API de cadastro de usuários funcionando!"
    }


# =========================
# CRIAR USUÁRIO
# =========================

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):

    senha_hash = criptografar_senha(usuario.senha)

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
            """,
            (usuario.nome, usuario.email, senha_hash)
        )

        conexao.commit()

        return {
            "mensagem": "Usuário criado com sucesso!"
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Este email já está cadastrado."
        )


# =========================
# LOGIN
# =========================

@app.post("/login")
def login(dados: Login):

    senha_hash = criptografar_senha(dados.senha)

    cursor.execute(
        """
        SELECT id, nome, email
        FROM usuarios
        WHERE email = ? AND senha = ?
        """,
        (dados.email, senha_hash)
    )

    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos."
        )

    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2]
        }
    }


# =========================
# LISTAR USUÁRIOS
# =========================

@app.get("/usuarios")
def listar_usuarios():

    cursor.execute(
        "SELECT id, nome, email FROM usuarios"
    )

    usuarios = cursor.fetchall()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2]
        })

    return resultado


# =========================
# BUSCAR USUÁRIO
# =========================

@app.get("/usuarios/{id}")
def buscar_usuario(id: int):

    cursor.execute(
        """
        SELECT id, nome, email
        FROM usuarios
        WHERE id = ?
        """,
        (id,)
    )

    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2]
    }


# =========================
# EDITAR USUÁRIO
# =========================

@app.put("/usuarios/{id}")
def editar_usuario(id: int, usuario: Usuario):

    senha_hash = criptografar_senha(usuario.senha)

    cursor.execute(
        """
        UPDATE usuarios
        SET nome = ?, email = ?, senha = ?
        WHERE id = ?
        """,
        (
            usuario.nome,
            usuario.email,
            senha_hash,
            id
        )
    )

    conexao.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "mensagem": "Usuário atualizado com sucesso!"
    }


# =========================
# EXCLUIR USUÁRIO
# =========================

@app.delete("/usuarios/{id}")
def excluir_usuario(id: int):

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (id,)
    )

    conexao.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "mensagem": "Usuário excluído com sucesso!"
    }