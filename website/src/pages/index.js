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
  { number: '01', title: 'Produto e jornada', text: 'Conheça o MyFlow, a organização de cursos e o progresso individual de cada usuário.', to: '/docs/product/visao-geral', label: 'Conhecer o produto' },
  { number: '02', title: 'Dashboard e tarefas', text: 'Explore os indicadores, o controle de atividades e a gestão de prioridades.', to: '/docs/guides/tarefas', label: 'Ver tarefas' },
  { number: '03', title: 'Próxima ação', text: 'Entenda como o sistema recomenda uma tarefa conforme o tempo disponível.', to: '/docs/guides/sugestor', label: 'Explorar o algoritmo' },
  { number: '04', title: 'Contas e permissões', text: 'Documentação de perfil, login, proprietários e redefinição de senha.', to: '/docs/guides/administracao', label: 'Ver gestão de contas' },
  { number: '05', title: 'Arquitetura técnica', text: 'Modelos, repositórios, rotas Flask e estrutura do banco SQLite.', to: '/docs/architecture/arquitetura', label: 'Explorar arquitetura' },
  { number: '06', title: 'UML e execução', text: 'Diagramas atualizados, instalação e diretrizes de manutenção do projeto.', to: '/docs/reference/uml', label: 'Abrir diagramas' },
];

function PreviewPanel() {
  return (
    <div className={styles.previewWrap} aria-label="Prévia ilustrativa de um painel do MyFlow; dados fictícios">
      <div className={styles.orbitOne} />
      <div className={styles.orbitTwo} />
      <div className={styles.previewCard}>
        <div className={styles.previewTop}>
          <div className={styles.previewBrand}><span className={styles.previewBrandIcon}><BrandMark /></span><span>myflow</span></div>
          <span className={styles.previewAvatar}>N</span>
        </div>
        <div className={styles.previewHeading}>Seu painel de estudos</div>
        <div className={styles.previewSubheading}>Graduação · Negócios Digitais</div>
        <div className={styles.progressBlock}>
          <div className={styles.progressMeta}><span>Progresso do curso</span><strong>68%</strong></div>
          <div className={styles.progressTrack}><span /></div>
        </div>
        <div className={styles.previewSectionLabel}>PRÓXIMAS ATIVIDADES</div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconDone}`}>✓</span>
          <span className={styles.taskCopy}><strong>Revisar Marketing</strong><small>Tarefa concluída</small></span>
          <span className={styles.taskStatus}>Feito</span>
        </div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconActive}`}>↗</span>
          <span className={styles.taskCopy}><strong>Entregar atividade de POO</strong><small>Alta prioridade</small></span>
          <span className={styles.taskDot} />
        </div>
        <div className={styles.previewTask}>
          <span className={`${styles.taskIcon} ${styles.taskIconPending}`}>○</span>
          <span className={styles.taskCopy}><strong>Ler material de UX</strong><small>Estimativa: 20 min</small></span>
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
              <p className={styles.heroLead}>Documentação funcional e técnica do MyFlow: produtividade, jornada de estudos, gestão de contas, arquitetura e UML em um só lugar.</p>
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
          <div className={styles.valueItem}><strong>Visão do produto</strong><span>Jornada, tarefas e agenda</span></div>
          <div className={styles.valueItem}><strong>Referência técnica</strong><span>Contas, rotas e dados</span></div>
          <div className={styles.valueItem}><strong>Documentação visual</strong><span>UML e orientações de uso</span></div>
        </section>

        <section className={styles.section}>
          <div className={styles.sectionIntro}>
            <div><span className={styles.sectionEyebrow}>NAVEGUE POR TEMA</span><h2>Tudo sobre a versão atual do MyFlow</h2></div>
            <p>Explore guias objetivos e referências técnicas que acompanham o código real do sistema.</p>
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
          <div><h2>Pronto para começar?</h2><p>Execute a aplicação e consulte os guias atualizados.</p></div>
          <Link className={styles.primaryButton} to="/docs/getting-started/instalacao">Ver guia de instalação <span aria-hidden="true">→</span></Link>
        </section>
      </main>
    </Layout>
  );
}

export default Home;
