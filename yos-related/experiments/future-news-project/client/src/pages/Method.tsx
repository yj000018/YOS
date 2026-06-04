// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Method Page
// Editorial philosophy and how Future News works
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { ROUTES } from '@/lib/content';

const METHOD_CONTENT = {
  en: {
    title: 'The Method',
    subtitle: 'How Future News works',
    sections: [
      {
        heading: 'The Premise',
        body: "Future News is a newspaper published one year ahead of its time. Every article, every headline, every analysis is written as if it were April 4, 2027 — grounded in the real trajectories of today's world, extrapolated with rigor and without alarm.\n\nThis is not science fiction. It is structured foresight — the practice of taking the most credible signals of change and following them forward to their plausible near-term consequences. The goal is not prediction but preparation: to make the future legible before it arrives.",
      },
      {
        heading: 'The Four Routes',
        body: "Future News organizes its coverage around four transformation routes — the domains where change is most consequential and most interconnected. Each route is not a topic but a lens: a way of reading the world that reveals patterns invisible to single-domain analysis.\n\nThe routes are not parallel tracks. They intersect, amplify, and sometimes contradict each other. The most important stories — the Confluences — live at these intersections.",
      },
      {
        heading: 'The Horizon System',
        body: "Each story is tagged with a temporal horizon: Near Term (1-2 years), Medium Term (3-5 years), or Long Term (5-10 years). This is not a measure of certainty but of distance. Near-term stories are grounded in current data and announced initiatives. Long-term stories are grounded in structural forces and technological trajectories.\n\nThe horizon system helps readers calibrate their attention and planning. Not all futures arrive at the same speed.",
      },
      {
        heading: 'What Future News Is Not',
        body: "Future News is not a prediction machine. It does not claim to know what will happen. It claims to know what is already in motion — and to follow those motions to their logical near-term conclusions.\n\nFuture News is not optimistic propaganda. The stories in this edition are grounded in real data, real policy experiments, and real technological developments. Where the data is ambiguous, the analysis says so. Where the future is contested, the analysis presents the contest.\n\nFuture News is not a technology publication. Technology is a means, not an end. The subject of Future News is the human condition — how it is changing, how it might change, and what choices remain open.",
      },
    ],
  },
  fr: {
    title: 'La Méthode',
    subtitle: 'Comment fonctionne Future News',
    sections: [
      {
        heading: 'La Prémisse',
        body: "Future News est un journal publié un an en avance sur son temps. Chaque article, chaque titre, chaque analyse est rédigé comme si nous étions le 4 avril 2027 — ancré dans les trajectoires réelles du monde d'aujourd'hui, extrapolé avec rigueur et sans alarme.\n\nCe n'est pas de la science-fiction. C'est de la prospective structurée — la pratique de prendre les signaux de changement les plus crédibles et de les suivre jusqu'à leurs conséquences plausibles à court terme. L'objectif n'est pas la prédiction mais la préparation : rendre le futur lisible avant qu'il n'arrive.",
      },
      {
        heading: 'Les Quatre Routes',
        body: "Future News organise sa couverture autour de quatre routes de transformation — les domaines où le changement est le plus conséquent et le plus interconnecté. Chaque route n'est pas un sujet mais une lentille : une façon de lire le monde qui révèle des patterns invisibles à l'analyse mono-domaine.\n\nLes routes ne sont pas des voies parallèles. Elles se croisent, s'amplifient et se contredisent parfois. Les histoires les plus importantes — les Confluences — vivent à ces intersections.",
      },
      {
        heading: 'Le Système d\'Horizon',
        body: "Chaque article est étiqueté avec un horizon temporel : Court terme (1-2 ans), Moyen terme (3-5 ans) ou Long terme (5-10 ans). Ce n'est pas une mesure de certitude mais de distance. Les articles à court terme sont ancrés dans des données actuelles et des initiatives annoncées. Les articles à long terme sont ancrés dans des forces structurelles et des trajectoires technologiques.\n\nLe système d'horizon aide les lecteurs à calibrer leur attention et leur planification. Tous les futurs n'arrivent pas à la même vitesse.",
      },
      {
        heading: 'Ce que Future News n\'est pas',
        body: "Future News n'est pas une machine à prédictions. Elle ne prétend pas savoir ce qui va se passer. Elle prétend savoir ce qui est déjà en mouvement — et suivre ces mouvements jusqu'à leurs conclusions logiques à court terme.\n\nFuture News n'est pas de la propagande optimiste. Les histoires de cette édition sont ancrées dans des données réelles, des expériences politiques réelles et des développements technologiques réels.\n\nFuture News n'est pas une publication technologique. La technologie est un moyen, pas une fin. Le sujet de Future News est la condition humaine — comment elle change, comment elle pourrait changer, et quels choix restent ouverts.",
      },
    ],
  },
  it: {
    title: 'Il Metodo',
    subtitle: 'Come funziona Future News',
    sections: [
      {
        heading: 'La Premessa',
        body: "Future News è un giornale pubblicato un anno in anticipo sui tempi. Ogni articolo, ogni titolo, ogni analisi è scritto come se fosse il 4 aprile 2027 — radicato nelle traiettorie reali del mondo di oggi, estrapolato con rigore e senza allarme.\n\nQuesto non è fantascienza. È previsione strutturata — la pratica di prendere i segnali di cambiamento più credibili e seguirli fino alle loro plausibili conseguenze a breve termine. L'obiettivo non è la previsione ma la preparazione: rendere il futuro leggibile prima che arrivi.",
      },
      {
        heading: 'Le Quattro Rotte',
        body: "Future News organizza la sua copertura attorno a quattro rotte di trasformazione — i domini dove il cambiamento è più conseguente e più interconnesso. Ogni rotta non è un argomento ma una lente: un modo di leggere il mondo che rivela pattern invisibili all'analisi mono-dominio.\n\nLe rotte non sono binari paralleli. Si intersecano, si amplificano e a volte si contraddicono. Le storie più importanti — le Confluenze — vivono a queste intersezioni.",
      },
      {
        heading: 'Il Sistema degli Orizzonti',
        body: "Ogni storia è etichettata con un orizzonte temporale: Breve termine (1-2 anni), Medio termine (3-5 anni) o Lungo termine (5-10 anni). Questa non è una misura di certezza ma di distanza. Le storie a breve termine sono radicate in dati attuali e iniziative annunciate. Le storie a lungo termine sono radicate in forze strutturali e traiettorie tecnologiche.",
      },
      {
        heading: 'Cosa Future News non è',
        body: "Future News non è una macchina per previsioni. Non pretende di sapere cosa accadrà. Pretende di sapere cosa è già in movimento — e di seguire questi movimenti fino alle loro conclusioni logiche a breve termine.\n\nFuture News non è propaganda ottimista. Le storie in questa edizione sono radicate in dati reali, esperimenti politici reali e sviluppi tecnologici reali.\n\nFuture News non è una pubblicazione tecnologica. La tecnologia è un mezzo, non un fine. Il soggetto di Future News è la condizione umana — come sta cambiando, come potrebbe cambiare, e quali scelte rimangono aperte.",
      },
    ],
  },
};

