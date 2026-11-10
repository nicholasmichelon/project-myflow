
const config = {
  title: 'MyFlow · Documentação',
  tagline: 'Arquitetura, fluxos e guia de execução do projeto',
  favicon: 'img/myflow-mark.svg',
  url: 'https://example.com',
  baseUrl: '/',
  organizationName: 'myflow',
  projectName: 'myflow-documentation',

  // Links internos quebrados devem gerar erro.
  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'docs',
          showLastUpdateTime: false,
        },
        blog: false,
        pages: {},
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  // Tema necessário para renderizar diagramas Mermaid.
  themes: ['@docusaurus/theme-mermaid'],

  // Configurações globais do Markdown.
  markdown: {
    mermaid: true,
    hooks: {
      // Mantém o comportamento anterior:
      // links Markdown quebrados geram erro.
      onBrokenMarkdownLinks: 'throw',
    },
  },

  themeConfig: {
    image: 'img/myflow-social-card.svg',

    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    navbar: {
      title: 'MyFlow',
      logo: {
        alt: 'Símbolo do MyFlow',
        src: 'img/myflow-mark.svg',
      },
      hideOnScroll: false,
      items: [
        {
          to: '/docs/intro',
          label: 'Documentação',
          position: 'left',
        },
        {
          to: '/docs/guides/tarefas',
          label: 'Tarefas',
          position: 'left',
        },
        {
          to: '/docs/architecture/arquitetura',
          label: 'Arquitetura',
          position: 'left',
        },
      ],
    },

    footer: {
      style: 'light',
      links: [
        {
          title: 'Comece aqui',
          items: [
            {
              label: 'Visão geral',
              to: '/docs/product/visao-geral',
            },
            {
              label: 'Instalação',
              to: '/docs/getting-started/instalacao',
            },
          ],
        },
        {
          title: 'Projeto',
          items: [
            {
              label: 'Arquitetura',
              to: '/docs/architecture/arquitetura',
            },
            {
              label: 'Modelos',
              to: '/docs/architecture/modelos',
            },
            {
              label: 'Diagramas UML',
              to: '/docs/reference/uml',
            },
            {
              label: 'Tarefas e agenda',
              to: '/docs/guides/tarefas',
            },
          ],
        },
      ],
      copyright: 'MyFlow · Documentação técnica e funcional',
    },

    prism: {
      additionalLanguages: [
        'bash',
        'powershell',
        'sql',
        'python',
        'json',
      ],
    },
  },
};

module.exports = config;