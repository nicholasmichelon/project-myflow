"""
database/conexao.py

Responsável por abrir a conexão com o banco SQLite do MyFlow e por criar
as tabelas na primeira execução.

Uso:
    from database.conexao import criar_tabelas
    criar_tabelas()   # chame uma vez ao iniciar a aplicação

Relações:
    - um curso tem várias disciplinas  -> disciplinas.curso_id
    - um usuário tem apenas um curso   -> usuarios.curso_id
    - ao excluir um curso, as disciplinas e os usuários dele NÃO são
      apagados: apenas ficam sem curso (curso_id = NULL)
"""

import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent.parent / 'myflow.db'


def obter_conexao():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute('PRAGMA foreign_keys = ON')
    return conexao


def criar_tabelas():
    conexao = obter_conexao()
    try:
        conexao.executescript(
            """
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE COLLATE NOCASE,
                nivel TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                codigo TEXT NOT NULL UNIQUE COLLATE NOCASE,
                carga_horaria INTEGER NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0,
                curso_id INTEGER,
                FOREIGN KEY (curso_id) REFERENCES cursos (id)
                    ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                jornada TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                tempo_disponivel INTEGER NOT NULL,
                curso_id INTEGER,
                FOREIGN KEY (curso_id) REFERENCES cursos (id)
                    ON DELETE SET NULL
            );
            """
        )
        conexao.commit()
    finally:
        conexao.close()