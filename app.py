"""Aplicação web Flask do MyFlow."""

import os
import secrets
import hashlib
import smtplib
from datetime import date, datetime, timedelta, timezone
from email.message import EmailMessage

from dotenv import load_dotenv

# Carrega as configurações locais do arquivo .env, se existir.
load_dotenv()

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
)
from werkzeug.security import check_password_hash, generate_password_hash
from database.conexao import obter_conexao

from models.usuarios import Usuario
from models.cursos import Curso
from models.disciplinas import Disciplina
from models.progresso_disciplina import ProgressoDisciplina
from models.tarefa import Tarefa
from models.sugestor_de_tarefas import SugestorDeTarefas

from repository.usuarios_repository import UsuarioRepository
from repository.cursos_repository import CursoRepository
from repository.progresso_disciplina_repository import ProgressoDisciplinaRepository
from repository.tarefas_repository import TarefaRepository

from database.conexao import inicializar_banco


app = Flask(__name__)
# Sem variável definida, gera uma chave aleatória para o uso local.
# Isso invalida as sessões quando o app é reiniciado, mas evita usar uma chave pública.
app.secret_key = os.environ.get("MYFLOW_SECRET_KEY") or secrets.token_urlsafe(32)

# Token de uso único para ativar o primeiro proprietário pela interface.
# Em ambiente local, é exibido no terminal quando ainda não há proprietários.
TOKEN_PROPRIETARIO = os.environ.get("MYFLOW_OWNER_SETUP_TOKEN") or secrets.token_urlsafe(24)
app.config["TOKEN_PROPRIETARIO"] = TOKEN_PROPRIETARIO


@app.context_processor
def disponibilizar_csrf_e_configuracao():
    """Disponibiliza token CSRF e informa se a configuração inicial está aberta."""
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)

    try:
        pode_configurar_proprietario = UsuarioRepository().contar_proprietarios() == 0
    except Exception:
        pode_configurar_proprietario = False

    return {
        "csrf_token": lambda: session.get("_csrf_token", ""),
        "pode_configurar_proprietario": pode_configurar_proprietario,
    }


@app.before_request
def proteger_formularios_post():
    """Validação CSRF simples para todos os formulários POST."""
    if request.method == "POST":
        token_sessao = session.get("_csrf_token", "")
        token_formulario = request.form.get("_csrf_token", "")
        if (
            not token_sessao
            or not token_formulario
            or not secrets.compare_digest(token_sessao, token_formulario)
        ):
            abort(400, description="Token de segurança inválido. Atualize a página e tente novamente.")


def usuario_da_sessao():
    """Recupera o usuário autenticado; não confia em papel guardado no cookie."""
    id_usuario = session.get("usuario_id")
    if id_usuario is None:
        return None
    return UsuarioRepository().buscar_por_id(id_usuario)


def exigir_proprietario():
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return None
    if not usuario.is_owner:
        abort(403, description="Esta área é exclusiva dos proprietários do MyFlow.")
    return usuario


def renderizar_cadastro_usuario(erro=None, status=200, form=None):
    return render_template(
        "cadastro.html",
        sucesso=None,
        erro=erro,
        form=form or {},
    ), status


def destino_usuario(usuario):
    """Encaminha contas existentes ao painel; contas novas completam o curso."""
    if usuario.curso is None:
        return url_for("pagina_curso")
    return url_for("pagina_dashboard")


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
                "Peça a um proprietário do MyFlow para definir uma senha inicial "
                "pela área administrativa."
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


# Recuperação de senha: tokens aleatórios, armazenados apenas como hash e de uso único.
TEMPO_TOKEN_RECUPERACAO_MINUTOS = 30
_ultimas_solicitacoes_recuperacao = {}

