import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { assetPath } from "@/lib/site";
import styles from "./dynamics.module.css";

const studyRepository =
  "https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics";
const sourceCommit =
  "https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics/commit/5e2889b9842e251d8e31a2c3580ebfd0d1d40966";
const sourceArtifact =
  "https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics/blob/5e2889b9842e251d8e31a2c3580ebfd0d1d40966/artifact_estado_programa.html";

export const metadata: Metadata = {
  title: "Dynamics in Depth — DOFT",
  description:
    "Study 06 figures on formation, escape, dynamical age, instability, and causal interaction in memory-bearing oscillator structures.",
};

const particleCriteria = [
  {
    term: "Formation",
    evidence:
      "A low-energy co-ignition window selects an antisymmetric phase-locked sector.",
  },
  {
    term: "Persistence",
    evidence:
      "The selected sector holds for a finite, state-dependent interval rather than disappearing immediately.",
  },
  {
    term: "Escape",
    evidence:
      "A seeded perturbation produces a reproducible departure time from the symmetric manifold.",
  },
  {
    term: "Spectrum",
    evidence:
      "An internal odd-sector frequency tracks accumulated dynamical age and admits an exact linear-mode anchor.",
  },
  {
    term: "Interaction",
    evidence:
      "A single switched link produces a differential clock shift in bit-identical paired counterfactuals.",
  },
];

const glossary = [
  ["S2", "Fast internal layer used to define the odd/even pair sectors."],
  [
    "b",
    "Accumulated dressing or age variable in the current model; not physical time itself.",
  ],
  [
    "λ₋",
    "Local odd-sector growth rate, λ₋ = ½ d(ln E₋)/dt, estimated on in-life windows.",
  ],
  [
    "Δω",
    "Differential frequency, ω̂₋ − ω̂₊; it cancels a common intra-node eigenmode.",
  ],
  [
    "draw",
    "One independently seeded deterministic realization—the statistical unit used here.",
  ],
];

function Arrow() {
  return <span aria-hidden="true">↗</span>;
}

function Figure({
  id,
  eyebrow,
  title,
  src,
  width,
  height,
  children,
  note,
}: {
  id: string;
  eyebrow: string;
  title: string;
  src: string;
  width: number;
  height: number;
  children: React.ReactNode;
  note: string;
}) {
  return (
    <figure className={styles.figure} id={id}>
      <div className={styles.figureHeading}>
        <div>
          <p>{eyebrow}</p>
          <h3>{title}</h3>
        </div>
        <span>{note}</span>
      </div>
      <div className={styles.figureImage}>
        <Image
          src={assetPath(src)}
          width={width}
          height={height}
          sizes="(max-width: 860px) calc(100vw - 32px), 1080px"
          unoptimized
          alt={title}
        />
      </div>
      <figcaption>{children}</figcaption>
    </figure>
  );
}

