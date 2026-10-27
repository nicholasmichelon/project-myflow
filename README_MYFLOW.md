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

O `app.py` chama `inicializar_banco()`, que cria tabelas ausentes e migra bancos antigos para incluir `senha_hash` e `progresso_disciplinas`. Faça backup do banco antes de atualizar um projeto que contenha dados importantes. O ZIP de entrega omite `database/banco.db` intencionalmente para não sobrescrever os dados locais; mantenha seu arquivo existente nessa pasta.

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

- `MYFLOW_SECRET_KEY` pode ser definida como variável de ambiente. A chave padrão do `app.py` é apenas para desenvolvimento local.
- Não há recuperação de senha por e-mail nem proteção CSRF implementada. O projeto é adequado a um protótipo acadêmico local; antes de publicar na internet, implemente esses controles.
- A pasta `website/` é um projeto Docusaurus separado e não é necessária para executar a aplicação Flask.

## Verificações desta revisão

- Compilação de sintaxe dos arquivos Python.
- Compilação dos templates Jinja.
- Teste dos repositórios com SQLite temporário:
  - vários usuários compartilham um curso;
  - cada usuário mantém estado de conclusão diferente para a mesma disciplina;
  - o percentual de progresso é calculado por usuário;
  - e-mails duplicados são recusados;
  - migração de banco legado conserva usuários e estados de conclusão.

O servidor Flask não foi executado neste ambiente de revisão, pois Flask não está instalado no interpretador utilizado para os testes. A dependência está listada em `requirements.txt`; execute dentro do seu `.venv` para validar a interface no navegador.