def _hash_token_recuperacao(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def _enviar_email_recuperacao(destinatario, link):
    """Envia por SMTP quando configurado; no modo local, registra o link no terminal."""
    host = os.environ.get("MYFLOW_SMTP_HOST")
    if not host:
        print(f"\n[MyFlow] Link de recuperação de senha para {destinatario}:\n{link}\n")
        return

    mensagem = EmailMessage()
    mensagem["Subject"] = "Redefinição de senha — MyFlow"
    mensagem["From"] = os.environ.get("MYFLOW_SMTP_FROM", os.environ.get("MYFLOW_SMTP_USER", "no-reply@myflow.local"))
    mensagem["To"] = destinatario
    mensagem.set_content(
        "Recebemos uma solicitação para redefinir a senha da sua conta MyFlow.\n\n"
        f"Acesse este link em até {TEMPO_TOKEN_RECUPERACAO_MINUTOS} minutos:\n{link}\n\n"
        "Se você não solicitou a alteração, ignore esta mensagem."
    )
    porta = int(os.environ.get("MYFLOW_SMTP_PORT", "587"))
    usuario_smtp = os.environ.get("MYFLOW_SMTP_USER")
    senha_smtp = os.environ.get("MYFLOW_SMTP_PASSWORD")
    with smtplib.SMTP(host, porta, timeout=15) as servidor:
        if os.environ.get("MYFLOW_SMTP_STARTTLS", "1") == "1":
            servidor.starttls()
        if usuario_smtp and senha_smtp:
            servidor.login(usuario_smtp, senha_smtp)
        servidor.send_message(mensagem)

@app.route("/esqueci-senha", methods=["GET", "POST"])
def pagina_esqueci_senha():
    """Solicita um link de redefinição sem revelar se o e-mail está cadastrado."""
    if request.method == "GET":
        return render_template("esqueci_senha.html", erro=None, sucesso=None, email="")

    email = request.form.get("email", "").strip()
    mensagem = (
        "Se o e-mail estiver cadastrado, enviaremos as instruções para redefinir a senha. "
        "Confira sua caixa de entrada."
    )
    agora = datetime.now(timezone.utc)
    chave_email = email.casefold()
    ultima = _ultimas_solicitacoes_recuperacao.get(chave_email)
    if email and (ultima is None or agora - ultima >= timedelta(minutes=2)):
        usuario = UsuarioRepository().buscar_por_email(email)
        if usuario is not None:
            token = secrets.token_urlsafe(32)
            hash_token = _hash_token_recuperacao(token)
            conexao = obter_conexao()
            try:
                conexao.execute(
                    "DELETE FROM tokens_recuperacao_senha WHERE usuario_id = ?",
                    (usuario.id,),
                )
                conexao.execute(
                    "INSERT INTO tokens_recuperacao_senha (usuario_id, token_hash, expira_em) VALUES (?, ?, ?)",
                    (usuario.id, hash_token, (agora + timedelta(minutes=TEMPO_TOKEN_RECUPERACAO_MINUTOS)).isoformat()),
                )
                conexao.commit()
            finally:
                conexao.close()
            link = url_for("pagina_redefinir_senha", token=token, _external=True)
            try:
                _enviar_email_recuperacao(usuario.email, link)
            except Exception:
                app.logger.exception("Não foi possível enviar o e-mail de recuperação do MyFlow.")
        _ultimas_solicitacoes_recuperacao[chave_email] = agora

    return render_template("esqueci_senha.html", erro=None, sucesso=mensagem, email=email)

@app.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def pagina_redefinir_senha(token):
    """Valida token de uso único e permite cadastrar uma nova senha."""
    hash_token = _hash_token_recuperacao(token)
    conexao = obter_conexao()
    try:
        registro = conexao.execute(
            "SELECT id, usuario_id, expira_em FROM tokens_recuperacao_senha "
            "WHERE token_hash = ? AND utilizado_em IS NULL",
            (hash_token,),
        ).fetchone()
    finally:
        conexao.close()

    agora = datetime.now(timezone.utc)
    valido = False
    if registro is not None:
        try:
            valido = datetime.fromisoformat(registro["expira_em"]) > agora
        except (TypeError, ValueError):
            valido = False
    if not valido:
        return render_template(
            "redefinir_senha.html", token=token, erro=(
                "Este link é inválido, já foi utilizado ou expirou. Solicite uma nova recuperação."
            ), sucesso=None,
        ), 400

    if request.method == "GET":
        return render_template("redefinir_senha.html", token=token, erro=None, sucesso=None)

    senha = request.form.get("nova_senha", "")
    confirmacao = request.form.get("confirmar_senha", "")
    if len(senha) < 8:
        return render_template("redefinir_senha.html", token=token, erro="A senha deve ter pelo menos 8 caracteres.", sucesso=None), 400
    if senha != confirmacao:
        return render_template("redefinir_senha.html", token=token, erro="A nova senha e a confirmação não coincidem.", sucesso=None), 400

    conexao = obter_conexao()
    try:
        cursor = conexao.execute(
            "UPDATE usuarios SET senha_hash = ? WHERE id = ?",
            (generate_password_hash(senha), registro["usuario_id"]),
        )
        if cursor.rowcount != 1:
            conexao.rollback()
            return render_template("redefinir_senha.html", token=token, erro="Não foi possível atualizar a senha. Solicite um novo link.", sucesso=None), 400
        conexao.execute(
            "UPDATE tokens_recuperacao_senha SET utilizado_em = ? WHERE id = ? AND utilizado_em IS NULL",
            (agora.isoformat(), registro["id"]),
        )
        conexao.execute(
            "DELETE FROM tokens_recuperacao_senha WHERE usuario_id = ? AND id != ?",
            (registro["usuario_id"], registro["id"]),
        )
        conexao.commit()
    finally:
        conexao.close()

    return render_template("redefinir_senha.html", token=token, erro=None, sucesso="Senha alterada com sucesso! Agora você já pode entrar no MyFlow com a nova senha." )

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


@app.route("/dashboard", methods=["GET"])
def pagina_dashboard():
    """Painel principal com resumo de estudos, tarefas e próxima recomendação."""
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))
    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    curso = CursoRepository().buscar_por_id(usuario.curso.id)
    if curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio_tarefas = TarefaRepository()
    tarefas = repositorio_tarefas.listar_do_usuario(usuario.id)
    pendentes = [t for t in tarefas if not t.concluida]
    concluidas = [t for t in tarefas if t.concluida]
    hoje = date.today().isoformat()
    atrasadas = [t for t in pendentes if t.esta_atrasada(hoje)]
    proximas = [t for t in pendentes if t.prazo and t.prazo >= hoje][:5]

    sugestor = SugestorDeTarefas(usuario.tempo_disponivel)
    sugestao = sugestor.sugerir_proxima_acao(tarefas, hoje=date.today())
    progresso = ProgressoDisciplinaRepository().calcular_progresso(
        usuario.id, curso.id
    )
    resumo_tarefas = repositorio_tarefas.resumo_do_usuario(usuario.id)

    return render_template(
        "dashboard.html",
        usuario=usuario,
        curso=curso,
        tarefas=tarefas,
        tarefas_pendentes=pendentes,
        tarefas_concluidas=concluidas,
        tarefas_atrasadas=atrasadas,
        tarefas_proximas=proximas,
        sugestao=sugestao,
        progresso_percentual=progresso,
        resumo_tarefas=resumo_tarefas,
        hoje=hoje,
    )


