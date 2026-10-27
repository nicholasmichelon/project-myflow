"""Aplicação web Flask do MyFlow."""

import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models.usuarios import Usuario
from models.cursos import Curso
from models.disciplinas import Disciplina
from models.progresso_disciplina import ProgressoDisciplina

from repository.usuarios_repository import UsuarioRepository
from repository.cursos_repository import CursoRepository
from repository.progresso_disciplina_repository import ProgressoDisciplinaRepository

from database.conexao import inicializar_banco


app = Flask(__name__)
app.secret_key = os.environ.get(
    "MYFLOW_SECRET_KEY",
    "chave-local-myflow-apenas-desenvolvimento",
)


def renderizar_cadastro_usuario(erro=None, status=200, form=None):
    return render_template(
        "cadastro.html",
        sucesso=None,
        erro=erro,
        form=form or {},
    ), status


def destino_usuario(usuario):
    """Encaminha usuário para a próxima etapa ainda não concluída."""
    if usuario.curso is None:
        return url_for("pagina_curso")
    return url_for("pagina_disciplinas")


@app.route("/", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "GET":
        return render_template(
            "cadastro.html",
            sucesso=None,
            erro=None,
            form={},
        )

    form = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "jornada": request.form.get("jornada", "").strip(),
        "objetivo": request.form.get("objetivo", "").strip(),
        "tempo_disponivel": request.form.get("tempo_disponivel", "").strip(),
    }
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")

    if len(senha) < 8:
        return renderizar_cadastro_usuario(
            "A senha deve ter pelo menos 8 caracteres.",
            status=400,
            form=form,
        )

    if senha != confirmar_senha:
        return renderizar_cadastro_usuario(
            "As senhas não coincidem.",
            status=400,
            form=form,
        )

    try:
        try:
            tempo_disponivel = int(form["tempo_disponivel"])
        except (TypeError, ValueError):
            raise ValueError(
                "Informe o tempo disponível em minutos usando um número inteiro."
            )

        if tempo_disponivel <= 0:
            raise ValueError("O tempo disponível deve ser maior que zero.")

        repositorio_usuario = UsuarioRepository()

        if repositorio_usuario.buscar_por_email(form["email"]) is not None:
            return renderizar_cadastro_usuario(
                "Já existe um cadastro com esse e-mail. Entre na sua conta.",
                status=409,
                form=form,
            )

        usuario = Usuario(
            nome=form["nome"],
            email=form["email"],
            jornada=form["jornada"],
            objetivo=form["objetivo"],
            tempo_disponivel=tempo_disponivel,
            senha_hash=generate_password_hash(senha),
        )

        id_usuario = repositorio_usuario.inserir(usuario)

        # Uma sessão nova evita reaproveitar dados de outra conta.
        session.clear()
        session["usuario_id"] = id_usuario

        return redirect(url_for("pagina_curso"))

    except ValueError as erro:
        mensagem = str(erro)
        if "email" in mensagem.casefold() and (
            "unique" in mensagem.casefold() or "já existe" in mensagem.casefold()
        ):
            mensagem = "Já existe um cadastro com esse e-mail. Entre na sua conta."

        return renderizar_cadastro_usuario(
            mensagem,
            status=400,
            form=form,
        )


@app.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "GET":
        return render_template("login.html", erro=None, email="")

    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")

    usuario = UsuarioRepository().buscar_por_email(email)

    # A mesma mensagem para usuário inexistente e senha incorreta reduz
    # a exposição de quais e-mails estão cadastrados.
    if usuario is None:
        return render_template(
            "login.html",
            erro="E-mail ou senha inválidos.",
            email=email,
        ), 401

    if not usuario.senha_hash:
        return render_template(
            "login.html",
            erro=(
                "Esta conta foi criada antes do login por senha. "
                "Defina uma senha pelo script "
                "scripts/definir_senha_usuario.py e tente novamente."
            ),
            email=email,
        ), 400

    if not check_password_hash(usuario.senha_hash, senha):
        return render_template(
            "login.html",
            erro="E-mail ou senha inválidos.",
            email=email,
        ), 401

    session.clear()
    session["usuario_id"] = usuario.id
    return redirect(destino_usuario(usuario))


@app.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("pagina_login"))


@app.route("/curso", methods=["GET", "POST"])
def pagina_curso():
    id_usuario = session.get("usuario_id")
    if id_usuario is None:
        return redirect(url_for("pagina_login"))

    repositorio_usuario = UsuarioRepository()
    usuario = repositorio_usuario.buscar_por_id(id_usuario)

    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))

    if usuario.curso is not None:
        return render_template(
            "cadastro_curso.html",
            usuario=usuario,
            erro=None,
            form={},
        )

    if request.method == "GET":
        return render_template(
            "cadastro_curso.html",
            usuario=usuario,
            erro=None,
            form={},
        )

    nome = request.form.get("nome", "").strip()
    nivel = request.form.get("nivel", "").strip()
    repositorio_curso = CursoRepository()
    curso_criado_nesta_requisicao = False
    curso = None

    try:
        # Cursos são compartilhados: reutiliza o cadastro existente.
        curso = repositorio_curso.buscar_por_nome(nome)

        if curso is not None:
            if curso.nivel.casefold() != nivel.casefold():
                raise ValueError(
                    "Já existe um curso com esse nome em outro nível."
                )
        else:
            curso = Curso(nome=nome, nivel=nivel)
            repositorio_curso.inserir(curso)
            curso_criado_nesta_requisicao = True

        if not usuario.definir_curso(curso):
            raise ValueError("Este usuário já possui um curso associado.")

        atualizado = repositorio_usuario.atualizar(usuario)
        if not atualizado:
            raise ValueError("Não foi possível associar o curso ao usuário.")

        return redirect(url_for("pagina_curso"))

    except ValueError as erro:
        if (
            curso_criado_nesta_requisicao
            and curso is not None
            and curso.id is not None
        ):
            usuario_atualizado = repositorio_usuario.buscar_por_id(id_usuario)
            if usuario_atualizado is None or usuario_atualizado.curso is None:
                repositorio_curso.excluir(curso.id)

        usuario = repositorio_usuario.buscar_por_id(id_usuario)
        return (
            render_template(
                "cadastro_curso.html",
                usuario=usuario,
                erro=str(erro),
                form={"nome": nome, "nivel": nivel},
            ),
            400,
        )


