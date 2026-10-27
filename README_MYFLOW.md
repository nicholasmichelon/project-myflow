# MyFlow — instruções e revisão

## Executar localmente (Windows / VS Code)

1. Abra o terminal na pasta que contém `app.py`.
2. Instale as dependências no ambiente virtual:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Se estiver usando um banco antigo que ainda impede vários usuários de compartilhar o mesmo curso, faça uma cópia de segurança de `database/banco.db` e execute a migração uma vez:

   ```powershell
   .\.venv\Scripts\python.exe database\corrigir_banco.py
   ```

   O script informa se o banco já permite compartilhar cursos e não o migra novamente nesse caso.

4. Inicie o aplicativo:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

5. Acesse <http://127.0.0.1:5000>.

## Estrutura funcional

- `models/`: regras e objetos `Usuario`, `Curso` e `Disciplina`.
- `repository/`: operações SQLite dos objetos.
- `database/`: conexão, schema e migração compatível com curso compartilhado.
- `templates/`: cadastro do usuário, curso e disciplinas.
- `static/styles.css`: estilos das telas.
- `uml/`: diagramas de classes e sequência.

## Correções feitas nesta revisão

- Criado `templates/cadastro_disciplinas.html`, que era referenciado na rota Flask mas não existia no projeto recebido.
- Adicionados os estilos CSS da lista de disciplinas, resumo do curso, etiquetas e botão de retorno.
- Mantida a possibilidade de vários usuários usarem o mesmo curso.
- `CursoRepository.buscar_por_nome()` passou a comparar nomes com `casefold()` em Python; o `NOCASE` padrão do SQLite não trata corretamente toda capitalização de letras acentuadas.
- `Curso.buscar_disciplina()` agora compara códigos sem diferenciar capitalização, em sintonia com a regra de unicidade dentro do curso.
- `DisciplinaRepository.buscar_por_codigo()` aceita `curso_id` opcional, já que o código da disciplina é único **por curso**, e não globalmente.
- O setter `Usuario.curso` impede substituir diretamente um curso por outro sem removê-lo primeiro.
- O cadastro mostra mensagem amigável quando o e-mail já existe e mantém os valores preenchidos após erros.
- A migração `database/corrigir_banco.py` agora verifica se a alteração já foi aplicada antes de modificar a tabela.
- Atualizados os diagramas de sequência para refletir o fluxo real de cadastro em etapas.
- Adicionados arquivos `__init__.py` para explicitar os pacotes Python.

## Limitações conhecidas / próximos passos

- `Disciplina.concluida` está armazenado na disciplina do curso compartilhado. Portanto, se futuramente um usuário marcar uma disciplina como concluída, esse estado será comum a todos os usuários associados ao curso. Para progresso individual, será necessário criar uma relação própria entre usuário e disciplina.
- O projeto ainda não tem fluxo de login para usuários existentes. A sessão representa o usuário que acabou de se cadastrar.
- A chave secreta padrão em `app.py` é apenas para desenvolvimento local. Antes de publicar, defina a variável de ambiente `MYFLOW_SECRET_KEY`.
- A pasta `website/` parece ser um scaffold Docusaurus separado da aplicação Flask; ela não é necessária para executar `app.py`.

## Verificações executadas nesta revisão

- Sintaxe Python analisada em todos os arquivos `.py`.
- Templates Jinja compilados.
- Testes de integração dos repositórios contra um banco SQLite temporário:
  - dois usuários compartilham o mesmo curso;
  - disciplinas persistem e são recuperadas para ambos;
  - códigos duplicados com diferenças de maiúsculas/minúsculas são bloqueados dentro do curso;
  - e-mails duplicados são rejeitados;
  - substituição direta de curso é bloqueada;
  - migração executada contra um schema antigo e novamente sem danificar o banco.

O servidor HTTP Flask não foi executado neste ambiente de revisão porque Flask não está instalado no interpretador utilizado para os testes. A dependência está declarada em `requirements.txt`; execute o projeto no seu `.venv` para validar o fluxo no navegador.