@app.route("/tarefas", methods=["GET", "POST"])
def pagina_tarefas():
    """Cria e lista tarefas pertencentes exclusivamente ao usuário conectado."""
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))
    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    curso = CursoRepository().buscar_por_id(usuario.curso.id)
    if curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio = TarefaRepository()
    form = {
        "titulo": request.form.get("titulo", "").strip() if request.method == "POST" else "",
        "descricao": request.form.get("descricao", "").strip() if request.method == "POST" else "",
        "prazo": request.form.get("prazo", "").strip() if request.method == "POST" else "",
        "prioridade": request.form.get("prioridade", "media").strip() if request.method == "POST" else "media",
        "duracao_estimada": request.form.get("duracao_estimada", "30").strip() if request.method == "POST" else "30",
        "disciplina_id": request.form.get("disciplina_id", "").strip() if request.method == "POST" else "",
    }

    if request.method == "POST":
        try:
            try:
                duracao = int(form["duracao_estimada"])
            except (TypeError, ValueError):
                raise ValueError("A duração estimada deve ser um número inteiro de minutos.")

            disciplina_id = None
            if form["disciplina_id"]:
                try:
                    disciplina_id = int(form["disciplina_id"])
                except (TypeError, ValueError):
                    raise ValueError("Selecione uma disciplina válida.")
                if not any(d.id == disciplina_id for d in curso.disciplinas):
                    raise ValueError("A disciplina selecionada não pertence ao seu curso.")

            tarefa = Tarefa(
                usuario_id=usuario.id,
                disciplina_id=disciplina_id,
                titulo=form["titulo"],
                descricao=form["descricao"],
                prazo=form["prazo"] or None,
                prioridade=form["prioridade"],
                duracao_estimada=duracao,
            )
            repositorio.criar(tarefa)
            session["mensagem_tarefas"] = "Tarefa criada com sucesso!"
            return redirect(url_for("pagina_tarefas"))
        except ValueError as erro:
            return render_template(
                "tarefas.html",
                usuario=usuario,
                curso=curso,
                tarefas=repositorio.listar_do_usuario(usuario.id),
                disciplinas=curso.disciplinas,
                sucesso=None,
                erro=str(erro),
                form=form,
                hoje=date.today().isoformat(),
            ), 400

    sucesso = session.pop("mensagem_tarefas", None)
    return render_template(
        "tarefas.html",
        usuario=usuario,
        curso=curso,
        tarefas=repositorio.listar_do_usuario(usuario.id),
        disciplinas=curso.disciplinas,
        sucesso=sucesso,
        erro=None,
        form=form,
        hoje=date.today().isoformat(),
    )


