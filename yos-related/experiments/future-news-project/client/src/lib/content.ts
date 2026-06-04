// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Content Data
// Generated: April 4, 2026 | Published date: April 4, 2027
// 20 headlines × 3 languages + edition + confluences + futura
// ═══════════════════════════════════════════════════════════════

export type Lang = 'en' | 'fr' | 'it';
export type Horizon = 'Near' | 'Mid' | 'Far';

export interface Headline {
  id: string;
  routeId: RouteId;
  headline_en: string; lead_en: string; milestone_en: string;
  headline_fr: string; lead_fr: string; milestone_fr: string;
  headline_it: string; lead_it: string; milestone_it: string;
  horizon: Horizon;
}

export type RouteId = 'work' | 'ai' | 'robotics' | 'energy';

export interface Route {
  id: RouteId;
  symbol: string;
  color: string;
  colorHex: string;
  name_en: string; name_fr: string; name_it: string;
  desc_en: string; desc_fr: string; desc_it: string;
}

export const ROUTES: Route[] = [
  {
    id: 'work',
    symbol: '◆',
    color: 'route-work',
    colorHex: '#2D5A8E',
    name_en: 'Work & Human Purpose',
    name_fr: 'Travail & Sens Humain',
    name_it: 'Lavoro & Scopo Umano',
    desc_en: 'The transformation of work, employment, and human purpose as automation reshapes the economy.',
    desc_fr: "La transformation du travail, de l'emploi et du sens humain à mesure que l'automatisation remodèle l'économie.",
    desc_it: "La trasformazione del lavoro, dell'occupazione e dello scopo umano mentre l'automazione ridisegna l'economia.",
  },
  {
    id: 'ai',
    symbol: '●',
    color: 'route-ai',
    colorHex: '#6B3FA0',
    name_en: 'AI & Cognitive Expansion',
    name_fr: 'IA & Expansion Cognitive',
    name_it: 'IA & Espansione Cognitiva',
    desc_en: 'Artificial intelligence integration into daily life, cognitive augmentation, and human-machine collaboration.',
    desc_fr: "L'intégration de l'IA dans la vie quotidienne, l'augmentation cognitive et la collaboration homme-machine.",
    desc_it: "L'integrazione dell'IA nella vita quotidiana, l'aumento cognitivo e la collaborazione uomo-macchina.",
  },
  {
    id: 'robotics',
    symbol: '▲',
    color: 'route-robotics',
    colorHex: '#2D6A4F',
    name_en: 'Robotics & Physical World',
    name_fr: 'Robotique & Monde Physique',
    name_it: 'Robotica & Mondo Fisico',
    desc_en: 'Physical automation, humanoid robots entering homes and workplaces, autonomous systems in cities and agriculture.',
    desc_fr: "L'automatisation physique, les robots humanoïdes dans les foyers et les lieux de travail, les systèmes autonomes dans les villes.",
    desc_it: "L'automazione fisica, i robot umanoidi nelle case e nei luoghi di lavoro, i sistemi autonomi nelle città e nell'agricoltura.",
  },
  {
    id: 'energy',
    symbol: '■',
    color: 'route-energy',
    colorHex: '#B5451B',
    name_en: 'Energy & Productive Abundance',
    name_fr: 'Énergie & Abondance Productive',
    name_it: 'Energia & Abbondanza Produttiva',
    desc_en: 'The energy transition reaching critical mass, renewable abundance, and new economic models based on cheap clean energy.',
    desc_fr: "La transition énergétique atteignant une masse critique, l'abondance renouvelable et de nouveaux modèles économiques.",
    desc_it: "La transizione energetica che raggiunge la massa critica, l'abbondanza rinnovabile e nuovi modelli economici.",
  },
];

