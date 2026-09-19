import { motion, type Variants } from "framer-motion";

const github = "https://github.com/vznd3v/Aemilius-agent";

const features = [
  {
    id: "01",
    title: "Fast onboarding",
    body: "Understand an unfamiliar codebase in minutes, not days.",
  },
  {
    id: "02",
    title: "Reads the whole tree",
    body: "Walks any project structure and surfaces what actually matters.",
  },
  {
    id: "03",
    title: "Runs locally",
    body: "Private on your own machine — no cloud, no accounts.",
  },
  {
    id: "04",
    title: "Quiet by design",
    body: "A minimal assistant that gets out of your way.",
  },
];

const engravings = [
  {
    src: "/engravings/venus.jpg",
    alt: "Gravure de la Vénus de Milo, frontispice, Paris 1821",
    caption: "Venus de Milo · 1821",
  },
  {
    src: "/engravings/caryatid.jpg",
    alt: "Gravure de deux caryatides, d'après Marcantonio Raimondi",
    caption: "Caryatids · after Marcantonio",
  },
  {
    src: "/engravings/discobolus.jpg",
    alt: "Gravure du Discobole, Illustrated Companion to the Latin Dictionary, 1849",
    caption: "Discobolus · A. Rich, 1849",
  },
];

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
};

export function Welcome() {
  return (
    <div className="min-h-screen">
      <div className="meander meander-invert" />

      <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-8">
        <a href="#top" className="font-serif text-lg tracking-[0.25em]">
          ΑΙΜΙΛΙΟΣ
        </a>
        <a
          className="text-[11px] font-semibold uppercase tracking-widest hover:underline"
          href={github}
          target="_blank"
          rel="noreferrer"
        >
          GitHub ↗
        </a>
      </header>

      <motion.section
        id="top"
        initial="hidden"
        animate="visible"
        variants={{ visible: { transition: { staggerChildren: 0.14 } } }}
        className="mx-auto max-w-3xl px-6 pt-20 pb-24 text-center md:pt-32 md:pb-32"
      >
        <motion.p
          variants={fadeUp}
          className="text-[11px] font-semibold uppercase tracking-[0.3em]"
        >
          Lightweight developer assistant
        </motion.p>
        <motion.h1
          variants={fadeUp}
          className="mt-8 font-display text-[16vw] leading-[0.82] uppercase md:text-[6rem]"
        >
          Aemilius
          <br />
          Agent
        </motion.h1>
        <motion.p
          variants={fadeUp}
          className="mx-auto mt-10 max-w-xl text-lg leading-relaxed"
        >
          Understand external codebases quickly, simply, and effortlessly —
          whether it is a trending open-source repository or the codebase at a
          new company.
        </motion.p>
        <motion.div variants={fadeUp} className="mt-12">
          <motion.a
            whileHover={{ y: -3 }}
            whileTap={{ scale: 0.97 }}
            transition={{ type: "spring", stiffness: 400, damping: 22 }}
            href={github}
            target="_blank"
            rel="noreferrer"
            className="inline-block border-2 border-ink bg-ink px-7 py-4 text-sm font-semibold uppercase text-paper"
          >
            Clone the repo
          </motion.a>
        </motion.div>
      </motion.section>

      <motion.figure
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.9 }}
        className="mx-auto max-w-[20rem] px-6 pb-24 md:pb-40"
      >
        <img
          src="/engravings/apollo.jpg"
          alt="Gravure de l’Apollon du Belvédère, 1813"
          className="stamp w-full"
        />
        <figcaption className="mt-5 text-center text-[10px] uppercase tracking-[0.2em]">
          Apollo Belvedere · 1813 engraving
        </figcaption>
      </motion.figure>

      <section className="mx-auto max-w-2xl px-6 pb-24 md:pb-36">
        <h2 className="text-[11px] font-semibold uppercase tracking-[0.3em]">
          The project
        </h2>
        <div className="mt-8 space-y-6 text-base leading-relaxed">
          <p>
            Aemilius Agent is a lightweight developer assistant for onboarding
            into unfamiliar codebases. Point it at any repository — a trending
            open-source project or the codebase at your new job — and it walks
            the tree with you, answering questions and surfacing what matters.
          </p>
          <p>
            It runs locally on your machine, stays out of the way, and asks for
            nothing more than the project itself. The goal is simple: help you
            understand strange code fast, with as little ceremony as possible.
          </p>
        </div>
      </section>

      <section id="features" className="mx-auto max-w-4xl px-6 pb-24 md:pb-36">
        <h2 className="text-[11px] font-semibold uppercase tracking-[0.3em]">
          Features
        </h2>
        <div className="mt-12 grid gap-x-16 gap-y-16 md:grid-cols-2">
          {features.map((feature, index) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, delay: (index % 2) * 0.08 }}
              className="border-t-2 border-ink pt-6"
            >
              <p className="font-serif text-xs tracking-[0.3em]">{feature.id}</p>
              <h3 className="mt-4 font-display text-xl uppercase">
                {feature.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed opacity-90">
                {feature.body}
              </p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-6 pb-24 md:pb-36">
        <div className="grid gap-16 md:grid-cols-3 md:gap-10">
          {engravings.map((engraving, index) => (
            <motion.figure
              key={engraving.src}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="aspect-[3/4] overflow-hidden">
                <img
                  src={engraving.src}
                  alt={engraving.alt}
                  className="stamp-invert h-full w-full object-cover object-top"
                />
              </div>
              <figcaption className="mt-5 text-center text-[10px] uppercase tracking-[0.2em]">
                {engraving.caption}
              </figcaption>
            </motion.figure>
          ))}
        </div>
      </section>

      <footer className="mx-auto max-w-5xl px-6 pb-24">
        <p className="font-serif text-xs uppercase tracking-[0.3em]">
          Aemilius Agent · v0.0.1 pre-alpha · MIT
        </p>
        <p className="mt-6 max-w-3xl text-[11px] leading-relaxed opacity-80">
          Images: Apollo Belvedere engraving (Bourdon / Bourgois, 1813, PD);
          Vénus de Milo, frontispiece engraving (Paris, 1821, PD); Caryatids
          (after Marcantonio Raimondi, 16th c., PD); Discobolus engraving
          (A. Rich, Illustrated Companion to the Latin Dictionary, 1849, PD),
          all via Wikimedia Commons.
        </p>
      </footer>
      <div className="meander meander-invert" />
    </div>
  );
}