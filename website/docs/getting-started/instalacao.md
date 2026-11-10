---
title: Instalação e execução local
sidebar_position: 1
description: Executar MyFlow Flask e Docusaurus em ambientes separados.
---

# Instalação e execução local

O repositório contém **duas aplicações independentes**: o MyFlow em Flask e o portal de documentação em Docusaurus.

## 1. Requisitos

| Ferramenta | Uso |
|---|---|
| Python 3.10+ | Aplicação Flask e testes |
| pip e venv | Dependências Python |
| Node.js compatível com Docusaurus 3.10.2 | Site de documentação |
| npm | Dependências e build Docusaurus |

## 2. Aplicação Flask (Windows PowerShell)

Abra o terminal na raiz, onde está `app.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`. A primeira inicialização cria as tabelas presentes em `database/schema.sql` e aplica algumas migrações de compatibilidade. **Não sobrescreva `database/banco.db`** caso já tenha dados. O código no ZIP inicia com `debug=True`; execute apenas localmente e consulte [Segurança](../reference/seguranca-e-limitacoes.md).

## 3. Portal Docusaurus

Em outro terminal, dentro de `website`:

```powershell
npm ci
npm run start
```

Abra o endereço indicado no terminal (normalmente `http://localhost:3000`). Para validar o site em modo de produção:

```powershell
npm run build
npm run serve
```

O portal não exige que o servidor Flask esteja ligado, pois é um site de documentação estática.

## 4. Executar testes Python

Na raiz do projeto:

```powershell
python -m unittest discover -s tests -v
```

Os testes disponíveis em `tests/test_tarefas.py` usam SQLite temporário e cobrem tarefas, isolamento entre usuários e sugestão por tempo disponível. Não constituem cobertura integral dos formulários web ou do fluxo de recuperação de senha.

:::warning Atenção ao banco local
O ZIP original contém `database/banco.db`, mas ele não deve ser redistribuído. O pacote atualizado fornecido com a documentação exclui o banco local. As rotas de redefinição consultam uma tabela que não é criada pelo schema desta versão.
:::