export const HEADLINES: Headline[] = [
  // ── WORK ────────────────────────────────────────────────────
  {
    id: 'work-1', routeId: 'work', horizon: 'Near',
    headline_en: "Seattle's UBI Pilot Program Boosts Local Entrepreneurship by 15%",
    lead_en: "A two-year universal basic income pilot in Seattle has yielded remarkable results, with participants showing a 15% increase in new business registrations and a notable rise in creative sector employment. City officials are now considering a permanent expansion of the program.",
    milestone_en: 'UBI Milestone',
    headline_fr: "Le programme pilote de revenu universel de Seattle stimule l'entrepreneuriat local de 15 %",
    lead_fr: "Un programme pilote de revenu universel de base de deux ans à Seattle a donné des résultats remarquables, les participants affichant une augmentation de 15 % des nouvelles immatriculations d'entreprises. Les responsables municipaux envisagent désormais une expansion permanente du programme.",
    milestone_fr: 'Jalon RUB',
    headline_it: "Il programma pilota UBI di Seattle aumenta l'imprenditorialità locale del 15%",
    lead_it: "Un programma pilota di reddito di base universale di due anni a Seattle ha prodotto risultati notevoli, con i partecipanti che mostrano un aumento del 15% nelle nuove registrazioni di imprese. I funzionari della città stanno ora considerando un'espansione permanente del programma.",
    milestone_it: 'Traguardo RUB',
  },
  {
    id: 'work-2', routeId: 'work', horizon: 'Near',
    headline_en: "Germany Retrains 200,000 Workers for AI-Augmented Roles",
    lead_en: "Germany's leading industrial firms, in collaboration with national trade unions, have successfully reskilled over 200,000 employees for advanced positions in automation and AI management. This comprehensive national initiative showcases a proactive approach to workforce evolution.",
    milestone_en: 'Workforce Reskilling',
    headline_fr: "L'Allemagne recycle 200 000 travailleurs pour des rôles augmentés par l'IA",
    lead_fr: "Les principales entreprises industrielles allemandes, en collaboration avec les syndicats nationaux, ont reconverti avec succès plus de 200 000 employés pour des postes avancés dans l'automatisation et la gestion de l'IA.",
    milestone_fr: 'Reconversion Main-d\'œuvre',
    headline_it: "La Germania riqualifica 200.000 lavoratori per ruoli potenziati dall'IA",
    lead_it: "Le principali aziende industriali tedesche, in collaborazione con i sindacati nazionali, hanno riqualificato con successo oltre 200.000 dipendenti per posizioni avanzate nell'automazione e nella gestione dell'IA.",
    milestone_it: 'Riqualificazione Lavoro',
  },
  {
    id: 'work-3', routeId: 'work', horizon: 'Near',
    headline_en: "EU Report: 'Passion Economy' Contributes €1.2 Trillion, Fuels New Entrepreneurship",
    lead_en: "A new analysis from the European Commission reveals that the 'passion economy,' encompassing creators, freelancers, and service entrepreneurs, now constitutes a significant portion of the continent's GDP. The sector's expansion is attributed to accessible digital platforms and evolving worker support frameworks.",
    milestone_en: 'Creative Economy Growth',
    headline_fr: "Rapport de l'UE : l'« économie de la passion » contribue à 1 200 milliards d'euros",
    lead_fr: "Une nouvelle analyse de la Commission européenne révèle que l'« économie de la passion », englobant les créateurs, les freelances et les entrepreneurs de services, constitue désormais une part significative du PIB du continent.",
    milestone_fr: 'Économie Créative',
    headline_it: "Rapporto UE: la 'Passion Economy' contribuisce con 1,2 trilioni di euro",
    lead_it: "Una nuova analisi della Commissione Europea rivela che la 'passion economy', che comprende creatori, freelance e imprenditori di servizi, costituisce ora una parte significativa del PIL del continente.",
    milestone_it: 'Economia Creativa',
  },
  {
    id: 'work-4', routeId: 'work', horizon: 'Near',
    headline_en: "New Zealand's Four-Day Work Week Pilot Leads to Sustained Productivity Gains",
    lead_en: "Following a nationwide trial involving 50 companies, New Zealand's Ministry of Business announced that a four-day work week has consistently delivered higher employee satisfaction and maintained, or even increased, output. The positive outcomes are prompting discussions for wider public sector adoption.",
    milestone_en: 'Work Week Innovation',
    headline_fr: "La semaine de quatre jours en Nouvelle-Zélande entraîne des gains de productivité durables",
    lead_fr: "Suite à un essai national impliquant 50 entreprises, le ministère néo-zélandais a annoncé qu'une semaine de travail de quatre jours a constamment généré une plus grande satisfaction des employés.",
    milestone_fr: 'Innovation Travail',
    headline_it: "La settimana lavorativa di quattro giorni della Nuova Zelanda porta a guadagni di produttività sostenuti",
    lead_it: "A seguito di un'indagine a livello nazionale che ha coinvolto 50 aziende, il Ministero neozelandese ha annunciato che una settimana lavorativa di quattro giorni ha costantemente portato a una maggiore soddisfazione dei dipendenti.",
    milestone_it: 'Innovazione Lavoro',
  },
  {
    id: 'work-5', routeId: 'work', horizon: 'Mid',
    headline_en: "Nordic Nations Launch 'Universal Creative Income' for Artists and Innovators",
    lead_en: "Sweden, Norway, and Denmark have jointly announced a groundbreaking 'Universal Creative Income' initiative, providing stipends to artists, researchers, and social innovators. The program aims to cultivate a robust creative sector and address the societal need for human-centered work in an increasingly automated economy.",
    milestone_en: 'Creative Income Policy',
    headline_fr: "Les pays nordiques lancent un « Revenu Créatif Universel » pour artistes et innovateurs",
    lead_fr: "La Suède, la Norvège et le Danemark ont conjointement annoncé une initiative révolutionnaire de « Revenu Créatif Universel », fournissant des allocations aux artistes, chercheurs et innovateurs sociaux.",
    milestone_fr: 'Revenu Créatif',
    headline_it: "I Paesi nordici lanciano il 'Reddito Creativo Universale' per artisti e innovatori",
    lead_it: "Svezia, Norvegia e Danimarca hanno annunciato congiuntamente un'innovativa iniziativa di 'Reddito Creativo Universale', fornendo stipendi ad artisti, ricercatori e innovatori sociali.",
    milestone_it: 'Reddito Creativo',
  },
  // ── AI ──────────────────────────────────────────────────────
  {
    id: 'ai-1', routeId: 'ai', horizon: 'Near',
    headline_en: "AI Accelerates Global Research: Drug Discovery Times Halved by Collaborative Intelligence",
    lead_en: "A landmark study published in Nature reveals that AI-assisted drug discovery platforms have reduced average development timelines from 12 years to under 6, with three new treatments for rare diseases approved in Q1 2027 alone. The breakthrough represents a fundamental shift in pharmaceutical research methodology.",
    milestone_en: 'Research Acceleration',
    headline_fr: "L'IA accélère la recherche mondiale : les délais de découverte de médicaments divisés par deux",
    lead_fr: "Une étude publiée dans Nature révèle que les plateformes de découverte de médicaments assistées par IA ont réduit les délais de développement moyens de 12 ans à moins de 6, avec trois nouveaux traitements approuvés au premier trimestre 2027.",
    milestone_fr: 'Accélération Recherche',
    headline_it: "L'IA accelera la ricerca globale: i tempi di scoperta dei farmaci dimezzati dall'intelligenza collaborativa",
    lead_it: "Uno studio pubblicato su Nature rivela che le piattaforme di scoperta di farmaci assistite dall'IA hanno ridotto i tempi medi di sviluppo da 12 anni a meno di 6, con tre nuovi trattamenti approvati solo nel primo trimestre del 2027.",
    milestone_it: 'Accelerazione Ricerca',
  },
  {
    id: 'ai-2', routeId: 'ai', horizon: 'Near',
    headline_en: "Nexus Capital Reports 15% Productivity Boost with Integrated Cognitive Assistants",
    lead_en: "Global finance firm Nexus Capital has reported a 15% increase in analyst productivity following the firm-wide deployment of integrated cognitive assistants. The AI tools handle data synthesis and preliminary report drafting, freeing analysts to focus on strategic interpretation and client relationships.",
    milestone_en: 'Productivity Milestone',
    headline_fr: "Nexus Capital signale un gain de productivité de 15 % grâce aux assistants cognitifs intégrés",
    lead_fr: "La société financière mondiale Nexus Capital a signalé une augmentation de 15 % de la productivité des analystes suite au déploiement à l'échelle de l'entreprise d'assistants cognitifs intégrés.",
    milestone_fr: 'Gain Productivité',
    headline_it: "Nexus Capital registra un aumento del 15% della produttività con assistenti cognitivi integrati",
    lead_it: "La società finanziaria globale Nexus Capital ha riportato un aumento del 15% della produttività degli analisti a seguito del dispiegamento aziendale di assistenti cognitivi integrati.",
    milestone_it: 'Traguardo Produttività',
  },
  {
    id: 'ai-3', routeId: 'ai', horizon: 'Near',
    headline_en: "UN Council Endorses Global AI Ethics Accord: 'Algorithmic Responsibility Charter' Ratified by 120 Nations",
    lead_en: "In a historic vote at the United Nations, 120 member states ratified the Algorithmic Responsibility Charter, establishing binding international standards for AI transparency, accountability, and human oversight. The accord represents the most comprehensive global AI governance framework to date.",
    milestone_en: 'Global AI Governance',
    headline_fr: "Le Conseil de l'ONU approuve l'Accord mondial sur l'éthique de l'IA, ratifié par 120 nations",
    lead_fr: "Lors d'un vote historique aux Nations Unies, 120 États membres ont ratifié la Charte de Responsabilité Algorithmique, établissant des normes internationales contraignantes pour la transparence et la surveillance humaine de l'IA.",
    milestone_fr: 'Gouvernance IA Mondiale',
    headline_it: "Il Consiglio ONU approva l'Accordo Globale sull'Etica dell'IA, ratificato da 120 Nazioni",
    lead_it: "In un voto storico alle Nazioni Unite, 120 Stati membri hanno ratificato la Carta di Responsabilità Algoritmica, stabilendo standard internazionali vincolanti per la trasparenza e la supervisione umana dell'IA.",
    milestone_it: 'Governance IA Globale',
  },
  {
    id: 'ai-4', routeId: 'ai', horizon: 'Near',
    headline_en: "Guggenheim Announces AI-Assisted Architectural Design for Abu Dhabi Wing Expansion",
    lead_en: "The Guggenheim Foundation has unveiled plans for its Abu Dhabi wing expansion, designed in collaboration with an AI architectural partner. The project marks a milestone in human-AI creative collaboration, with the AI generating 847 structural variations before the final design was selected.",
    milestone_en: 'Creative Collaboration',
    headline_fr: "Le Guggenheim annonce la conception architecturale assistée par IA pour l'expansion d'Abu Dhabi",
    lead_fr: "La Fondation Guggenheim a dévoilé ses plans pour l'expansion de son aile d'Abu Dhabi, conçue en collaboration avec un partenaire architectural IA, marquant une étape dans la collaboration créative homme-IA.",
    milestone_fr: 'Collaboration Créative',
    headline_it: "Il Guggenheim annuncia il design architettonico assistito dall'IA per l'espansione di Abu Dhabi",
    lead_it: "La Fondazione Guggenheim ha svelato i piani per l'espansione della sua ala di Abu Dhabi, progettata in collaborazione con un partner architettonico IA, segnando una pietra miliare nella collaborazione creativa uomo-IA.",
    milestone_it: 'Collaborazione Creativa',
  },
  {
    id: 'ai-5', routeId: 'ai', horizon: 'Mid',
    headline_en: "MIT Study: AI Tutors Reduce Educational Achievement Gap by 40% in Pilot Schools",
    lead_en: "A comprehensive three-year study from MIT's Education Lab reveals that AI-powered personalized tutoring systems have reduced the educational achievement gap between high- and low-income students by 40% in participating schools. The findings are prompting calls for nationwide deployment.",
    milestone_en: 'Education Equity',
    headline_fr: "Étude MIT : les tuteurs IA réduisent de 40 % les inégalités éducatives dans les écoles pilotes",
    lead_fr: "Une étude complète de trois ans du MIT révèle que les systèmes de tutorat personnalisé alimentés par l'IA ont réduit de 40 % les inégalités éducatives entre élèves à hauts et bas revenus dans les écoles participantes.",
    milestone_fr: 'Équité Éducative',
    headline_it: "Studio MIT: i tutor IA riducono del 40% il divario educativo nelle scuole pilota",
    lead_it: "Uno studio completo di tre anni del MIT rivela che i sistemi di tutoraggio personalizzato alimentati dall'IA hanno ridotto del 40% il divario educativo tra studenti ad alto e basso reddito nelle scuole partecipanti.",
    milestone_it: 'Equità Educativa',
  },
  // ── ROBOTICS ────────────────────────────────────────────────
  {
    id: 'robotics-1', routeId: 'robotics', horizon: 'Near',
    headline_en: "Nordic Consortium Pilots Domestic Humanoids, Enhancing Elderly Care",
    lead_en: "A Nordic consortium of healthcare providers has launched a pilot program deploying humanoid robots in 200 assisted living facilities across Sweden and Finland. Early results show a 30% reduction in caregiver workload and improved quality of life metrics for residents.",
    milestone_en: 'Care Innovation',
    headline_fr: "Le Consortium Nordique déploie des humanoïdes domestiques, révolutionnant l'aide aux aînés",
    lead_fr: "Un consortium nordique de prestataires de soins de santé a lancé un programme pilote déployant des robots humanoïdes dans 200 établissements de soins en Suède et en Finlande, avec une réduction de 30 % de la charge de travail des soignants.",
    milestone_fr: 'Innovation Soins',
    headline_it: "Il Consorzio Nordico sperimenta umanoidi domestici, migliorando l'assistenza anziani",
    lead_it: "Un consorzio nordico di fornitori di assistenza sanitaria ha lanciato un programma pilota che distribuisce robot umanoidi in 200 strutture di assistenza in Svezia e Finlandia, con una riduzione del 30% del carico di lavoro degli assistenti.",
    milestone_it: 'Innovazione Cura',
  },
  {
    id: 'robotics-2', routeId: 'robotics', horizon: 'Near',
    headline_en: "Midwestern U.S. Farms Report Record Efficiency Gains with Autonomous Harvesting Fleets",
    lead_en: "Agricultural cooperatives across the American Midwest have reported record efficiency gains following the deployment of autonomous harvesting fleets. The robotic systems, operating 24 hours a day, have reduced harvest time by 35% while cutting operational costs by 28%.",
    milestone_en: 'Agricultural Automation',
    headline_fr: "Les fermes du Midwest américain atteignent des gains d'efficacité records grâce aux flottes de récolte autonomes",
    lead_fr: "Les coopératives agricoles du Midwest américain ont signalé des gains d'efficacité records suite au déploiement de flottes de récolte autonomes, réduisant le temps de récolte de 35 % et les coûts opérationnels de 28 %.",
    milestone_fr: 'Automatisation Agricole',
    headline_it: "Le fattorie del Midwest americano segnalano guadagni di efficienza record con flotte di raccolta autonome",
    lead_it: "Le cooperative agricole del Midwest americano hanno riportato guadagni di efficienza record a seguito del dispiegamento di flotte di raccolta autonome, riducendo il tempo di raccolta del 35% e i costi operativi del 28%.",
    milestone_it: 'Automazione Agricola',
  },
  {
    id: 'robotics-3', routeId: 'robotics', horizon: 'Near',
    headline_en: "Paris and London Expand Autonomous Last-Mile Delivery Zones by 30%",
    lead_en: "Following successful trials, Paris and London have announced a 30% expansion of their autonomous last-mile delivery zones. The programs, which use a combination of ground robots and aerial drones, have reduced delivery emissions by 45% while improving delivery speed.",
    milestone_en: 'Urban Logistics',
    headline_fr: "Paris et Londres étendent leurs zones de livraison autonome du dernier kilomètre de 30 %",
    lead_fr: "Suite à des essais réussis, Paris et Londres ont annoncé une expansion de 30 % de leurs zones de livraison autonome du dernier kilomètre, réduisant les émissions de livraison de 45 %.",
    milestone_fr: 'Logistique Urbaine',
    headline_it: "Parigi e Londra espandono le zone di consegna autonoma dell'ultimo miglio del 30%",
    lead_it: "A seguito di prove riuscite, Parigi e Londra hanno annunciato un'espansione del 30% delle loro zone di consegna autonoma dell'ultimo miglio, riducendo le emissioni di consegna del 45%.",
    milestone_it: 'Logistica Urbana',
  },
  {
    id: 'robotics-4', routeId: 'robotics', horizon: 'Near',
    headline_en: "European Manufacturing SMEs Report 20% Boost in Worker Safety with Collaborative Robotics",
    lead_en: "A survey of 500 European small and medium-sized manufacturers reveals that the adoption of collaborative robotic systems has led to a 20% reduction in workplace injuries. The cobots work alongside human employees, handling hazardous tasks while humans focus on quality control and complex assembly.",
    milestone_en: 'Safety Milestone',
    headline_fr: "Les PME manufacturières européennes signalent une augmentation de 20 % de la sécurité des travailleurs grâce à la robotique collaborative",
    lead_fr: "Une enquête auprès de 500 PME manufacturières européennes révèle que l'adoption de systèmes robotiques collaboratifs a conduit à une réduction de 20 % des accidents du travail.",
    milestone_fr: 'Sécurité Travail',
    headline_it: "PMI manifatturiere europee registrano aumento del 20% nella sicurezza dei lavoratori con robotica collaborativa",
    lead_it: "Un sondaggio su 500 PMI manifatturiere europee rivela che l'adozione di sistemi robotici collaborativi ha portato a una riduzione del 20% degli infortuni sul lavoro.",
    milestone_it: 'Sicurezza Lavoro',
  },
  {
    id: 'robotics-5', routeId: 'robotics', horizon: 'Near',
    headline_en: "Global Rehabilitation Centers Adopt Robotic Exoskeletons, Aiding Mobility for 50,000 Patients",
    lead_en: "A new generation of AI-guided robotic exoskeletons has been adopted by rehabilitation centers across 40 countries, enabling 50,000 patients with mobility impairments to regain functional movement. The devices adapt in real-time to each patient's neurological patterns.",
    milestone_en: 'Medical Breakthrough',
    headline_fr: "Les centres de rééducation mondiaux adoptent des exosquelettes robotiques, aidant la mobilité de 50 000 patients",
    lead_fr: "Une nouvelle génération d'exosquelettes robotiques guidés par IA a été adoptée par des centres de rééducation dans 40 pays, permettant à 50 000 patients de retrouver une mobilité fonctionnelle.",
    milestone_fr: 'Percée Médicale',
    headline_it: "Centri di riabilitazione globali adottano esoscheletri robotici, aiutando la mobilità di 50.000 pazienti",
    lead_it: "Una nuova generazione di esoscheletri robotici guidati dall'IA è stata adottata da centri di riabilitazione in 40 paesi, consentendo a 50.000 pazienti di recuperare il movimento funzionale.",
    milestone_it: 'Svolta Medica',
  },
  // ── ENERGY ──────────────────────────────────────────────────
  {
    id: 'energy-1', routeId: 'energy', horizon: 'Near',
    headline_en: "ERCOT Reports Record 90% Renewable Integration During Texas Peak Demand",
    lead_en: "The Electric Reliability Council of Texas achieved a historic milestone, sustaining 90% renewable energy integration during a peak summer demand period. The achievement, powered by a combination of solar, wind, and advanced battery storage, marks a turning point for grid reliability in renewable-heavy systems.",
    milestone_en: 'Grid Milestone',
    headline_fr: "ERCOT enregistre un record d'intégration de 90 % d'énergies renouvelables lors du pic de demande au Texas",
    lead_fr: "Le Conseil de fiabilité électrique du Texas a atteint une étape historique, maintenant 90 % d'intégration d'énergie renouvelable lors d'une période de pointe estivale, grâce à une combinaison de solaire, d'éolien et de stockage par batterie avancé.",
    milestone_fr: 'Jalon Réseau',
    headline_it: "ERCOT registra un record del 90% di integrazione rinnovabile durante il picco di domanda in Texas",
    lead_it: "Il Consiglio di Affidabilità Elettrica del Texas ha raggiunto una pietra miliare storica, mantenendo il 90% di integrazione di energia rinnovabile durante un periodo di picco estivo, grazie a una combinazione di solare, eolico e stoccaggio avanzato a batteria.",
    milestone_it: 'Traguardo Rete',
  },
  {
    id: 'energy-2', routeId: 'energy', horizon: 'Near',
    headline_en: "ArcelorMittal Commissions Europe's First Zero-Emission Green Steel Plant in Bremen",
    lead_en: "ArcelorMittal has inaugurated Europe's first fully zero-emission green steel production facility in Bremen, Germany, powered entirely by hydrogen derived from renewable sources. The plant produces 2 million tonnes of steel annually with zero carbon emissions, setting a new standard for heavy industry decarbonization.",
    milestone_en: 'Industrial Decarbonization',
    headline_fr: "ArcelorMittal met en service la première usine d'acier vert zéro émission d'Europe à Brême",
    lead_fr: "ArcelorMittal a inauguré la première installation de production d'acier vert entièrement zéro émission d'Europe à Brême, alimentée entièrement par de l'hydrogène issu de sources renouvelables.",
    milestone_fr: 'Décarbonation Industrielle',
    headline_it: "ArcelorMittal commissiona il primo impianto di acciaio verde a zero emissioni d'Europa a Brema",
    lead_it: "ArcelorMittal ha inaugurato il primo impianto di produzione di acciaio verde completamente a zero emissioni d'Europa a Brema, alimentato interamente da idrogeno derivato da fonti rinnovabili.",
    milestone_it: 'Decarbonizzazione Industriale',
  },
  {
    id: 'energy-3', routeId: 'energy', horizon: 'Near',
    headline_en: "EU Household Energy Bills Drop 18% as Renewables Drive Down Wholesale Prices",
    lead_en: "European households are experiencing significant relief as average energy bills have fallen 18% year-on-year, driven by the rapid expansion of renewable generation capacity and improved grid interconnection. The price reductions are most pronounced in countries with the highest renewable penetration.",
    milestone_en: 'Consumer Benefit',
    headline_fr: "Les factures énergétiques des ménages de l'UE chutent de 18 % grâce à la baisse des prix de gros par les renouvelables",
    lead_fr: "Les ménages européens bénéficient d'un allègement significatif, les factures d'énergie moyennes ayant chuté de 18 % d'une année sur l'autre, grâce à l'expansion rapide des capacités de production renouvelable.",
    milestone_fr: 'Bénéfice Consommateur',
    headline_it: "Le bollette energetiche delle famiglie UE calano del 18% mentre le rinnovabili abbassano i prezzi all'ingrosso",
    lead_it: "Le famiglie europee stanno vivendo un significativo sollievo poiché le bollette energetiche medie sono scese del 18% su base annua, trainate dalla rapida espansione della capacità di generazione rinnovabile.",
    milestone_it: 'Beneficio Consumatori',
  },
  {
    id: 'energy-4', routeId: 'energy', horizon: 'Near',
    headline_en: "Japan's 'Solar City' Initiative Connects 50,000 Homes to Local Microgrids",
    lead_en: "Japan's Ministry of Economy has announced the successful completion of its Solar City initiative, connecting 50,000 homes across 12 cities to locally-managed solar microgrids. The program has reduced grid dependency by 60% in participating communities while creating 8,000 local energy management jobs.",
    milestone_en: 'Microgrid Expansion',
    headline_fr: "L'initiative japonaise « Villes Solaires » connecte 50 000 foyers à des micro-réseaux locaux",
    lead_fr: "Le ministère japonais de l'Économie a annoncé l'achèvement réussi de son initiative Villes Solaires, connectant 50 000 foyers dans 12 villes à des micro-réseaux solaires gérés localement.",
    milestone_fr: 'Expansion Micro-réseau',
    headline_it: "L'iniziativa giapponese 'Città Solare' collega 50.000 abitazioni a microrid locali",
    lead_it: "Il Ministero dell'Economia giapponese ha annunciato il completamento con successo della sua iniziativa Città Solare, collegando 50.000 abitazioni in 12 città a microrid solari gestiti localmente.",
    milestone_it: 'Espansione Microgrid',
  },
  {
    id: 'energy-5', routeId: 'energy', horizon: 'Mid',
    headline_en: "AfDB Announces $50 Billion in New Commitments for African Renewable Energy Projects",
    lead_en: "The African Development Bank has announced $50 billion in new financing commitments for renewable energy projects across 35 African nations, the largest single clean energy investment in the continent's history. The initiative is projected to provide electricity access to 300 million people by 2030.",
    milestone_en: 'African Energy Access',
    headline_fr: "La BAD annonce 50 milliards de dollars de nouveaux engagements pour des projets d'énergie renouvelable en Afrique",
    lead_fr: "La Banque africaine de développement a annoncé 50 milliards de dollars de nouveaux engagements de financement pour des projets d'énergie renouvelable dans 35 nations africaines, le plus grand investissement en énergie propre de l'histoire du continent.",
    milestone_fr: 'Accès Énergie Afrique',
    headline_it: "Banca Africana di Sviluppo annuncia 50 miliardi di dollari per progetti di energia rinnovabile in Africa",
    lead_it: "La Banca Africana di Sviluppo ha annunciato 50 miliardi di dollari in nuovi impegni di finanziamento per progetti di energia rinnovabile in 35 nazioni africane, il più grande singolo investimento in energia pulita nella storia del continente.",
    milestone_it: 'Accesso Energia Africa',
  },
];

