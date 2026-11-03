"""Define uma senha para uma conta antiga que ainda não possui senha.

Uso local: .venv\\Scripts\\python.exe scripts\\definir_senha_usuario.py
"""

import getpass
import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from werkzeug.security import generate_password_hash
from database.conexao import inicializar_banco, obter_conexao


def main():
    inicializar_banco()

    email = input("E-mail da conta existente: ").strip()
    senha = getpass.getpass("Nova senha (mínimo 8 caracteres): ")
    confirmacao = getpass.getpass("Digite a senha novamente: ")

    if len(senha) < 8:
        print("Erro: a senha deve ter pelo menos 8 caracteres.")
        return 1

    if senha != confirmacao:
        print("Erro: as senhas não coincidem.")
        return 1

    conexao = obter_conexao()
    try:
        usuario = conexao.execute(
            "SELECT id FROM usuarios WHERE email = ?",
            (email,),
        ).fetchone()

        if usuario is None:
            print("Nenhuma conta encontrada com esse e-mail.")
            return 1

        hash_senha = generate_password_hash(senha)
        conexao.execute(
            "UPDATE usuarios SET senha_hash = ? WHERE id = ?",
            (hash_senha, usuario["id"]),
        )
        conexao.commit()
        print("Senha definida. Agora você pode entrar pela tela de login.")
        return 0
    finally:
        conexao.close()


if __name__ == "__main__":
    raise SystemExit(main())
