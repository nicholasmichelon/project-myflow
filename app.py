import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from models.usuarios import Usuario
from models.cursos import Curso
from models.disciplinas import Disciplina

from repository.usuarios_repository import UsuarioRepository
from repository.cursos_repository import CursoRepository

from database.conexao import inicializar_banco


app = Flask(__name__)
# A chave padrão serve apenas para desenvolvimento local.
# Defina MYFLOW_SECRET_KEY no ambiente antes de publicar a aplicação.
app.secret_key = os.environ.get(
    "MYFLOW_SECRET_KEY",
    "chave-local-myflow-apenas-desenvolvimento",
)


def renderizar_cadastro_usuario(erro=None, status=200, form=None):
    return (
        render_template(
            "cadastro.html",
            sucesso=None,
            erro=erro,
            form=form or {},
        ),
        status,
    )


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

        # Evita exibir o erro técnico de restrição UNIQUE para o usuário.
        if repositorio_usuario.buscar_por_email(form["email"]) is not None:
            return renderizar_cadastro_usuario(
                "Já existe um cadastro com esse e-mail. Use outro e-mail.",
                status=409,
                form=form,
            )

        usuario = Usuario(
            nome=form["nome"],
            email=form["email"],
            jornada=form["jornada"],
            objetivo=form["objetivo"],
            tempo_disponivel=tempo_disponivel,
        )

        id_usuario = repositorio_usuario.inserir(usuario)
        session["usuario_id"] = id_usuario

        return redirect(url_for("pagina_curso"))

    except ValueError as erro:
        mensagem = str(erro)
        if "usuarios.email" in mensagem.lower() or (
            "unique constraint failed" in mensagem.lower()
            and "email" in mensagem.lower()
        ):
            mensagem = "Já existe um cadastro com esse e-mail. Use outro e-mail."

        return renderizar_cadastro_usuario(
            mensagem,
            status=400,
            form=form,
        )


@app.route("/curso", methods=["GET", "POST"])
def pagina_curso():
    id_usuario = session.get("usuario_id")

    if id_usuario is None:
        return redirect(url_for("pagina_cadastro"))

    repositorio_usuario = UsuarioRepository()
    usuario = repositorio_usuario.buscar_por_id(id_usuario)

    if usuario is None:
        session.pop("usuario_id", None)
        return redirect(url_for("pagina_cadastro"))

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
        # Os cursos são compartilhados: reutiliza o cadastro existente.
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
        # Se o curso foi criado nesta requisição e não foi associado,
        # tenta removê-lo para não deixar registro órfão.
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
        return redirect(url_for("pagina_cadastro"))

    repositorio_usuario = UsuarioRepository()
    usuario = repositorio_usuario.buscar_por_id(id_usuario)

    if usuario is None:
        session.pop("usuario_id", None)
        return redirect(url_for("pagina_cadastro"))

    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio_curso = CursoRepository()
    curso = repositorio_curso.buscar_por_id(usuario.curso.id)

    if curso is None:
        return redirect(url_for("pagina_curso"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo = request.form.get("codigo", "").strip()
        carga_texto = request.form.get("carga_horaria", "").strip()
        form = {
            "nome": nome,
            "codigo": codigo,
            "carga_horaria": carga_texto,
        }

        try:
            carga_horaria = int(carga_texto)
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
            # Recarrega a lista do banco para não mostrar alteração não salva.
            curso = repositorio_curso.buscar_por_id(usuario.curso.id)
            if curso is None:
                return redirect(url_for("pagina_curso"))

            return (
                render_template(
                    "cadastro_disciplinas.html",
                    usuario=usuario,
                    curso=curso,
                    disciplinas=curso.disciplinas,
                    sucesso=None,
                    erro=str(erro),
                    form=form,
                ),
                400,
            )

    sucesso = session.pop("mensagem_disciplinas", None)

    return render_template(
        "cadastro_disciplinas.html",
        usuario=usuario,
        curso=curso,
        disciplinas=curso.disciplinas,
        sucesso=sucesso,
        erro=None,
        form={},
    )


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
