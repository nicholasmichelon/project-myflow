# MyFlow Documentation (Docusaurus)

Portal em português para documentar o protótipo acadêmico MyFlow. O conteúdo cobre produto, instalação, configuração, fluxos da aplicação, modelos, repositórios, SQLite, rotas Flask, segurança, solução de problemas e UML.

## Requisitos

- Node.js 20 ou superior
- npm

## Desenvolvimento local

```bash
npm install
npm run start
```

O Docusaurus abre `http://localhost:3000` e atualiza a página ao salvar arquivos em `docs/`, `src/` ou na configuração.

## Build

```bash
npm run build
npm run serve
```

O resultado estático fica em `build/`. Configure `url` e `baseUrl` em `docusaurus.config.js` quando souber o endereço real de publicação; `https://example.com` é apenas um valor provisório de configuração.

## Organização

- `docs/`: documentação funcional e técnica em Markdown/MDX.
- `src/pages/index.js`: página inicial customizada.
- `src/css/custom.css`: tokens visuais e personalização do tema.
- `src/pages/index.module.css`: layout da página inicial, com breakpoints responsivos.
- `static/img/`: marca e ilustração vetorial para metadados.
- `static/uml/`: fontes PlantUML disponíveis para download.