export default function Method() {
  const { lang } = useLang();
  const content = METHOD_CONTENT[lang];

  return (
    <div className="animate-fade-in-up">
      <div className="mb-4">
        <Link href="/"><span style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-muted-text)', cursor: 'pointer' }}>
          ← {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
        </span></Link>
      </div>

      <div className="thick-rule mb-6" />

      <div className="grid" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>
        <div style={{ paddingRight: '3rem', borderRight: '1px solid var(--color-rule)' }}>
          <p className="byline mb-2" style={{ color: 'var(--color-crimson)', letterSpacing: '0.15em' }}>
            {lang === 'en' ? 'EDITORIAL PHILOSOPHY' : lang === 'fr' ? 'PHILOSOPHIE ÉDITORIALE' : 'FILOSOFIA EDITORIALE'}
          </p>
          <h1 className="headline-xl mb-1">{content.title}</h1>
          <p style={{ fontFamily: 'Playfair Display, Georgia, serif', fontStyle: 'italic', fontSize: '1rem', color: 'var(--color-muted-text)', marginBottom: '2rem' }}>
            {content.subtitle}
          </p>

          {content.sections.map((section, i) => (
            <div key={i} className="mb-6">
              {i > 0 && <div className="thin-rule mb-4" />}
              <h2 className="headline-md mb-3">{section.heading}</h2>
              {section.body.split('\n\n').map((p, j) => (
                <p key={j} className="lead-text" style={{ marginBottom: '0.875rem' }}>{p}</p>
              ))}
            </div>
          ))}
        </div>

        {/* Sidebar: routes reference */}
        <div style={{ paddingLeft: '2rem' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? 'The Four Routes' : lang === 'fr' ? 'Les Quatre Routes' : 'Le Quattro Rotte'}
            </span>
          </div>
          {ROUTES.map((r, i) => (
            <div key={r.id}>
              {i > 0 && <div className="thin-rule my-3" />}
              <Link href={`/route/${r.id}`}>
                <div className="cursor-pointer" style={{ borderLeft: `3px solid ${r.colorHex}`, paddingLeft: '0.75rem' }}>
                  <div className="flex items-center gap-2 mb-1">
                    <span style={{ color: r.colorHex, fontSize: '0.65rem' }}>{r.symbol}</span>
                    <span className="byline" style={{ color: r.colorHex }}>{r[`name_${lang}` as keyof typeof r] as string}</span>
                  </div>
                  <p style={{ fontFamily: 'Source Serif 4, Georgia, serif', fontSize: '0.8125rem', lineHeight: 1.5, color: 'var(--color-ink-light)' }}>
                    {r[`desc_${lang}` as keyof typeof r] as string}
                  </p>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
