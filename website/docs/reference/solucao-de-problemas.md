---
title: Solução de problemas
sidebar_position: 3
description: Diagnóstico das falhas comuns ao executar a aplicação e o portal de documentação.
---

# Solução de problemas

## `ModuleNotFoundError: No module named 'flask'`

Ative o ambiente virtual na raiz e instale as dependências:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Confirme que o Python usado é o do ambiente virtual com `python --version` e `where python`.

## O navegador não consegue abrir `127.0.0.1:5000`

- Confirme se `python app.py` continua em execução.
- Leia a mensagem no terminal para descobrir erros de inicialização.
- Se a porta 5000 já estiver ocupada, pare a aplicação que a usa antes de iniciar novamente.

## A conta não consegue entrar

- Confira se o e-mail está correto.
- A senha diferencia maiúsculas e minúsculas.
- Contas anteriores à implementação de senha podem ter `senha_hash` vazio; execute `python scripts\definir_senha_usuario.py` localmente para definir uma senha.
- Se a mensagem for genérica, o e-mail pode não existir ou a senha pode estar incorreta.

## O banco apresenta erro de schema ou não permite compartilhar cursos

Antes de executar qualquer migração, faça cópia de `database/banco.db`. A migração `database/corrigir_banco.py` só é necessária quando a tabela antiga `usuarios` tem uma restrição `UNIQUE` isolada em `curso_id`. Para outros erros, confira `database/schema.sql` e a mensagem completa no terminal; não remova tabelas sem entender os dados que serão perdidos.

## `npm install` falha no Docusaurus

- Confirme Node.js 20 ou superior: `node --version`.
- Confirme o npm: `npm --version`.
- Verifique a conexão com a internet e tente novamente.
- Execute os comandos a partir da pasta `website/`, onde fica `package.json`.

## O site de documentação não abre os diagramas `.puml`

Os arquivos `.puml` são fontes, não imagens renderizadas. Baixe o arquivo e use uma extensão PlantUML ou ferramenta compatível. Os diagramas Mermaid incluídos nas páginas são renderizados no próprio portal.

## O link ou documento gera erro durante `npm run build`

O Docusaurus está configurado para falhar em links internos quebrados. Confira o destino, o nome do arquivo `.md` e o `id` da página em `website/sidebars.js`.