@app.route("/tarefas/<int:tarefa_id>/editar", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))
    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    curso = CursoRepository().buscar_por_id(usuario.curso.id)
    if curso is None:
        return redirect(url_for("pagina_curso"))

    repositorio = TarefaRepository()
    tarefa_atual = repositorio.buscar_por_id(tarefa_id, usuario.id)
    if tarefa_atual is None:
        session["mensagem_tarefas"] = "Tarefa não encontrada."
        return redirect(url_for("pagina_tarefas"))

    if request.method == "GET":
        form = {
            "titulo": tarefa_atual.titulo,
            "descricao": tarefa_atual.descricao,
            "prazo": tarefa_atual.prazo or "",
            "prioridade": tarefa_atual.prioridade,
            "duracao_estimada": str(tarefa_atual.duracao_estimada),
            "disciplina_id": str(tarefa_atual.disciplina_id or ""),
        }
        return render_template(
            "editar_tarefa.html", usuario=usuario, curso=curso,
            disciplinas=curso.disciplinas, tarefa=tarefa_atual,
            form=form, erro=None
        )

    form = {
        "titulo": request.form.get("titulo", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "prazo": request.form.get("prazo", "").strip(),
        "prioridade": request.form.get("prioridade", "media").strip(),
        "duracao_estimada": request.form.get("duracao_estimada", "").strip(),
        "disciplina_id": request.form.get("disciplina_id", "").strip(),
    }
    try:
        try:
            duracao = int(form["duracao_estimada"])
        except (TypeError, ValueError):
            raise ValueError("A duração estimada deve ser um número inteiro de minutos.")

        disciplina_id = None
        if form["disciplina_id"]:
            try:
                disciplina_id = int(form["disciplina_id"])
            except (TypeError, ValueError):
                raise ValueError("Selecione uma disciplina válida.")
            if not any(d.id == disciplina_id for d in curso.disciplinas):
                raise ValueError("A disciplina selecionada não pertence ao seu curso.")

        tarefa_atual.titulo = form["titulo"]
        tarefa_atual.descricao = form["descricao"]
        tarefa_atual.prazo = form["prazo"] or None
        tarefa_atual.prioridade = form["prioridade"]
        tarefa_atual.duracao_estimada = duracao
        tarefa_atual.disciplina_id = disciplina_id

        repositorio.atualizar(tarefa_atual)
        session["mensagem_tarefas"] = "Tarefa atualizada com sucesso."
        return redirect(url_for("pagina_tarefas"))
    except ValueError as erro:
        return render_template(
            "editar_tarefa.html", usuario=usuario, curso=curso,
            disciplinas=curso.disciplinas, tarefa=tarefa_atual,
            form=form, erro=str(erro)
        ), 400


@app.route("/tarefas/<int:tarefa_id>/acao", methods=["POST"])
def acao_tarefa(tarefa_id):
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))

    repositorio = TarefaRepository()
    tarefa = repositorio.buscar_por_id(tarefa_id, usuario.id)
    if tarefa is None:
        session["mensagem_tarefas"] = "Tarefa não encontrada."
        return redirect(url_for("pagina_tarefas"))

    acao = request.form.get("acao", "")
    if acao == "concluir":
        tarefa.concluir()
        repositorio.atualizar(tarefa)
        session["mensagem_tarefas"] = "Tarefa marcada como concluída."
    elif acao == "reabrir":
        tarefa.reabrir()
        repositorio.atualizar(tarefa)
        session["mensagem_tarefas"] = "Tarefa reaberta."
    elif acao == "excluir":
        repositorio.excluir(tarefa.id, usuario.id)
        session["mensagem_tarefas"] = "Tarefa excluída."
    else:
        session["mensagem_tarefas"] = "Ação de tarefa inválida."

    destino = request.form.get("origem", "tarefas")
    if destino == "agenda":
        return redirect(url_for("pagina_agenda"))
    return redirect(url_for("pagina_tarefas"))


