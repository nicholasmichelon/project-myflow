---
title: Documentação do MyFlow
sidebar_position: 1
description: Portal oficial de referência funcional e técnica do projeto.
---

# MyFlow, por dentro

O **MyFlow** organiza a jornada de estudos por meio de cursos, disciplinas, tarefas e prioridades. O portal documenta a implementação em **Python, Flask e SQLite**, incluindo o painel do usuário, a agenda, o sugestor por regras e as funcionalidades de conta.

<div className="doc-callout doc-callout--blue"><strong>Documentação baseada no código</strong><p>Atualizada para o projeto recebido em novembro de 2026. As funcionalidades existentes são diferenciadas das lacunas de implementação. O aplicativo Flask e este portal Docusaurus são sistemas independentes.</p></div>

<div className="doc-link-grid">
  <a className="doc-link-card" href="/docs/product/visao-geral"><span className="doc-link-card__eyebrow">01 · Produto</span><strong>Funcionalidades</strong><span>Conheça o escopo atual, os perfis e as principais telas.</span></a>
  <a className="doc-link-card" href="/docs/guides/tarefas"><span className="doc-link-card__eyebrow">02 · Produtividade</span><strong>Tarefas e agenda</strong><span>Crie tarefas, defina prioridades e acompanhe os prazos.</span></a>
  <a className="doc-link-card" href="/docs/getting-started/instalacao"><span className="doc-link-card__eyebrow">03 · Execução</span><strong>Executar localmente</strong><span>Inicie Flask e o portal de documentação sem misturar os ambientes.</span></a>
  <a className="doc-link-card" href="/docs/architecture/arquitetura"><span className="doc-link-card__eyebrow">04 · Engenharia</span><strong>Arquitetura e UML</strong><span>Entenda modelos, repositórios, rotas e dados.</span></a>
</div>

## Módulos documentados

| Módulo | Conteúdo |
|---|---|
| Aprendizagem | Cadastro, curso compartilhado, disciplinas e progresso individual |
| Produtividade | Dashboard, tarefas pessoais, sugestão da próxima ação e agenda |
| Conta | Login, perfil, troca de credenciais e controle de sessão |
| Administração | Ativação de proprietário, papéis e gerenciamento de contas |
| Recuperação | Rotas de redefinição e configuração SMTP; **dependência de tabela ausente no schema anexado** |

## Jornada resumida

```mermaid
flowchart LR
    Cadastro[Cadastro e login] --> Curso[Curso e disciplinas]
    Curso --> Painel[Dashboard]
    Painel --> Tarefas[Tarefas e agenda]
    Tarefas --> Sugestao[Sugestão por regras]
    Curso --> Progresso[Progresso individual]
```

:::warning Antes de executar a recuperação de senha
O código fornecido consulta a tabela `tokens_recuperacao_senha`, ausente do `database/schema.sql` fornecido. Consulte [Limitações e pendências](./reference/seguranca-e-limitacoes.md) antes de testar esse recurso em um banco novo.
:::
