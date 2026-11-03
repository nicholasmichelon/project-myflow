---
id: intro
title: Documentação do MyFlow
slug: /intro
sidebar_position: 1
description: Ponto de entrada para entender, executar e manter o projeto MyFlow.
---

# MyFlow, por dentro

O MyFlow é um protótipo web acadêmico que permite cadastrar uma conta, associar um curso, organizar as disciplinas desse curso e acompanhar a conclusão de cada disciplina individualmente.

<div className="doc-callout doc-callout--blue">
  <strong>O que esta documentação cobre</strong>
  <p>O comportamento descrito aqui foi baseado nos arquivos do projeto anexado: aplicação Flask, modelos, repositórios, templates, schema SQLite e fontes UML. Funcionalidades planejadas mas ainda não implementadas são identificadas como tal.</p>
</div>

## Comece pelo seu objetivo

<div className="doc-link-grid">
  <a className="doc-link-card" href="/docs/product/visao-geral"><span className="doc-link-card__eyebrow">01 · Produto</span><strong>Entender o MyFlow</strong><span>Escopo implementado, conceitos principais e limites atuais.</span></a>
  <a className="doc-link-card" href="/docs/getting-started/instalacao"><span className="doc-link-card__eyebrow">02 · Execução</span><strong>Rodar localmente</strong><span>Ambiente Python, dependências, banco e servidor Flask.</span></a>
  <a className="doc-link-card" href="/docs/architecture/arquitetura"><span className="doc-link-card__eyebrow">03 · Engenharia</span><strong>Conhecer a arquitetura</strong><span>Como interface, modelos, repositórios e SQLite se conectam.</span></a>
  <a className="doc-link-card" href="/docs/reference/uml"><span className="doc-link-card__eyebrow">04 · Diagramas</span><strong>Explorar o UML</strong><span>Diagramas de classes e de sequência com os arquivos-fonte.</span></a>
</div>

## Visão rápida

| Elemento | Tecnologia ou responsabilidade |
|---|---|
| Aplicação web | Flask, com rotas para cadastro, login, curso e disciplinas |
| Interface | Templates HTML/Jinja e `static/styles.css` |
| Domínio | `Usuario`, `Curso`, `Disciplina` e `ProgressoDisciplina` |
| Persistência | SQLite, acessado por classes de repositório |
| Segurança de senha | Hash de senha por `werkzeug.security` |
| Documentação | Docusaurus e Markdown/MDX |

## Fluxo principal

```mermaid
flowchart LR
    A[Cadastro da conta] --> B[Associar ou criar curso]
    B --> C[Adicionar disciplinas]
    C --> D[Marcar disciplinas concluídas]
    D --> E[Consultar progresso individual]
```

:::info Sobre o escopo
O projeto guarda o tempo disponível informado no cadastro, mas a versão anexada ainda não contém classes de tarefas, sessões de estudo nem um mecanismo que sugira a próxima ação. Consulte [Visão geral do produto](./product/visao-geral.md) para distinguir as funcionalidades existentes das ideias futuras.
:::