@app.route("/agenda", methods=["GET"])
def pagina_agenda():
    """Agenda baseada nos prazos das tarefas do usuário conectado."""
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))
    if usuario.curso is None:
        return redirect(url_for("pagina_curso"))

    tarefas = TarefaRepository().listar_do_usuario(usuario.id)
    hoje = date.today().isoformat()
    return render_template(
        "agenda.html",
        usuario=usuario,
        tarefas=tarefas,
        hoje=hoje,
        sucesso=session.pop("mensagem_tarefas", None),
    )


@app.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    """Permite ao usuário editar seus dados e as próprias credenciais."""
    usuario = usuario_da_sessao()
    if usuario is None:
        session.clear()
        return redirect(url_for("pagina_login"))

    repositorio = UsuarioRepository()

    if request.method == "GET":
        sucesso = session.pop("mensagem_perfil", None)
        return render_template(
            "perfil.html", usuario=usuario, erro=None, sucesso=sucesso,
            form={
                "nome": usuario.nome,
                "email": usuario.email,
                "jornada": usuario.jornada,
                "objetivo": usuario.objetivo,
                "tempo_disponivel": str(usuario.tempo_disponivel),
            },
        )

    form = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "jornada": request.form.get("jornada", "").strip(),
        "objetivo": request.form.get("objetivo", "").strip(),
        "tempo_disponivel": request.form.get("tempo_disponivel", "").strip(),
    }
    senha_atual = request.form.get("senha_atual", "")
    nova_senha = request.form.get("nova_senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")

    email_alterado = form["email"].casefold() != usuario.email.casefold()
    senha_solicitada = bool(nova_senha or confirmar_senha)

    try:
        if email_alterado or senha_solicitada:
            if not usuario.senha_hash or not check_password_hash(usuario.senha_hash, senha_atual):
                raise ValueError("Informe sua senha atual corretamente para alterar o e-mail ou a senha.")

        existente = repositorio.buscar_por_email(form["email"])
        if existente is not None and existente.id != usuario.id:
            raise ValueError("Este e-mail já está cadastrado em outra conta.")

        try:
            tempo = int(form["tempo_disponivel"])
        except (TypeError, ValueError):
            raise ValueError("O tempo disponível deve ser um número inteiro de minutos.")

        if senha_solicitada:
            if len(nova_senha) < 8:
                raise ValueError("A nova senha deve ter pelo menos 8 caracteres.")
            if nova_senha != confirmar_senha:
                raise ValueError("A nova senha e a confirmação não coincidem.")

        usuario.nome = form["nome"]
        usuario.email = form["email"]
        usuario.jornada = form["jornada"]
        usuario.objetivo = form["objetivo"]
        usuario.tempo_disponivel = tempo

        if senha_solicitada:
            usuario.senha_hash = generate_password_hash(nova_senha)

        repositorio.atualizar(usuario)
        session["mensagem_perfil"] = "Seus dados foram atualizados com sucesso."
        return redirect(url_for("pagina_perfil"))

    except ValueError as erro:
        return render_template(
            "perfil.html", usuario=usuario, erro=str(erro), sucesso=None, form=form
        ), 400