export const EDITION = {
  date: { en: 'April 4, 2027', fr: '4 avril 2027', it: '4 aprile 2027' },
  vol: 'Vol. I, No. 1',
  editor_note_en: "As we mark April 2027, the velocity of progress across intertwined domains—artificial intelligence, robotics, energy, and the nature of work itself—has surpassed even the most optimistic projections of five years prior. What we are witnessing is not merely technological advancement, but a fundamental reordering of the relationship between human effort and human flourishing.\n\nFuture News exists to document this transition with clarity and without alarm. The stories in this edition are not predictions—they are reports from a world already in motion. Our correspondents cover not the disruption, but the emergence: the new institutions, the new compacts, the new possibilities that arise when humanity chooses to direct its most powerful tools toward collective elevation rather than narrow advantage.",
  editor_note_fr: "En ce mois d'avril 2027, la vélocité du progrès dans des domaines entrelacés—l'intelligence artificielle, la robotique, l'énergie et la nature même du travail—a dépassé même les projections les plus optimistes d'il y a cinq ans. Ce dont nous sommes témoins n'est pas simplement une avancée technologique, mais un réordonnancement fondamental de la relation entre l'effort humain et l'épanouissement humain.\n\nFuture News existe pour documenter cette transition avec clarté et sans alarme. Les histoires de cette édition ne sont pas des prédictions—ce sont des reportages d'un monde déjà en mouvement. Nos correspondants couvrent non pas la disruption, mais l'émergence : les nouvelles institutions, les nouveaux pactes, les nouvelles possibilités qui surgissent quand l'humanité choisit de diriger ses outils les plus puissants vers l'élévation collective.",
  editor_note_it: "Mentre segniamo l'aprile 2027, la velocità del progresso in domini intrecciati—intelligenza artificiale, robotica, energia e la natura stessa del lavoro—ha superato anche le proiezioni più ottimistiche di cinque anni fa. Ciò a cui stiamo assistendo non è semplicemente un avanzamento tecnologico, ma un riordino fondamentale del rapporto tra lo sforzo umano e il fiorire umano.\n\nFuture News esiste per documentare questa transizione con chiarezza e senza allarme. Le storie in questa edizione non sono previsioni—sono reportage da un mondo già in movimento. I nostri corrispondenti coprono non la disruption, ma l'emergenza: le nuove istituzioni, i nuovi patti, le nuove possibilità che emergono quando l'umanità sceglie di dirigere i suoi strumenti più potenti verso l'elevazione collettiva.",
  quote: {
    en: { text: "The greatest shift of our era isn't merely technological; it's a philosophical reawakening to what it means to be human when the burdens of existence are lifted by silicon and steel.", attribution: "Dr. Elara Vance, Futurist & Ethicist, 2027" },
    fr: { text: "Le plus grand changement de notre ère n'est pas seulement technologique ; c'est un réveil philosophique sur ce que signifie être humain quand les fardeaux de l'existence sont allégés par le silicium et l'acier.", attribution: "Dr. Elara Vance, Futuriste & Éthicienne, 2027" },
    it: { text: "Il più grande cambiamento della nostra era non è meramente tecnologico; è un risveglio filosofico su cosa significhi essere umani quando i fardelli dell'esistenza vengono sollevati dal silicio e dall'acciaio.", attribution: "Dr. Elara Vance, Futurista & Eticista, 2027" },
  },
};

