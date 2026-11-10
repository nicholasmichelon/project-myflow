# MyFlow — Guia de login, perfil e administração

## 1. Atualizar sem perder o banco de dados

1. Pare o servidor Flask (`Ctrl + C`).
2. Faça uma cópia de segurança de `database/banco.db`.
3. Extraia o ZIP atualizado e copie os arquivos para a pasta do projeto. O ZIP não inclui `database/banco.db`; mantenha o seu banco local.
4. No terminal do VS Code, na raiz do projeto, execute:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe app.py
   ```

## 2. Configurar o primeiro proprietário

O primeiro proprietário é ativado uma única vez pela interface. Essa etapa exige um código de configuração para impedir que qualquer pessoa se torne proprietária apenas abrindo uma URL.

1. Se ainda não existir proprietário, o terminal exibirá um token de configuração.
2. Entre no MyFlow com a conta que será proprietária. Se ainda não houver uma conta com senha, cadastre uma nova conta pela tela inicial.
3. No menu da conta, clique em **Ativar proprietário**. Também é possível abrir `/configurar-proprietario` no navegador.
4. Informe o token mostrado no terminal.
5. Após essa configuração, a rota de primeiro acesso fica fechada; use o menu **Administração**.

O token é válido apenas durante a execução atual do aplicativo e enquanto não existir proprietário. Para definir seu próprio token antes de iniciar, configure a variável de ambiente `MYFLOW_OWNER_SETUP_TOKEN`.

## 3. Recuperação de senha

Na tela de login, o usuário pode clicar em **Esqueceu sua senha?**, informar o e-mail cadastrado e seguir o link de redefinição. Por segurança, a tela apresenta a mesma confirmação mesmo quando o e-mail não existe. O link expira em 30 minutos e só pode ser utilizado uma vez. A senha nova deve ter pelo menos oito caracteres.

- **Execução local:** sem SMTP configurado, o link de recuperação é exibido no terminal onde o Flask está rodando. Copie o endereço completo e abra-o no navegador. Esse comportamento é destinado ao desenvolvimento local.
- **Envio por e-mail com Gmail (para destinatários de qualquer provedor):** o Gmail será o remetente; os usuários podem informar endereços Gmail, Outlook, Hotmail ou outros.
  1. Na Conta Google, ative a verificação em duas etapas e crie uma senha de app em https://myaccount.google.com/apppasswords.
  2. Na raiz do projeto, copie `.env.example` para `.env`.
  3. Edite `.env` e substitua `seuemail@gmail.com` pelo seu Gmail e `COLE_AQUI_A_SENHA_DE_APP_DO_GOOGLE` pela senha de app de 16 caracteres. Não use a senha normal do Gmail.
  4. Instale as dependências e inicie o app: `python -m pip install -r requirements.txt` e `python app.py`. O aplicativo carrega `.env` automaticamente.
  5. Faça um teste enviando a recuperação para um Gmail e depois para um endereço Outlook/Hotmail. Confira também Spam/Lixo eletrônico.
  O arquivo `.env` é ignorado pelo Git e não deve ser compartilhado. O STARTTLS fica ativo na porta 587.
- O banco guarda somente o hash do token, não o token original. Uma nova solicitação invalida o link anterior da mesma conta.

## 4. Meu perfil

A opção **Meu perfil** permite alterar nome, e-mail, jornada, objetivo e tempo disponível. Para trocar e-mail ou senha, o usuário precisa informar sua senha atual. A nova senha precisa ter pelo menos oito caracteres e confirmação igual.

## 5. Administração de contas

Somente contas marcadas como proprietárias podem abrir `/admin/usuarios`; a autorização é verificada no servidor e no banco, não apenas pelo menu.

No painel, proprietários podem:

- listar usuários sem visualizar hashes ou senhas existentes;
- definir uma senha inicial/temporária para contas antigas sem senha ou redefinir a senha de uma conta comum;
- conceder ou remover o papel de proprietário, sem remover o último proprietário nem alterar o próprio papel pela tela;
- excluir contas comuns. Excluir uma conta remove o e-mail e o hash da senha e elimina o progresso individual associado. A conta ativa e contas ainda proprietárias são protegidas contra exclusão direta.

Senhas nunca são mostradas no painel. Ao definir uma senha temporária, o proprietário deve entregá-la ao titular por um canal confiável e orientá-lo a alterá-la em **Meu perfil**.

## 6. Observações de segurança

- O arquivo `database/banco.db` contém dados locais; faça backup antes de qualquer migração ou exclusão.
- Se `MYFLOW_SECRET_KEY` não estiver definida, o app gera uma chave aleatória para a execução atual; ao reiniciar, as sessões são invalidadas e será necessário entrar novamente. Para manter sessões entre reinicializações, defina essa variável no ambiente.
- Este projeto é um protótipo acadêmico local. Antes de publicar na internet, configure HTTPS, segredos fortes e uma estratégia segura de recuperação de senha e limitação de tentativas de login.