@app.route("/configurar-proprietario", methods=["GET", "POST"])
def configurar_primeiro_proprietario():
    """Ativação inicial, disponível somente enquanto ainda não há proprietários."""
    repositorio = UsuarioRepository()
    if repositorio.contar_proprietarios() > 0:
        usuario_atual = usuario_da_sessao()
        if usuario_atual and usuario_atual.is_owner:
            return redirect(url_for("pagina_admin_usuarios"))
        abort(404)

    usuario = usuario_da_sessao()
    if usuario is None:
        return redirect(url_for("pagina_login"))

    if request.method == "GET":
        return render_template("configurar_proprietario.html", usuario=usuario, erro=None)

    token_informado = request.form.get("token_configuracao", "")
    token_esperado = app.config["TOKEN_PROPRIETARIO"]
    if not secrets.compare_digest(token_informado, token_esperado):
        return render_template(
            "configurar_proprietario.html",
            usuario=usuario,
            erro="Código de configuração inválido. Confira o terminal do Flask.",
        ), 403

    if not repositorio.definir_proprietario(usuario.id, True):
        return render_template(
            "configurar_proprietario.html",
            usuario=usuario,
            erro="Não foi possível ativar o perfil de proprietário.",
        ), 400

    session["mensagem_admin"] = "Perfil de proprietário ativado com sucesso."
    return redirect(url_for("pagina_admin_usuarios"))


@app.route("/admin/usuarios", methods=["GET"])
def pagina_admin_usuarios():
    proprietario = exigir_proprietario()
    if proprietario is None:
        return redirect(url_for("pagina_login"))

    sucesso = session.pop("mensagem_admin", None)
    contas = UsuarioRepository().listar_para_administracao()
    return render_template(
        "admin_usuarios.html",
        usuario=proprietario,
        contas=contas,
        sucesso=sucesso,
        erro=None,
    )


@app.route("/admin/usuarios/<int:id_usuario>/excluir", methods=["POST"])
def admin_excluir_usuario(id_usuario):
    proprietario = exigir_proprietario()
    if proprietario is None:
        return redirect(url_for("pagina_login"))

    repositorio = UsuarioRepository()
    alvo = repositorio.buscar_por_id(id_usuario)
    if alvo is None:
        session["mensagem_admin"] = "A conta selecionada não foi encontrada."
        return redirect(url_for("pagina_admin_usuarios"))

    if alvo.id == proprietario.id:
        session["mensagem_admin"] = "Você não pode excluir a própria conta enquanto está conectado."
        return redirect(url_for("pagina_admin_usuarios"))

    if alvo.is_owner:
        session["mensagem_admin"] = "Contas de proprietários não podem ser excluídas por este painel. Remova o papel de proprietário primeiro."
        return redirect(url_for("pagina_admin_usuarios"))

    if repositorio.excluir(id_usuario):
        session["mensagem_admin"] = (
            f"A conta de {alvo.email} foi excluída. O e-mail e o hash da senha foram removidos."
        )
    else:
        session["mensagem_admin"] = "Não foi possível excluir a conta selecionada."
    return redirect(url_for("pagina_admin_usuarios"))


