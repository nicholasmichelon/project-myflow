---
title: Configuração e ambiente
sidebar_position: 1
description: Variáveis de ambiente e execução segura no desenvolvimento.
---

# Configuração e ambiente

O `app.py` usa `python-dotenv` e chama `load_dotenv()` na inicialização. Assim, configurações podem vir do ambiente ou de um `.env` criado manualmente na raiz do projeto. **O anexo não inclui `.env.example`**, apesar da menção no guia de administração.

## Variáveis reconhecidas

| Variável | Função | Comportamento sem configuração |
|---|---|---|
| `MYFLOW_SECRET_KEY` | Assina sessões Flask | Chave aleatória por processo; reiniciar invalida sessões |
| `MYFLOW_OWNER_SETUP_TOKEN` | Token de ativação do primeiro proprietário | Token aleatório exibido no terminal se ainda não houver proprietário |
| `MYFLOW_SMTP_HOST` | Servidor SMTP de recuperação | Link de redefinição é mostrado no terminal |
| `MYFLOW_SMTP_PORT` | Porta do servidor SMTP | `587` |
| `MYFLOW_SMTP_USER` | Usuário SMTP | Autenticação somente se usuário/senha informados |
| `MYFLOW_SMTP_PASSWORD` | Senha SMTP | Não definida |
| `MYFLOW_SMTP_FROM` | Remetente do e-mail | SMTP user ou fallback local |
| `MYFLOW_SMTP_STARTTLS` | Ativa STARTTLS quando `1` | `1` |

Exemplo **sem segredos reais** para criar manualmente o arquivo `.env`:

```dotenv
MYFLOW_SECRET_KEY=SUBSTITUA_POR_VALOR_SEGURO
MYFLOW_OWNER_SETUP_TOKEN=SUBSTITUA_POR_TOKEN_ALEATORIO
# Configure somente ao testar e-mail:
# MYFLOW_SMTP_HOST=smtp.exemplo.com
# MYFLOW_SMTP_PORT=587
# MYFLOW_SMTP_USER=usuario@example.com
# MYFLOW_SMTP_PASSWORD=SENHA_ESPECIFICA_DO_SERVICO
# MYFLOW_SMTP_FROM=usuario@example.com
# MYFLOW_SMTP_STARTTLS=1
```

**Não publique `.env` e nunca copie valores reais para a documentação.**

## Modo de depuração

O arquivo **atual** termina com `app.run(debug=True, use_reloader=False)`. Portanto, o modo debug está ligado no código recebido. A variável `MYFLOW_DEBUG` mencionada na documentação anterior **não é lida** pelo `app.py` atual; defini-la não desativa a depuração. Antes de implantar a aplicação, corrija esse ponto no código e faça revisão de segurança.

## Dependências

`requirements.txt` lista Flask, Werkzeug e `python-dotenv`; `website/package.json` controla as dependências Node do Docusaurus, incluindo o tema Mermaid.
