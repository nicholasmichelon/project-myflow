import sqlite3
from pathlib import Path

CAMINHO = Path(__file__).resolve().parent / "banco.db"

conexao = sqlite3.connect(CAMINHO)

try:
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
        INSERT INTO usuarios_nova
        SELECT id, nome, email, jornada, objetivo,
               tempo_disponivel, curso_id
        FROM usuarios
    """)

    conexao.execute("DROP TABLE usuarios")
    conexao.execute(
        "ALTER TABLE usuarios_nova RENAME TO usuarios"
    )

    conexao.commit()
    print("Banco corrigido com sucesso!")

except Exception:
    conexao.rollback()
    raise

finally:
    conexao.close()