@app.route("/disciplinas", methods=["GET", "POST"])
def pagina_disciplinas():
    id_usuario = session.get("usuario_id")
    if id_usuario is None:
        return redirect(url_for("pagina_login"))

    repositorio_usuario = UsuarioRepository()
    usuario = repositorio_usuario.buscar_por_id(id_usuario)

    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))

    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio_curso = CursoRepository()
    curso = repositorio_curso.buscar_por_id(usuario.curso.id)
    if curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio_progresso = ProgressoDisciplinaRepository()

    if request.method == "POST":
        acao = request.form.get("acao", "adicionar")

        # O progresso de conclusão é salvo separadamente para cada usuário.
        if acao in {"concluir", "reabrir"}:
            try:
                disciplina_id = int(request.form.get("disciplina_id", ""))
            except (TypeError, ValueError):
                return redirect(url_for("pagina_disciplinas"))

            disciplina = next(
                (d for d in curso.disciplinas if d.id == disciplina_id),
                None,
            )
            if disciplina is None:
                return redirect(url_for("pagina_disciplinas"))

            progresso = repositorio_progresso.buscar(
                usuario.id, disciplina_id
            )
            if progresso is None:
                progresso = ProgressoDisciplina(
                    usuario_id=usuario.id,
                    disciplina_id=disciplina_id,
                    concluida=False,
                )

            mudou = (
                progresso.concluir()
                if acao == "concluir"
                else progresso.reabrir()
            )

            if mudou:
                repositorio_progresso.salvar(progresso)
                session["mensagem_disciplinas"] = (
                    f"Progresso de '{disciplina.nome}' atualizado."
                )
            else:
                session["mensagem_disciplinas"] = (
                    "O progresso dessa disciplina já estava nesse estado."
                )

            return redirect(url_for("pagina_disciplinas"))

        # Cadastro de uma nova disciplina compartilhada pelo curso.
        nome = request.form.get("nome", "").strip()
        codigo = request.form.get("codigo", "").strip()
        carga_texto = request.form.get("carga_horaria", "").strip()
        form = {
            "nome": nome,
            "codigo": codigo,
            "carga_horaria": carga_texto,
        }

        try:
            try:
                carga_horaria = int(carga_texto)
            except (TypeError, ValueError):
                raise ValueError("A carga horária deve ser um número inteiro.")

            disciplina = Disciplina(
                nome=nome,
                codigo=codigo,
                carga_horaria=carga_horaria,
            )

            if not curso.adicionar_disciplina(disciplina):
                raise ValueError(
                    "Já existe uma disciplina com esse código neste curso."
                )

            if not repositorio_curso.atualizar(curso):
                raise ValueError("Não foi possível salvar a disciplina.")

            session["mensagem_disciplinas"] = (
                f"Disciplina '{disciplina.nome}' cadastrada com sucesso!"
            )
            return redirect(url_for("pagina_disciplinas"))

        except ValueError as erro:
            curso = repositorio_curso.buscar_por_id(usuario.curso.id)
            if curso is None:
                return redirect(url_for("pagina_curso"))

            status_por_disciplina = repositorio_progresso.listar_status_do_curso(
                usuario.id, curso.id
            )
            itens_disciplinas = [
                {
                    "disciplina": disciplina,
                    "concluida": status_por_disciplina.get(disciplina.id, False),
                }
                for disciplina in curso.disciplinas
            ]

            return (
                render_template(
                    "cadastro_disciplinas.html",
                    usuario=usuario,
                    curso=curso,
                    disciplinas=curso.disciplinas,
                    itens_disciplinas=itens_disciplinas,
                    progresso_percentual=repositorio_progresso.calcular_progresso(
                        usuario.id, curso.id
                    ),
                    sucesso=None,
                    erro=str(erro),
                    form=form,
                ),
                400,
            )

    sucesso = session.pop("mensagem_disciplinas", None)
    status_por_disciplina = repositorio_progresso.listar_status_do_curso(
        usuario.id, curso.id
    )
    itens_disciplinas = [
        {
            "disciplina": disciplina,
            "concluida": status_por_disciplina.get(disciplina.id, False),
        }
        for disciplina in curso.disciplinas
    ]
    progresso_percentual = repositorio_progresso.calcular_progresso(
        usuario.id, curso.id
    )

    return render_template(
        "cadastro_disciplinas.html",
        usuario=usuario,
        curso=curso,
        disciplinas=curso.disciplinas,
        itens_disciplinas=itens_disciplinas,
        progresso_percentual=progresso_percentual,
        sucesso=sucesso,
        erro=None,
        form={},
    )


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
