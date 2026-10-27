"""Migra a tabela usuarios para permitir que vários usuários compartilhem um curso.

Execute uma vez, com o Flask parado:
    python database/corrigir_banco.py

A migração preserva os IDs e os registros existentes. Se o banco já estiver
corrigido, o script informa isso e não faz alterações.
"""

import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "banco.db"


def coluna_curso_tem_unique(conexao):
    """Verifica se existe um índice UNIQUE composto apenas por curso_id."""
    indices = conexao.execute("PRAGMA index_list('usuarios')").fetchall()

    for indice in indices:
        nome_indice = indice[1]
        unico = bool(indice[2])

        if not unico:
            continue

        # O nome do índice é retornado pelo próprio SQLite.
        colunas = conexao.execute(
            f'PRAGMA index_info("{nome_indice.replace(chr(34), chr(34) * 2)}")'
        ).fetchall()

        nomes_colunas = [coluna[2] for coluna in colunas]
        if nomes_colunas == ["curso_id"]:
            return True

    return False


def migrar():
    if not CAMINHO_BANCO.exists():
        raise FileNotFoundError(
            f"Banco não encontrado: {CAMINHO_BANCO}. "
            "Inicialize-o primeiro executando database/conexao.py."
        )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        tabelas = {
            linha[0]
            for linha in conexao.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

        if "usuarios" not in tabelas or "cursos" not in tabelas:
            raise RuntimeError(
                "O banco não possui as tabelas usuarios e cursos. "
                "Confira database/schema.sql."
            )

        if not coluna_curso_tem_unique(conexao):
            print(
                "Nenhuma restrição UNIQUE isolada em usuarios.curso_id "
                "foi encontrada. O banco já permite compartilhar cursos."
            )
            return

        # A instrução deve ocorrer antes de iniciar uma transação.
        conexao.execute("PRAGMA foreign_keys = OFF")
        conexao.execute("BEGIN")

        conexao.execute("""
            CREATE TABLE usuarios_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                jornada TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                tempo_disponivel INTEGER NOT NULL
                    CHECK (tempo_disponivel > 0),
                curso_id INTEGER,
                FOREIGN KEY (curso_id)
                    REFERENCES cursos(id)
                    ON DELETE SET NULL
            )
        """)

        conexao.execute("""
            INSERT INTO usuarios_nova (
                id, nome, email, jornada, objetivo,
                tempo_disponivel, curso_id
            )
            SELECT
                id, nome, email, jornada, objetivo,
                tempo_disponivel, curso_id
            FROM usuarios
        """)

        conexao.execute("DROP TABLE usuarios")
        conexao.execute(
            "ALTER TABLE usuarios_nova RENAME TO usuarios"
        )

        problemas = conexao.execute("PRAGMA foreign_key_check").fetchall()
        if problemas:
            raise sqlite3.IntegrityError(
                f"Falha na verificação de chaves estrangeiras: {problemas}"
            )

        conexao.commit()
        print(
            "Migração concluída. Vários usuários agora podem compartilhar "
            "o mesmo curso."
        )

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.close()


if __name__ == "__main__":
    migrar()