export const CONFLUENCES = [
  {
    id: 'ai-robotics-energy',
    title_en: 'The Convergence: AI, Robots & Cheap Energy',
    title_fr: 'La Convergence : IA, Robots et Énergie Bon Marché',
    title_it: 'La Convergenza: IA, Robot ed Energia a Basso Costo',
    routes: ['ai', 'robotics', 'energy'] as RouteId[],
    analysis_en: "The simultaneous maturation of artificial intelligence, robotics, and renewable energy is not three parallel revolutions—it is one compounding transformation. Each domain amplifies the others in ways that were theoretically understood but are now empirically observable. AI makes robots smarter; cheap energy makes robots economically viable at scale; robots accelerate the deployment of renewable infrastructure.\n\nThe feedback loops are accelerating. Solar panel installation, once labor-intensive, is now largely automated by robotic systems powered by the very energy they install. AI optimizes grid management in real-time, making renewable intermittency a solved problem rather than a constraint. The result is a virtuous cycle of decreasing costs and increasing capability that is reshaping industrial economics globally.\n\nWhat emerges from this convergence is not merely efficiency—it is a new material baseline for human civilization. When energy is abundant and physical labor is automated, the fundamental scarcity that has organized human societies for millennia begins to dissolve. The question shifts from 'how do we produce enough?' to 'how do we distribute wisely and live well?'",
    analysis_fr: "La maturation simultanée de l'intelligence artificielle, de la robotique et de l'énergie renouvelable ne représente pas trois révolutions parallèles—c'est une transformation composée unique. Chaque domaine amplifie les autres de manières qui étaient théoriquement comprises mais sont maintenant empiriquement observables. L'IA rend les robots plus intelligents ; l'énergie bon marché rend les robots économiquement viables à grande échelle ; les robots accélèrent le déploiement de l'infrastructure renouvelable.\n\nLes boucles de rétroaction s'accélèrent. L'installation de panneaux solaires, autrefois à forte intensité de main-d'œuvre, est maintenant largement automatisée par des systèmes robotiques alimentés par l'énergie même qu'ils installent. L'IA optimise la gestion du réseau en temps réel, faisant de l'intermittence renouvelable un problème résolu plutôt qu'une contrainte.\n\nCe qui émerge de cette convergence n'est pas simplement l'efficacité—c'est une nouvelle base matérielle pour la civilisation humaine. Quand l'énergie est abondante et le travail physique automatisé, la rareté fondamentale qui a organisé les sociétés humaines pendant des millénaires commence à se dissoudre.",
    analysis_it: "La maturazione simultanea dell'intelligenza artificiale, della robotica e dell'energia rinnovabile non rappresenta tre rivoluzioni parallele—è un'unica trasformazione composta. Ogni dominio amplifica gli altri in modi che erano teoricamente compresi ma sono ora empiricamente osservabili. L'IA rende i robot più intelligenti; l'energia a basso costo rende i robot economicamente viabili su larga scala; i robot accelerano il dispiegamento dell'infrastruttura rinnovabile.\n\nI cicli di feedback si stanno accelerando. L'installazione di pannelli solari, un tempo ad alta intensità di lavoro, è ora in gran parte automatizzata da sistemi robotici alimentati dalla stessa energia che installano. L'IA ottimizza la gestione della rete in tempo reale, rendendo l'intermittenza rinnovabile un problema risolto piuttosto che un vincolo.\n\nCiò che emerge da questa convergenza non è semplicemente l'efficienza—è una nuova base materiale per la civiltà umana. Quando l'energia è abbondante e il lavoro fisico è automatizzato, la scarsità fondamentale che ha organizzato le società umane per millenni inizia a dissolversi.",
  },
  {
    id: 'ai-work-redistribution',
    title_en: 'The Great Redistribution: AI, Work & the New Social Contract',
    title_fr: 'La Grande Redistribution : IA, Travail et le Nouveau Contrat Social',
    title_it: 'La Grande Redistribuzione: IA, Lavoro e il Nuovo Contratto Sociale',
    routes: ['ai', 'work'] as RouteId[],
    analysis_en: "When AI systems began automating not just physical but cognitive labor—drafting, analyzing, synthesizing, advising—the implicit social contract of the industrial era entered its terminal phase. The contract that exchanged human cognitive effort for economic security was written for a world where human cognition was the primary scarce resource. That world is ending.\n\nWhat replaces it is not yet fully formed, but its outlines are visible in the policy experiments and economic data of 2027. Universal basic income pilots, creative income stipends, and four-day work weeks are not isolated experiments—they are early drafts of a new social contract that decouples human dignity and economic security from the quantity of cognitive labor one can sell.\n\nThe deeper transformation is cultural. As the necessity of work diminishes, the question of purpose becomes central. What do humans do when they are not required to work? The answer, emerging from the data of 2027, is: they create, they care, they connect, and they contribute to communities in ways that market economies systematically undervalued. The new social contract must find ways to recognize and support this broader conception of human contribution.",
    analysis_fr: "Lorsque les systèmes d'IA ont commencé à automatiser non seulement le travail physique mais aussi cognitif—rédiger, analyser, synthétiser, conseiller—le contrat social implicite de l'ère industrielle est entré dans sa phase terminale. Le contrat qui échangeait l'effort cognitif humain contre la sécurité économique était écrit pour un monde où la cognition humaine était la principale ressource rare. Ce monde prend fin.\n\nCe qui le remplace n'est pas encore entièrement formé, mais ses contours sont visibles dans les expériences politiques et les données économiques de 2027. Les programmes pilotes de revenu universel de base, les allocations de revenu créatif et les semaines de quatre jours ne sont pas des expériences isolées—ce sont des premières ébauches d'un nouveau contrat social qui découple la dignité humaine et la sécurité économique de la quantité de travail cognitif que l'on peut vendre.\n\nLa transformation plus profonde est culturelle. À mesure que la nécessité du travail diminue, la question du sens devient centrale. Que font les humains quand ils ne sont pas obligés de travailler ? La réponse, qui émerge des données de 2027, est : ils créent, ils prennent soin, ils se connectent et contribuent aux communautés d'une manière que les économies de marché sous-évaluaient systématiquement.",
    analysis_it: "Quando i sistemi di IA hanno iniziato ad automatizzare non solo il lavoro fisico ma anche quello cognitivo—redigere, analizzare, sintetizzare, consigliare—il contratto sociale implicito dell'era industriale è entrato nella sua fase terminale. Il contratto che scambiava lo sforzo cognitivo umano con la sicurezza economica era scritto per un mondo in cui la cognizione umana era la principale risorsa scarsa. Quel mondo sta finendo.\n\nCiò che lo sostituisce non è ancora pienamente formato, ma i suoi contorni sono visibili negli esperimenti politici e nei dati economici del 2027. I programmi pilota di reddito di base universale, le indennità di reddito creativo e le settimane di quattro giorni non sono esperimenti isolati—sono prime bozze di un nuovo contratto sociale che disaccoppia la dignità umana e la sicurezza economica dalla quantità di lavoro cognitivo che si può vendere.\n\nLa trasformazione più profonda è culturale. Man mano che la necessità del lavoro diminuisce, la questione dello scopo diventa centrale. Cosa fanno gli esseri umani quando non sono obbligati a lavorare? La risposta, che emerge dai dati del 2027, è: creano, si prendono cura, si connettono e contribuiscono alle comunità in modi che le economie di mercato sistematicamente sottovalutavano.",
  },
];

