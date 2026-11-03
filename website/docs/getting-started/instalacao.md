---
title: Instalação e execução local
sidebar_position: 1
description: Como preparar Python, iniciar Flask e executar o portal Docusaurus.
---

# Instalação e execução local

Este repositório reúne duas partes independentes: a aplicação Flask e o portal de documentação Docusaurus. É possível executar a aplicação sem instalar Node.js; Node é necessário somente para editar ou executar o portal.

## Requisitos

| Ferramenta | Requisito | Para quê |
|---|---|---|
| Python | 3.10 ou superior | Aplicação Flask e scripts de banco |
| pip | Incluído na instalação usual do Python | Instalar bibliotecas Python |
| Node.js | 20 ou superior | Executar Docusaurus |
| npm | Incluído com Node.js | Instalar pacotes do portal |

## 1. Executar a aplicação Flask no Windows

Abra o VS Code na pasta raiz do projeto, onde está `app.py`, e execute no PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000). O comando `python app.py` chama `inicializar_banco()` antes de iniciar o servidor e cria o banco quando necessário.

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

## 2. Banco de dados

O aplicativo cria ou atualiza o schema em `database/banco.db` quando é iniciado pela entrada `app.py`. A estrutura de tabelas está documentada em [Banco de dados](../architecture/banco-de-dados.md).

:::warning Faça backup antes de migrar
Se você está atualizando uma instalação antiga, copie `database/banco.db` para um local seguro antes de executar migrações. Não apague o banco original para resolver um erro sem antes verificar se ele contém dados que precisam ser preservados.
:::

Se o banco antigo tiver uma restrição `UNIQUE` isolada em `usuarios.curso_id` — que impede vários usuários de compartilhar um curso — e a migração ainda não tiver sido feita, execute uma vez:

```powershell
python database\corrigir_banco.py
```

O script informa quando nenhuma alteração é necessária. Não o execute repetidamente como parte do uso normal.

## 3. Executar o Docusaurus

Em outro terminal, a partir da raiz do projeto:

```powershell
cd website
npm install
npm run start
```

O portal abrirá em [http://localhost:3000](http://localhost:3000). Se o navegador não abrir automaticamente, acesse esse endereço manualmente.

Para validar a versão de produção estática:

```powershell
npm run build
npm run serve
```

O comando `build` gera os arquivos estáticos na pasta `website/build/`.

## Observações

- O banco `database/banco.db` é local e fica fora do controle de versão. O arquivo não deve ser compartilhado com a documentação.
- O diretório `.venv/`, `node_modules/`, caches Python e a pasta `website/build/` são gerados localmente.
- Se a instalação do Docusaurus falhar, confirme `node --version` (20+) e `npm --version`, e tente novamente com acesso à rede habilitado.
