import sqlite3
from pathlib import Path


PASTA_DATABASE = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_DATABASE / "banco.db"
CAMINHO_SCHEMA = PASTA_DATABASE / "schema.sql"


def obter_conexao():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    conexao = obter_conexao()

    try:
        with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as arquivo:
            script = arquivo.read()

        conexao.executescript(script)
    finally:
        conexao.close()


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")