export const FUTURA = {
  description_en: "Futura is not simply a place on a map, but a state of being, an emerging continent forged by the shifting tectonic plates of technology and human aspiration. Imagine a landscape where the air itself hums with accessible knowledge and boundless energy, where the boundaries between the natural and the engineered merge into a harmonious, self-optimizing ecosystem. Its topography is defined not by mountains and rivers, but by the intellectual and creative currents flowing through its cities of light and its tranquil, rewilded expanses.\n\nTo traverse Futura is to journey through diverse biomes of innovation and tranquility. Vast plains stretch, not of wheat or corn, but of energy capture networks and material synthesis hubs, producing goods with effortless efficiency. Imposing urban spires rise toward the skies, each a vertical village fostering communities dedicated to art, science, and the exploration of consciousness. Yet, interwoven with these feats of engineering, are ancient forests, meticulously restored and enhanced, where bioluminescent flora guides evening walks.\n\nThe air of Futura carries a distinct quality—a scent of possibility, an absence of scarcity. It is a destination where the default mode is growth and creation, where the common human experience is one of purposeful engagement rather than repetitive labor. It is a testament to what can be achieved when humanity collectively decides to leverage its most powerful tools—intelligence and collaboration—not for conquest, but for collective elevation.",
  description_fr: "Futura n'est pas simplement un lieu sur une carte, mais un état d'être, un continent émergent forgé par les plaques tectoniques changeantes de la technologie et de l'aspiration humaine. Imaginez un paysage où l'air lui-même bourdonne de connaissances accessibles et d'énergie illimitée, où les frontières entre le naturel et l'ingénierie fusionnent en un écosystème harmonieux et auto-optimisant.\n\nParcourir Futura, c'est voyager à travers divers biomes d'innovation et de tranquillité. De vastes plaines s'étendent, non pas de blé ou de maïs, mais de réseaux de capture d'énergie et de centres de synthèse de matériaux. Des flèches urbaines imposantes s'élèvent vers les cieux, chacune étant un village vertical favorisant des communautés dédiées à l'art, à la science et à l'exploration de la conscience.\n\nL'air de Futura a une qualité distincte—un parfum de possibilité, une absence de rareté. C'est une destination où le mode par défaut est la croissance et la création, où l'expérience humaine commune est celle d'un engagement purposeful plutôt que d'un travail répétitif.",
  description_it: "Futura non è semplicemente un luogo su una mappa, ma uno stato d'essere, un continente emergente forgiato dalle mutevoli placche tettoniche della tecnologia e dell'aspirazione umana. Immaginate un paesaggio dove l'aria stessa ronza di conoscenza accessibile ed energia illimitata, dove i confini tra il naturale e l'ingegnerizzato si fondono in un ecosistema armonioso e auto-ottimizzante.\n\nAttraversare Futura è un viaggio attraverso diversi biomi di innovazione e tranquillità. Vaste pianure si estendono, non di grano o mais, ma di array di cattura energetica e hub di sintesi di materiali. Imponenti guglie urbane si innalzano verso i cieli, ognuna un villaggio verticale che promuove comunità dedicate all'arte, alla scienza e all'esplorazione della coscienza.\n\nL'aria di Futura porta una qualità distinta—un aroma di possibilità, un'assenza di scarsità. È una destinazione dove la modalità predefinita è la crescita e la creazione, dove l'esperienza umana comune è quella di un impegno mirato piuttosto che di un lavoro meccanico.",
  coordinates: [
    { name_en: 'The Plains of Abundance', name_fr: "Les Plaines de l'Abondance", name_it: "Le Pianure dell'Abbondanza", description_en: 'Where energy is no longer a constraint on human development; sprawling fields of advanced energy harvesting and storage solutions.', routeId: 'energy' as RouteId },
    { name_en: 'The Ridge of Cognitive Expansion', name_fr: "La Crête de l'Expansion Cognitive", name_it: "La Cresta dell'Espansione Cognitiva", description_en: 'Where human and machine intelligence amplify each other, fostering innovation and understanding at an unprecedented scale.', routeId: 'ai' as RouteId },
    { name_en: 'The Valley of New Work', name_fr: 'La Vallée du Nouveau Travail', name_it: 'La Valle del Nuovo Lavoro', description_en: 'Where purpose has replaced mere employment as the organizing principle of human activity, driven by creativity and shared value.', routeId: 'work' as RouteId },
    { name_en: 'The Horizon of Physical Autonomy', name_fr: "L'Horizon de l'Autonomie Physique", name_it: "L'Orizzonte dell'Autonomia Fisica", description_en: 'Where machines handle the physical burden and humans direct the creative effort, freeing us to engage with higher-order problems.', routeId: 'robotics' as RouteId },
  ],
};

// Helpers
export function getRoute(id: RouteId): Route {
  return ROUTES.find(r => r.id === id)!;
}

export function getHeadlinesByRoute(routeId: RouteId): Headline[] {
  return HEADLINES.filter(h => h.routeId === routeId);
}

export function getHeadline(id: string): Headline | undefined {
  return HEADLINES.find(h => h.id === id);
}

export function t(obj: Record<string, string>, lang: Lang): string {
  return obj[lang] ?? obj['en'] ?? '';
}
