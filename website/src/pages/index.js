import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

function BrandMark() {
  return (
    <svg className={styles.brandMark} viewBox="0 0 48 48" aria-hidden="true">
      <rect width="48" height="48" rx="15" fill="currentColor" />
      <path d="M12 27.5c0-6.1 4.4-10.5 10-10.5 4.8 0 7.2 3.5 7.2 7.4v10" fill="none" stroke="#fff" strokeWidth="3.4" strokeLinecap="round" />
      <path d="M22 31.2c0-4.8 3.5-8.2 8.2-8.2 3.4 0 5.8 2.1 5.8 5.3 0 3.5-2.7 6.1-6.5 6.1" fill="none" stroke="#9DE8D1" strokeWidth="3.4" strokeLinecap="round" />
      <circle cx="12" cy="27.5" r="3.2" fill="#9DE8D1" />
    </svg>
  );
}

const areas = [
  { number: '01', title: 'Produto e escopo', text: 'Entenda o que a versão atual faz, como o usuário percorre as etapas e quais ideias continuam no roadmap.', to: '/docs/product/visao-geral', label: 'Conhecer o produto' },
  { number: '02', title: 'Primeiros passos', text: 'Prepare Python, instale as dependências e execute o aplicativo localmente no VS Code.', to: '/docs/getting-started/instalacao', label: 'Ver instalação' },
  { number: '03', title: 'Arquitetura técnica', text: 'Explore modelos, repositórios, rotas Flask e o schema que sustenta os dados.', to: '/docs/architecture/arquitetura', label: 'Explorar arquitetura' },
  { number: '04', title: 'Diagramas UML', text: 'Consulte os diagramas de classes e sequência e baixe seus arquivos PlantUML originais.', to: '/docs/reference/uml', label: 'Abrir diagramas' },
];

