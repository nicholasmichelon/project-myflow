# MyFlow — Projeto de POO

Aplicação web feita com Flask e SQLite para cadastro de usuários, cursos, disciplinas e tarefas, com login, painel do aluno, sugestão de próxima ação, agenda e acompanhamento individual do progresso.

## Executar localmente (VS Code)

Abra o terminal na pasta que contém `app.py`. No macOS/Linux, execute:

```bash
python3 -m venv .venv  # somente se ainda não existir
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

No Windows PowerShell, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Acesse <http://127.0.0.1:5000>. O ZIP não inclui `database/banco.db`, para não sobrescrever os dados que você já possui; mantenha o arquivo local dentro da pasta `database/`. A inicialização cria as tabelas novas (incluindo tarefas) em um banco existente.

Se o banco antigo ainda tiver `UNIQUE` isolado em `usuarios.curso_id`, faça uma cópia de segurança e execute uma vez a migração específica (`database/corrigir_banco.py`), apenas se essa restrição ainda estiver presente.

O `app.py` chama `inicializar_banco()`, que cria tabelas ausentes e migra bancos antigos para incluir `senha_hash` e `progresso_disciplinas`. Faça backup do banco antes de atualizar um projeto que contenha dados importantes. O ZIP de entrega omite `database/banco.db` intencionalmente para não sobrescrever os dados locais; mantenha seu arquivo existente nessa pasta.

## Funcionalidades

- Cadastro de usuário com nome, e-mail, jornada, objetivo, tempo diário e senha.
- Login e saída da conta.
- Um curso associado a cada usuário; o mesmo curso pode ser compartilhado por vários usuários.
- Várias disciplinas em cada curso.
- Progresso de conclusão separado por usuário e disciplina.
- Painel `/dashboard` com resumo do curso, progresso, tarefas concluídas/pendentes/atrasadas e sugestão da próxima ação.
- Gerenciamento de tarefas em `/tarefas`: criar, editar, concluir, reabrir e excluir tarefas individuais.
- Agenda em `/agenda` baseada nos prazos das tarefas.
- O sugestor considera tarefas pendentes que cabem no tempo diário do usuário e prioriza atrasos, prioridade, prazo e duração.

## Organização principal

- `models/`: classes `Usuario`, `Curso`, `Disciplina`, `ProgressoDisciplina`, `Tarefa` e `SugestorDeTarefas`.
- `repository/`: repositórios SQLite, incluindo `ProgressoDisciplinaRepository` e `TarefaRepository`.
- `database/`: conexão, `schema.sql` e migrações.
- `templates/`: cadastro, login, curso, disciplinas, painel, tarefas, edição de tarefa, agenda, perfil e administração.
- `static/styles.css`: estilo das páginas.
- `uml/`: diagramas de classes e sequência.
- `scripts/definir_senha_usuario.py`: script legado opcional para manutenção local; contas antigas também podem ter senha inicial definida pela área administrativa.

## Login, perfil e administração de contas

Novos usuários criam uma senha de pelo menos 8 caracteres. O MyFlow armazena o hash gerado por `werkzeug.security`, nunca a senha em texto puro.

- A rota `/login` autentica usuários existentes.
- A rota `/perfil` permite editar dados pessoais e trocar o e-mail ou a senha. Para alterar e-mail ou senha, é necessário informar a senha atual.
- A rota `/admin/usuarios` é exclusiva de proprietários: lista as contas sem expor hashes, permite definir uma senha inicial/temporária para contas comuns antigas, conceder/remover papel de proprietário e excluir contas comuns.
- Excluir conta remove seu e-mail e hash da senha; a área administrativa não permite excluir a própria conta ativa nem excluir uma conta que ainda tenha o papel de proprietário.
- O primeiro proprietário é ativado pela interface em `/configurar-proprietario`. Faça login com a conta que será proprietária e use o token mostrado no terminal quando o app iniciar sem proprietários. O token funciona apenas enquanto ainda não existe proprietário. Se preferir, configure `MYFLOW_OWNER_SETUP_TOKEN` no ambiente antes de iniciar.
- Contas antigas sem senha podem receber uma senha inicial pela área administrativa, sem usar o terminal. O proprietário deve transmitir essa senha temporária diretamente ao titular e orientá-lo a alterá-la em `Meu perfil`.

## Dashboard, tarefas, sugestão e agenda

- Depois de entrar, usuários que já possuem um curso são encaminhados para `/dashboard`.
- Cada tarefa pertence a um usuário e pode estar associada opcionalmente a uma disciplina do curso desse usuário. Campos: título, descrição, prazo, prioridade e duração estimada em minutos.
- O usuário pode criar, editar, concluir, reabrir e excluir as próprias tarefas. O repositório sempre limita consultas/alterações ao `usuario_id` autenticado.
- `/agenda` lista as tarefas por prazo, destacando as atrasadas.
- `SugestorDeTarefas` recomenda uma tarefa pendente que caiba no tempo disponível informado no perfil. A regra prioriza tarefas atrasadas, depois prioridade declarada, prazo mais próximo e menor duração. Não utiliza IA externa.
- A tabela `tarefas` é criada automaticamente na inicialização em bancos existentes, sem remover usuários/cursos/disciplina.

## Progresso individual

As disciplinas pertencem ao curso compartilhado. A conclusão individual é armazenada em `progresso_disciplinas`, com chave composta `(usuario_id, disciplina_id)`. Assim, duas pessoas do mesmo curso podem ter progressos diferentes.

A migração de dados antigos copia o estado de conclusão legado para os usuários que já estavam associados ao curso no momento da atualização. Essa migração é executada uma única vez. Novos usuários começam com seu próprio progresso pendente.

A coluna antiga `disciplinas.concluida`, quando existente em um banco anterior, é mantida apenas para compatibilidade durante a migração; a aplicação atual não a utiliza como fonte de progresso individual.

## Segurança e limitações

- `MYFLOW_SECRET_KEY` deve ser definida como variável de ambiente para manter sessões entre reinicializações e em qualquer implantação fora de testes locais. Se não for definida, o app gera uma chave aleatória a cada execução e invalida as sessões quando reinicia.
- Os formulários POST validam token CSRF. O projeto continua sendo um protótipo acadêmico; antes de publicar na internet, revise o armazenamento de segredos, HTTPS, limitação de tentativas de login e recuperação segura de senha.
- A pasta `website/` é um projeto Docusaurus separado e não é necessária para executar a aplicação Flask.

## Verificações desta revisão

- Compilação de sintaxe dos arquivos Python.
- Compilação dos templates Jinja.
- Testes de modelo/repositório para criar, listar, concluir, editar e excluir tarefas, isolamento entre usuários e recomendação conforme o tempo disponível.
- Teste dos repositórios com SQLite temporário:
  - vários usuários compartilham um curso;
  - cada usuário mantém estado de conclusão diferente para a mesma disciplina;
  - o percentual de progresso é calculado por usuário;
  - e-mails duplicados são recusados;
  - migração de banco legado conserva usuários e estados de conclusão.

O servidor Flask não foi executado neste ambiente de revisão, pois Flask não está instalado no interpretador utilizado para os testes. A dependência está listada em `requirements.txt`; execute dentro do seu `.venv` para validar a interface no navegador.


## Testes dos modelos e repositórios de tarefas

Com o ambiente virtual ativado, execute:

```bash
python -m unittest discover -s tests -v
```

Os testes usam um banco SQLite temporário e não alteram o `database/banco.db` do usuário.