export default function DynamicsPage() {
  return (
    <main className={styles.page}>
      <div className="status-strip">
        <div className="page-shell status-strip-inner">
          <span>Study 06 · evidence in depth</span>
          <span className="status-strip-divider" aria-hidden="true" />
          <span>Versioned artifact 5e2889b · pre-freeze (Study 06 sealed 29 July 2026)</span>
          <span className="status-strip-date">Reviewed 24 July 2026</span>
        </div>
      </div>

      <header className="site-header page-shell">
        <Link className="wordmark" href="/" aria-label="DOFT home">
          <span className="wordmark-mark" aria-hidden="true">
            D
          </span>
          <span>
            <strong>DOFT</strong>
            <small>Delayed Oscillator Field Theory</small>
          </span>
        </Link>
        <nav aria-label="Dynamics navigation">
          <Link href="/">Overview</Link>
          <Link href="/#evidence">Evidence</Link>
          <a href="#figures">Figures</a>
          <a href="#limits">Limits</a>
          <Link href="/#method">Method</Link>
        </nav>
        <a className="header-link" href={studyRepository}>
          Study 06 <Arrow />
        </a>
      </header>

      <section className={`page-shell ${styles.hero}`}>
        <div>
          <p className="eyebrow">Dynamics in depth</p>
          <h1>
            When does a dynamical structure begin to look{" "}
            <em>particle-like?</em>
          </h1>
          <p className={styles.heroLead}>
            Here, “particle-like” is an operational resemblance—not an
            ontological claim. The question is whether a deterministic,
            memory-bearing structure can form, persist, escape, carry a
            spectrum, and respond causally to another structure.
          </p>
        </div>

        <aside className={styles.provenance}>
          <p>Evidence boundary</p>
          <strong>4 draws · seeds 42 / 57 / 71 / 73</strong>
          <span>
            Deterministic engine at T=0, dt=8×10⁻⁵. The plots below are direct
            English re-renderings of the committed Study 06 artifact. No new
            fit or smoothing was added.
          </span>
          <a href={sourceCommit}>
            Inspect the sealed artifact commit <Arrow />
          </a>
        </aside>
      </section>

      <section className={`page-shell ${styles.criteria}`}>
        <div className={styles.sectionIntro}>
          <p className="eyebrow">Operational checklist</p>
          <h2>Five behaviors worth separating from the word “particle.”</h2>
          <p>
            None is sufficient on its own. Together they define the current
            experimental program and, more importantly, expose what remains
            missing.
          </p>
        </div>
        <div className={styles.criteriaList}>
          {particleCriteria.map((criterion, index) => (
            <div key={criterion.term}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{criterion.term}</strong>
              <p>{criterion.evidence}</p>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.figureSection} id="figures">
        <div className="page-shell">
          <div className={styles.sectionIntro}>
            <p className="eyebrow">Formation and escape</p>
            <h2>A finite-lived sector with a measurable route out.</h2>
            <p>
              The first two figures concern selection and persistence of an
              antisymmetric phase-locked sector. They are suggestive of a
              bound-state picture, but they remain statements about this model
              family.
            </p>
          </div>

          <div className={styles.figurePair}>
            <Figure
              id="hold"
              eyebrow="Study 06 · §72 / §74"
              title="The hold decays smoothly with weaker-node energy."
              src="/figures/hold-vs-energy.png"
              width={1222}
              height={778}
              note="two independent histories"
            >
              The antisymmetric lock is longest when the weaker node is
              connected at low energy. The monotone staircase reproduced in
              two pairs and across all nine threshold/window combinations.
              Fine attribution to the minimum rather than the maximum node
              energy remains confounded by pair identity.
            </Figure>

            <Figure
              id="escape"
              eyebrow="Study 06 · §73"
              title="Escape time is approximately logarithmic in seed size."
              src="/figures/escape-law.png"
              width={1222}
              height={778}
              note="effective law · n=4"
            >
              A perturbation of amplitude δ leaves the symmetric manifold at{" "}
              <span className={styles.equation}>
                t<sub>esc</sub> ≈ 7.33 + 3.06 ln(1/δ)
              </span>
              . The fit has R²=0.98 and zero censoring, but four points do not
              distinguish a logarithm from a nearby power law. The result is
              therefore retained as an effective description, not a universal
              escape law.
            </Figure>
          </div>

          <div className={styles.fullFigure}>
            <Figure
              id="epoch"
              eyebrow="Study 06 · §74"
              title="The instability pulse depends on epoch, not scalar energy."
              src="/figures/instability-pulse.png"
              width={1452}
              height={820}
              note="five connection epochs"
            >
              Connections made while the background burn is rising produce a
              full odd-sector growth pulse. Connections at the peak or on the
              falling branch remain nearly flat. The t<sub>c</sub>=80 and
              t<sub>c</sub>=104 cases revisit comparable scalar energies on
              opposite sides of the peak: the fold-back rejects instantaneous
              energy as a state coordinate for λ₋ by more than an order of
              magnitude.
            </Figure>
          </div>
        </div>
      </section>

      <section className={`page-shell ${styles.spectralSection}`}>
        <div className={styles.sectionIntro}>
          <p className="eyebrow">Spectrum and interaction</p>
          <h2>An internal clock—and a link that changes it.</h2>
          <p>
            The strongest particle-like analogy currently comes from the
            combination of a state-dependent spectral readout and a paired
            causal interaction test.
          </p>
        </div>

        <div className={styles.figurePair}>
          <Figure
            id="spectroscopy"
            eyebrow="Study 06 · §78 / §79"
            title="The odd-sector frequency reads accumulated age."
            src="/figures/spectroscopic-age.png"
            width={1279}
            height={777}
            note="three signed state points"
          >
            Cold, hold, and post-release measurements follow{" "}
            <span className={styles.equation}>
              ω<sub>eff</sub> = ω<sub>0</sub>√(1 + 0.1b)
            </span>
            . The low-frequency anchor was independently identified as the
            exact S2-block quadratic eigenmode: 48.5266, with measured{" "}
            <span className={styles.equation}>
              decay(Ψ₋) = Re(QEP) = −0.093
            </span>
            . The response to the memory kernel is measured as sublinear; its
            law remains open.
          </Figure>

          <Figure
            id="causal-splitting"
            eyebrow="Study 06 · §79-c / d / e"
            title="The connection produces a differential clock shift."
            src="/figures/causal-splitting.png"
            width={1248}
            height={725}
            note="4/4 draws · paired causality in 3–4"
          >
            The same-sign shift reproduces across four independent draws. In
            draws 3 and 4, active and sham branches are bit-identical until the
            connection is switched on, giving an exactly zero
            pre-bifurcation baseline. Those paired contrasts attribute the
            cold splitting to the link itself. Draw 4 also attributes the
            event-locked bump and release braking to the interaction under
            controlled surgery.
          </Figure>
        </div>
      </section>

      <section className={styles.limitSection} id="limits">
        <div className="page-shell">
          <div className={styles.sectionIntro}>
            <p className="eyebrow">Where the analogy stops</p>
            <h2>Interesting dynamics are not yet a particle theory.</h2>
          </div>

          <div className={styles.limitGrid}>
            <div>
              <span>Observed in the model</span>
              <ul>
                <li>Formation of an odd-parity phase sector</li>
                <li>Finite hold, release, and seeded escape</li>
                <li>State-dependent spectral readout</li>
                <li>Exact linear-mode anchor</li>
                <li>Interaction-induced clock splitting</li>
              </ul>
            </div>
            <div>
              <span>Still required</span>
              <ul>
                <li>A transferable interaction or scattering law</li>
                <li>Dispersion and scaling beyond the tested networks</li>
                <li>A conserved identity across formation and interaction</li>
                <li>Independent experimental correspondence</li>
                <li>Any connection to relativistic particle ontology</li>
              </ul>
            </div>
          </div>

          <div className={styles.glossary}>
            <p>Notation used on this page</p>
            <dl>
              {glossary.map(([term, definition]) => (
                <div key={term}>
                  <dt>{term}</dt>
                  <dd>{definition}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </section>

      <section className={styles.sourceSection}>
        <div className="page-shell">
          <div>
            <p className="eyebrow">Source record</p>
            <h2>Read the figures with their full experimental history.</h2>
          </div>
          <div>
            <p>
              The versioned artifact includes all seven original charts,
              retractions, method notes, and the qualitative distance map to
              known physics. Daily logs preserve preregistration, panel
              decisions, software receipts, and post-run verdicts.
            </p>
            <a href={sourceArtifact}>
              Open the exact source artifact <Arrow />
            </a>
            <a href={studyRepository}>
              Browse the Study 06 repository <Arrow />
            </a>
          </div>
        </div>
      </section>

      <footer>
        <div className={`page-shell ${styles.footer}`}>
          <div>
            <strong>DOFT</strong>
            <p>Dynamics in depth · Study 06</p>
          </div>
          <Link href="/">Return to the overview</Link>
          <div className={styles.footerMeta}>
            <p>Artifact reviewed 24 July 2026</p>
            <p>
              <span>Contact</span>
              <a href="mailto:cesar.agostino@gmail.com">
                cesar.agostino@gmail.com
              </a>
            </p>
            <p>
              <span>AI collaborators</span>
              <a href="https://openai.com">OpenAI</a>
              {" · "}
              <a href="https://www.anthropic.com">Anthropic</a>
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