function PreviewPanel() {
  return (
    <div className={styles.previewWrap} aria-label="Ilustração de uma tela do MyFlow">
      <div className={styles.orbitOne} />
      <div className={styles.orbitTwo} />
      <div className={styles.previewCard}>
        <div className={styles.previewTop}>
          <div className={styles.previewBrand}><span className={styles.previewBrandIcon}><BrandMark /></span><span>myflow</span></div>
          <span className={styles.previewAvatar}>N</span>
        </div>
        <div className={styles.previewHeading}>Seu fluxo de aprendizagem</div>
        <div className={styles.previewSubheading}>Graduação · Negócios Digitais</div>
        <div className={styles.progressBlock}>
          <div className={styles.progressMeta}><span>Progresso do curso</span><strong>68%</strong></div>
          <div className={styles.progressTrack}><span /></div>
        </div>
        <div className={styles.previewSectionLabel}>Suas disciplinas</div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconDone}`}>✓</span>
          <span className={styles.taskCopy}><strong>Fundamentos de Marketing</strong><small>Concluída</small></span>
          <span className={styles.taskStatus}>Feito</span>
        </div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconActive}`}>↗</span>
          <span className={styles.taskCopy}><strong>Programação Orientada a Objetos</strong><small>Em andamento</small></span>
          <span className={styles.taskDot} />
        </div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconPending}`}>○</span>
          <span className={styles.taskCopy}><strong>Experiência do Usuário</strong><small>Pendente</small></span>
          <span className={styles.taskDot} />
        </div>
        <div className={styles.previewFoot}><span className={styles.previewFootDot} /> Uma etapa de cada vez</div>
      </div>
      <div className={styles.floatNote}><span className={styles.floatNoteIcon}>↗</span><span><strong>Seu progresso</strong><small>Individual e consistente</small></span></div>
    </div>
  );
}

function Home() {
  return (
    <Layout title="Documentação" description="Guia técnico e funcional do projeto MyFlow">
      <main className={styles.home}>
        <section className={styles.hero}>
          <div className={styles.heroInner}>
            <div className={styles.heroCopy}>
              <div className={styles.eyebrow}><span className={styles.eyebrowDot} /> DOCUMENTAÇÃO DO PROJETO</div>
              <h1>Organize a jornada.<br /><span>Entenda o sistema.</span></h1>
              <p className={styles.heroLead}>Um guia claro para conhecer, executar e evoluir o MyFlow — da primeira rota Flask ao modelo de dados.</p>
              <div className={styles.heroActions}>
                <Link className={styles.primaryButton} to="/docs/intro">Explorar documentação <span aria-hidden="true">→</span></Link>
                <Link className={styles.textButton} to="/docs/getting-started/instalacao">Começar pela instalação</Link>
              </div>
              <div className={styles.heroMeta}>
                <span><i className={styles.metaPython}>Py</i> Python + Flask</span>
                <span><i className={styles.metaDb} /> SQLite</span>
                <span><i className={styles.metaDocs}>D</i> Docusaurus</span>
              </div>
            </div>
            <div className={styles.heroVisual}><PreviewPanel /></div>
          </div>
          <div className={styles.heroRule}><span /><span /><span /></div>
        </section>

        <section className={styles.valueStrip} aria-label="Visão geral do portal">
          <div className={styles.valueItem}><strong>Visão do produto</strong><span>Fluxos reais e escopo atual</span></div>
          <div className={styles.valueItem}><strong>Referência técnica</strong><span>Modelos, repositórios e banco</span></div>
          <div className={styles.valueItem}><strong>Documentação visual</strong><span>Diagramas e guias navegáveis</span></div>
        </section>

        <section className={styles.section}>
          <div className={styles.sectionIntro}>
            <div><span className={styles.sectionEyebrow}>NAVEGUE POR TEMA</span><h2>Da visão geral ao detalhe técnico</h2></div>
            <p>Encontre o caminho certo para seu próximo passo no projeto, com conteúdo direto e organizado por responsabilidade.</p>
          </div>
          <div className={styles.areaGrid}>
            {areas.map((area) => (
              <article className={styles.areaCard} key={area.number}>
                <div className={styles.cardTop}><span className={styles.cardNumber}>{area.number}</span><span className={styles.cardArrow} aria-hidden="true">↗</span></div>
                <h3>{area.title}</h3>
                <p>{area.text}</p>
                <Link className={styles.cardLink} to={area.to}>{area.label} <span aria-hidden="true">→</span></Link>
              </article>
            ))}
          </div>
        </section>

        <section className={styles.architectureBand}>
          <div className={styles.architectureContent}>
            <span className={styles.sectionEyebrow}>UMA ESTRUTURA SIMPLES</span>
            <h2>Camadas com responsabilidades claras.</h2>
            <p>O Flask coordena os fluxos, os modelos validam os dados, os repositórios cuidam da persistência e o SQLite mantém os registros.</p>
            <Link className={styles.bandLink} to="/docs/architecture/arquitetura">Ver arquitetura completa <span aria-hidden="true">→</span></Link>
          </div>
          <div className={styles.layerStack} aria-label="Camadas principais do sistema">
            <div className={styles.layerRow}><span className={styles.layerGlyph}>01</span><span><strong>Interface</strong><small>Templates Jinja + CSS</small></span><em>View</em></div>
            <div className={styles.layerConnector} />
            <div className={styles.layerRow}><span className={styles.layerGlyph}>02</span><span><strong>Aplicação e modelos</strong><small>Rotas Flask + regras de domínio</small></span><em>Logic</em></div>
            <div className={styles.layerConnector} />
            <div className={styles.layerRow}><span className={styles.layerGlyph}>03</span><span><strong>Persistência</strong><small>Repositories + SQLite</small></span><em>Data</em></div>
          </div>
        </section>

        <section className={styles.lastCall}>
          <div className={styles.lastCallMark}><BrandMark /></div>
          <div><h2>Pronto para começar?</h2><p>Configure o ambiente e rode o projeto localmente.</p></div>
          <Link className={styles.primaryButton} to="/docs/getting-started/instalacao">Ver guia de instalação <span aria-hidden="true">→</span></Link>
        </section>
      </main>
    </Layout>
  );
}

export default Home;
