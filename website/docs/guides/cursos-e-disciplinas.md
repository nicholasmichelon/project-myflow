---
title: Cursos e disciplinas
sidebar_position: 3
description: Como cursos são compartilhados e como as disciplinas são cadastradas.
---

# Cursos e disciplinas

## Curso

Um curso tem `id`, `nome`, `nivel` e uma lista de disciplinas. O objeto `Curso` começa sem disciplinas; elas são gerenciadas pelos métodos `adicionar_disciplina()`, `remover_disciplina()` e `buscar_disciplina()`.

O banco considera o nome do curso único sem diferenciar maiúsculas/minúsculas. A aplicação também reutiliza cursos por nome, comparando o nível. O mesmo curso pode estar associado a vários usuários.

## Disciplina

Uma disciplina tem `id`, `nome`, `codigo` e `carga_horaria`. A carga horária é expressa em horas e deve ser um inteiro positivo. Não há atributo de professor na versão atual.

O código identifica a disciplina dentro de um curso. O mesmo código pode existir em cursos diferentes, mas não deve se repetir no mesmo curso. A classe `Disciplina` representa o catálogo da disciplina; ela não guarda o progresso de cada pessoa.

## Adicionar uma disciplina pela interface

1. Entre na conta e abra a página de disciplinas.
2. Informe nome, código e carga horária em horas.
3. Envie o formulário.
4. A aplicação valida os dados, adiciona a disciplina ao objeto `Curso` e chama `CursoRepository.atualizar()` para salvar as alterações.
5. Após o salvamento, a tela é recarregada com a lista e o progresso do usuário.

## Compartilhamento e separação de dados

O cadastro do curso e o catálogo de disciplinas são compartilhados por todos os usuários associados ao mesmo curso. Já a tabela de progresso usa o par `(usuario_id, disciplina_id)`, para que cada usuário possa marcar sua própria conclusão.

:::note Escopo da interface
Embora os repositórios tenham operações adicionais de consulta e exclusão, a interface web atual não oferece um fluxo de remoção de disciplinas. A documentação distingue as operações disponíveis no código das ações expostas nas páginas.
:::