@app.route("/admin/usuarios/<int:id_usuario>/papel", methods=["POST"])
def admin_alterar_papel(id_usuario):
    proprietario = exigir_proprietario()
    if proprietario is None:
        return redirect(url_for("pagina_login"))

    repositorio = UsuarioRepository()
    alvo = repositorio.buscar_por_id(id_usuario)
    acao = request.form.get("acao", "")

    if alvo is None:
        session["mensagem_admin"] = "A conta selecionada não foi encontrada."
        return redirect(url_for("pagina_admin_usuarios"))

    if alvo.id == proprietario.id:
        session["mensagem_admin"] = "Você não pode alterar seu próprio papel por esta tela."
        return redirect(url_for("pagina_admin_usuarios"))

    if acao == "promover":
        if not alvo.senha_hash:
            session["mensagem_admin"] = (
                "Defina uma senha para esta conta antes de promovê-la a proprietária."
            )
        else:
            repositorio.definir_proprietario(id_usuario, True)
            session["mensagem_admin"] = f"{alvo.email} agora é proprietário do MyFlow."
    elif acao == "rebaixar":
        if not alvo.is_owner:
            session["mensagem_admin"] = "Essa conta já é uma conta comum."
        elif repositorio.contar_proprietarios() <= 1:
            session["mensagem_admin"] = "Não é possível remover o último proprietário."
        else:
            repositorio.definir_proprietario(id_usuario, False)
            session["mensagem_admin"] = f"O papel de proprietário de {alvo.email} foi removido."
    else:
        session["mensagem_admin"] = "Ação de administração inválida."

    return redirect(url_for("pagina_admin_usuarios"))


@app.route("/admin/usuarios/<int:id_usuario>/senha", methods=["POST"])
def admin_definir_senha(id_usuario):
    proprietario = exigir_proprietario()
    if proprietario is None:
        return redirect(url_for("pagina_login"))

    repositorio = UsuarioRepository()
    alvo = repositorio.buscar_por_id(id_usuario)
    if alvo is None:
        session["mensagem_admin"] = "A conta selecionada não foi encontrada."
        return redirect(url_for("pagina_admin_usuarios"))

    if alvo.is_owner:
        session["mensagem_admin"] = "Por segurança, use a página Meu perfil para alterar a senha de uma conta proprietária."
        return redirect(url_for("pagina_admin_usuarios"))

    senha = request.form.get("nova_senha", "")
    confirmacao = request.form.get("confirmar_senha", "")
    if len(senha) < 8 or senha != confirmacao:
        session["mensagem_admin"] = "A senha deve ter pelo menos 8 caracteres e coincidir com a confirmação."
        return redirect(url_for("pagina_admin_usuarios"))

    alvo.senha_hash = generate_password_hash(senha)
    try:
        repositorio.atualizar(alvo)
        session["mensagem_admin"] = (
            f"Senha definida para {alvo.email}. O sistema armazenou apenas o hash. "
            "Informe a senha temporária diretamente ao usuário e oriente-o a alterá-la em Meu perfil."
        )
    except ValueError as erro:
        session["mensagem_admin"] = str(erro)

    return redirect(url_for("pagina_admin_usuarios"))


if __name__ == "__main__":
    inicializar_banco()
    if not os.environ.get("MYFLOW_SECRET_KEY"):
        print("[MyFlow] Aviso: MYFLOW_SECRET_KEY não definida; as sessões serão encerradas ao reiniciar o app.")
    repositorio_inicial = UsuarioRepository()
    if repositorio_inicial.contar_proprietarios() == 0:
        print("\n[MyFlow] Ainda não há proprietário configurado.")
        if os.environ.get("MYFLOW_OWNER_SETUP_TOKEN"):
            print("[MyFlow] Use o token definido na variável MYFLOW_OWNER_SETUP_TOKEN.")
        else:
            print("[MyFlow] Token de configuração do primeiro proprietário:")
            print(TOKEN_PROPRIETARIO)
        print("[MyFlow] Faça login com sua conta e abra /configurar-proprietario.\n")
    # use_reloader=False mantém válido o token de ativação inicial exibido no terminal.
    app.run(debug=True, use_reloader=False)
