# MyFlow — Projeto de POO

Aplicação web feita com Flask e SQLite para cadastro de usuários, cursos e disciplinas, com login e acompanhamento individual do progresso.

## Executar localmente (Windows / VS Code)

1. Abra o terminal na pasta que contém `app.py`.
2. Instale as dependências:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Se o banco antigo ainda tiver `UNIQUE` isolado em `usuarios.curso_id`, faça backup de `database/banco.db` e execute uma vez:

   ```powershell
   .\.venv\Scripts\python.exe database\corrigir_banco.py
   ```

   Se você já executou essa migração e o banco permite que usuários compartilhem cursos, não precisa repeti-la.

4. Inicie o aplicativo:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

5. Acesse <http://127.0.0.1:5000>.

O `app.py` chama `inicializar_banco()`, que cria tabelas ausentes e migra bancos antigos para incluir `senha_hash` e `progresso_disciplinas`. Faça backup do banco antes de atualizar um projeto que contenha dados importantes. O ZIP de entrega não inclui `database/banco.db` para não sobrescrever nem compartilhar dados locais; ao executar o aplicativo pela primeira vez, o banco será criado nessa pasta.

Por padrão, o modo de depuração do Flask fica desativado. Para ativá-lo apenas durante o desenvolvimento local no PowerShell, execute `$env:MYFLOW_DEBUG = "1"` antes de iniciar o aplicativo.

## Funcionalidades

- Cadastro de usuário com nome, e-mail, jornada, objetivo, tempo diário e senha.
- Login e saída da conta.
- Um curso associado a cada usuário; o mesmo curso pode ser compartilhado por vários usuários.
- Várias disciplinas em cada curso.
- Progresso de conclusão separado por usuário e disciplina.

## Organização principal

- `models/`: classes `Usuario`, `Curso`, `Disciplina` e `ProgressoDisciplina`.
- `repository/`: repositórios SQLite, incluindo `ProgressoDisciplinaRepository`.
- `database/`: conexão, `schema.sql` e migrações.
- `templates/`: cadastro, login, curso e disciplinas.
- `static/styles.css`: estilo das páginas.
- `uml/`: diagramas de classes e sequência.
- `scripts/definir_senha_usuario.py`: define senha para uma conta antiga que foi criada antes da implementação do login.

## Login e contas antigas

Novos usuários criam uma senha de pelo menos 8 caracteres. O MyFlow armazena o hash gerado por `werkzeug.security`, nunca a senha em texto puro.

Contas criadas antes da implementação do login têm `senha_hash` vazio. Para definir uma senha de uma dessas contas no ambiente local, execute:

```powershell
.\.venv\Scripts\python.exe scripts\definir_senha_usuario.py
```

O script solicita o e-mail existente e a nova senha. Ainda não há recuperação de senha por e-mail configurada.

## Progresso individual

As disciplinas pertencem ao curso compartilhado. A conclusão individual é armazenada em `progresso_disciplinas`, com chave composta `(usuario_id, disciplina_id)`. Assim, duas pessoas do mesmo curso podem ter progressos diferentes.

A migração de dados antigos copia o estado de conclusão legado para os usuários que já estavam associados ao curso no momento da atualização. Essa migração é executada uma única vez. Novos usuários começam com seu próprio progresso pendente.

A coluna antiga `disciplinas.concluida`, quando existente em um banco anterior, é mantida apenas para compatibilidade durante a migração; a aplicação atual não a utiliza como fonte de progresso individual.

## Segurança e limitações

- `MYFLOW_SECRET_KEY` pode ser definida como variável de ambiente. A chave padrão do `app.py` é apenas para desenvolvimento local e não deve ser usada em uma publicação real.
- O modo de depuração do Flask fica desligado por padrão e só é ativado quando `MYFLOW_DEBUG` é igual a `1`.
- Não há recuperação de senha por e-mail, proteção CSRF nem limite de tentativas de login implementados. O projeto é adequado a um protótipo acadêmico local; antes de publicar na internet, implemente esses controles.
- A pasta `website/` é um projeto Docusaurus separado e não é necessária para executar a aplicação Flask.

## Verificações realizadas na revisão

- Verificação de sintaxe dos 16 arquivos Python principais e dos 4 templates HTML/Jinja.
- Testes dos modelos e repositórios usando um banco SQLite temporário, sem alterar o banco local.
- Verificação de usuários compartilhando um curso e mantendo progresso individual.
- Verificação de e-mails repetidos, nomes de cursos repetidos, códigos de disciplinas repetidos e IDs de disciplinas inexistentes.
- Verificação de rollback: uma falha ao salvar um curso não deixa registros parciais nem IDs inconsistentes nos objetos em memória.
- Verificação da migração de um banco legado, incluindo preservação do progresso e remoção da restrição antiga que impedia vários usuários de compartilharem um curso.
- O servidor Flask não foi iniciado nesta revisão porque Flask não estava instalado no interpretador de análise. A dependência está listada em `requirements.txt`; execute dentro do seu `.venv` para validar o fluxo completo no navegador.
