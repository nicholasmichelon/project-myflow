---
title: Visão geral do produto
sidebar_position: 1
description: Objetivo, funcionalidades existentes e escopo da versão atual do MyFlow.
---

# Visão geral do produto

O MyFlow organiza informações básicas da jornada de aprendizagem. O usuário cria um perfil, define seu contexto de estudo, associa-se a um curso e visualiza as disciplinas cadastradas nesse curso. A conclusão das disciplinas é individual, mesmo quando várias pessoas compartilham o mesmo curso.

## Funcionalidades implementadas

- **Cadastro de conta:** nome, e-mail, jornada de aprendizagem, objetivo, tempo disponível e senha.
- **Autenticação:** login por e-mail e senha; saída por formulário `POST`.
- **Curso:** cada usuário tem no máximo um curso associado. Cursos com o mesmo nome podem ser reutilizados por outros usuários quando o nível for compatível.
- **Disciplinas:** cada curso pode conter várias disciplinas. O código de uma disciplina não pode se repetir dentro do mesmo curso.
- **Progresso individual:** concluir ou reabrir uma disciplina registra o estado para o usuário autenticado, sem alterar o progresso dos outros usuários.
- **Cálculos de apoio:** carga horária total do curso e percentual de disciplinas concluídas para um usuário.

## O que ainda não está implementado

A proposta conceitual do MyFlow pode ser ampliada futuramente, mas os itens a seguir **não aparecem como fluxos implementados na versão do código anexado**:

- tarefas e divisão de tarefas em etapas;
- sugestão automática da próxima ação baseada no tempo disponível;
- sessões de estudo com duração realizada;
- agenda, calendário ou notificações;
- recuperação de senha por e-mail.

O campo `tempo_disponivel` é validado e armazenado no perfil, porém não é usado atualmente para sugerir tarefas. Esta documentação não trata esses itens como funcionalidades disponíveis.

## Papéis e dados

A versão atual não apresenta painel administrativo nem perfis de permissão diferentes. O fluxo principal é centrado em uma pessoa usuária autenticada. Os dados do curso e das disciplinas são compartilhados pelo cadastro do curso; o progresso é armazenado por par usuário-disciplina.

## Indicadores exibidos

O progresso percentual considera apenas as disciplinas pertencentes ao curso do usuário e divide a quantidade concluída pelo total de disciplinas. Se o curso não possui disciplinas, o resultado é `0.0%`.
