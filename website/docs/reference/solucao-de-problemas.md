---
title: Solução de problemas
sidebar_position: 1
description: Diagnóstico de Flask, SQLite, login e Docusaurus.
---

# Solução de problemas

## Falha ao importar Flask ou dotenv

Na raiz do projeto, ative o ambiente Python e execute:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## `no such table: tokens_recuperacao_senha`

O schema enviado não define a tabela usada na recuperação. A página [Recuperação de senha](../guides/recuperacao-senha.md) explica a discrepância. Não resolva apagando o banco ou ignorando o erro; faça backup e implemente uma migração validada.

## Não consigo entrar com conta antiga

Se a conta não possui `senha_hash`, um proprietário pode atribuir senha temporária pelo painel. Alternativamente, o projeto possui `scripts/definir_senha_usuario.py` para manutenção local. A senha inicial deve ser alterada pelo titular.

## Link de recuperação não chega por e-mail

Sem `MYFLOW_SMTP_HOST`, o código **imprime o link no terminal**. Para usar e-mail, configure as variáveis SMTP. Isso não resolve a ausência de tabela no schema.

## O servidor não inicia ou reinicia sessões

- Confirme que está na raiz do projeto, no diretório com `app.py`.
- A chave da sessão é aleatória quando `MYFLOW_SECRET_KEY` não está configurada; reinicializar encerra sessões.
- O arquivo atual executa `debug=True`. Não o execute externamente sem corrigir.

## `onBrokenMarkdownLinks` está obsoleto

Coloque a configuração dentro de `markdown.hooks.onBrokenMarkdownLinks` no `docusaurus.config.js` (em vez de usar opção no objeto raiz).

## `editUrl` contém valor inválido

Remova a propriedade `editUrl` das opções de `docs`; não a defina como `null`.

## `intro` encontrado em dois arquivos

Não mantenha simultaneamente `docs/intro.md` e `docs/intro.mdx` com o mesmo ID. Este portal atualizado contém apenas um documento introdutório.

## `@docusaurus/theme-mermaid` ou `@mermaid-js/layout-elk` ausente

Na pasta `website`, execute `npm ci` para instalar as dependências especificadas no `package-lock.json`; confira se `@docusaurus/core` e `@docusaurus/theme-mermaid` têm versões compatíveis. O `package.json` recebido fixa Docusaurus 3.10.2 e inclui `@mermaid-js/layout-elk@0.1.9`.

## Falha em `npm run build`

Confira os links internos, IDs do sidebar, nomes de arquivos, versões do Node e dependências instaladas. Execute `npm run build` depois de qualquer mudança.
