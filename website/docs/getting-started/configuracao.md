---
title: Configuração e variáveis de ambiente
sidebar_position: 2
description: Configurações disponíveis para execução local do MyFlow.
---

# Configuração e variáveis de ambiente

A aplicação consulta duas variáveis de ambiente no `app.py`. Elas são lidas diretamente pelo Python; o projeto não declara uma biblioteca para carregar automaticamente um arquivo `.env`.

## `MYFLOW_SECRET_KEY`

Usada pelo Flask para assinar a sessão do navegador. O código contém um valor padrão destinado apenas ao desenvolvimento local. Para definir uma chave no PowerShell antes de iniciar a aplicação:

```powershell
$env:MYFLOW_SECRET_KEY = "troque-por-uma-chave-local-segura"
python app.py
```

Defina o valor real fora do código-fonte e não o publique em documentação, Git ou mensagens. O exemplo acima é um marcador ilustrativo, não uma chave pronta para produção.

## `MYFLOW_DEBUG`

O modo de depuração é desativado por padrão. Para ativá-lo temporariamente durante o desenvolvimento local:

```powershell
$env:MYFLOW_DEBUG = "1"
python app.py
```

Feche o terminal ou remova a variável após o teste. Não publique a aplicação com o modo de depuração ligado.

## Dependências Python

O arquivo `requirements.txt` declara:

- `Flask` — rotas, sessão e renderização de templates;
- `Werkzeug` — funções para gerar e verificar hash de senha.

SQLite faz parte da biblioteca padrão do Python usada pelo projeto. As dependências Node do Docusaurus ficam isoladas em `website/package.json`.
