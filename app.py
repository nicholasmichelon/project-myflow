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
app.secret_key = "chave-local-myflow-altere-depois"


@app.route("/", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "GET":
        return render_template(
            "cadastro.html",
            sucesso=None,
            erro=None
        )

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    jornada = request.form.get("jornada", "").strip()
    objetivo = request.form.get("objetivo", "").strip()
    tempo_texto = request.form.get(
        "tempo_disponivel", ""
    ).strip()

    try:
        tempo_disponivel = int(tempo_texto)

        usuario = Usuario(
            nome=nome,
            email=email,
            jornada=jornada,
            objetivo=objetivo,
            tempo_disponivel=tempo_disponivel,
        )

        repositorio_usuario = UsuarioRepository()
        id_usuario = repositorio_usuario.inserir(usuario)

        session["usuario_id"] = id_usuario

        return redirect(url_for("pagina_curso"))

    except ValueError as erro:
        return render_template(
            "cadastro.html",
            sucesso=None,
            erro=str(erro)
        ), 400


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
            erro=None
        )

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        nivel = request.form.get("nivel", "").strip()

        try:
            repositorio_curso = CursoRepository()

            # Procura um curso já cadastrado.
            curso = repositorio_curso.buscar_por_nome(nome)

            if curso is not None:
                # Reutiliza o registro, desde que o nível seja igual.
                if curso.nivel.casefold() != nivel.casefold():
                    raise ValueError(
                        "Já existe um curso com esse nome "
                        "cadastrado em outro nível."
                    )
            else:
                # Cria um curso somente se ele ainda não existir.
                curso = Curso(nome=nome, nivel=nivel)
                repositorio_curso.inserir(curso)

            if not usuario.definir_curso(curso):
                raise ValueError(
                    "Este usuário já possui um curso associado."
                )

            atualizado = repositorio_usuario.atualizar(usuario)

            if not atualizado:
                raise ValueError(
                    "Não foi possível associar o curso ao usuário."
                )

            return redirect(url_for("pagina_curso"))

        except ValueError as erro:
            usuario = repositorio_usuario.buscar_por_id(id_usuario)

            return render_template(
                "cadastro_curso.html",
                usuario=usuario,
                erro=str(erro)
            ), 400

    return render_template(
        "cadastro_curso.html",
        usuario=usuario,
        erro=None
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
        carga_texto = request.form.get(
            "carga_horaria", ""
        ).strip()

        try:
            carga_horaria = int(carga_texto)

            disciplina = Disciplina(
                nome=nome,
                codigo=codigo,
                carga_horaria=carga_horaria,
            )

            adicionada = curso.adicionar_disciplina(disciplina)

            if not adicionada:
                raise ValueError(
                    "Já existe uma disciplina com esse código no curso."
                )

            atualizado = repositorio_curso.atualizar(curso)

            if not atualizado:
                raise ValueError(
                    "Não foi possível atualizar o curso."
                )

            session["mensagem_disciplinas"] = (
                f"Disciplina '{disciplina.nome}' cadastrada com sucesso!"
            )

            return redirect(url_for("pagina_disciplinas"))

        except ValueError as erro:
            curso = repositorio_curso.buscar_por_id(usuario.curso.id)

            return render_template(
                "cadastro_disciplinas.html",
                usuario=usuario,
                curso=curso,
                disciplinas=curso.disciplinas,
                sucesso=None,
                erro=str(erro),
            ), 400

    sucesso = session.pop("mensagem_disciplinas", None)

    return render_template(
        "cadastro_disciplinas.html",
        usuario=usuario,
        curso=curso,
        disciplinas=curso.disciplinas,
        sucesso=sucesso,
        erro=None,
    )


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)