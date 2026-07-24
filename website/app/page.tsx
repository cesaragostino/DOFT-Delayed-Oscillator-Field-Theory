import Image from "next/image";
import Link from "next/link";
import { assetPath } from "@/lib/site";

const studies = [
  {
    id: "01",
    title: "Material fingerprints",
    status: "Exploratory",
    summary:
      "A constrained prime-space grammar compressed selected superconducting and superfluid scale ratios. The patterns are descriptive; they do not establish a fundamental mechanism.",
    href: "https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/tree/main/docs/studies/study-01",
  },
  {
    id: "02",
    title: "Structural oscillators",
    status: "Exploratory",
    summary:
      "A layered cluster pipeline turned fingerprint mismatch into structural noise. It remains useful as a model-building record, while its strongest physical interpretations stay unresolved.",
    href: "https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/tree/main/docs/studies/study-02",
  },
  {
    id: "03–04",
    title: "Course corrections",
    status: "No claims retained",
    summary:
      "These studies did not produce conclusions that survived review. Their role in the program is methodological: an explicit gap is more useful than inherited certainty.",
  },
  {
    id: "05",
    title: "Recursive networks",
    status: "Audited negative result",
    summary:
      "The published aggregate remains reproducible, but coupling and metric defects invalidate its main physical interpretations. The failure directly shaped the controls now used in Study 06.",
    href: "https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/tree/main/docs/studies/study-05",
  },
  {
    id: "06",
    title: "Fundamental lock dynamics",
    status: "Active",
    summary:
      "A deterministic laboratory for formation, aging, interaction, and failure. It contains the program’s strongest causal results so far—and its most disciplined record of retractions.",
    href: "https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics",
  },
];

const evidence = [
  {
    number: "01",
    label: "Reproduced",
    title: "Failure can announce itself.",
    text: (
      <>
        In one configured failure mode, a fluctuation in edge-flow variability
        preceded <strong>45 of 46</strong> observed breakdowns. It is a
        promising precursor, not yet a universal failure law.
      </>
    ),
  },
  {
    number: "02",
    label: "Falsification",
    title: "Instantaneous energy is not the state.",
    text: (
      <>
        Fold-back and intervention tests found trajectories with comparable
        energy but very different growth rates. The relevant state is
        history-dependent: epoch, phase organization, and accumulated
        dissipation matter.
      </>
    ),
  },
  {
    number: "03",
    label: "Measured",
    title: "Internal age leaves a spectral trace.",
    text: (
      <>
        In the controlled S2 sector, the effective frequency follows{" "}
        <span className="inline-equation">
          ω<sub>eff</sub> = ω<sub>0</sub>√(1 + 0.1b)
        </span>
        , where <em>b</em> is accumulated model age. External readout tracks
        that age in near-homogeneous pairs and breaks when sustained age
        asymmetry becomes large.
      </>
    ),
  },
  {
    number: "04",
    label: "Causal",
    title: "A link changes the clock.",
    text: (
      <>
        Paired branches share a bit-identical trajectory until the connection
        is switched on. The same-sign differential clock splitting appears
        across four independent draws, while the controlled paired branches
        identify the link as its cause. Paired runs also expose an earlier
        death through boundary drain.
      </>
    ),
  },
];

const lifetimePairs = [
  { label: "A · draw 3", connected: 93.6, sham: 125.5 },
  { label: "B · draw 3", connected: 117.0, sham: 125.6 },
  { label: "A · draw 4", connected: 113.0, sham: 131.1 },
  { label: "B · draw 4", connected: 125.3, sham: 131.1 },
];

const methodSteps = [
  ["01", "Pre-register", "State the observable, gate, and possible verdicts."],
  ["02", "Attack the design", "Review for leakage, confounds, and circular tests."],
  ["03", "Seal the instrument", "Commit the driver before opening the result."],
  ["04", "Run paired branches", "Change one cause and preserve shared history."],
  ["05", "Judge independently", "Recompute the claimed number from the artifact."],
  ["06", "Keep the correction", "Retractions remain attached to the evidence trail."],
];

const repositories = [
  {
    name: "Central index",
    detail: "Theory, audited findings, references, and this website",
    href: "https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory",
  },
  {
    name: "Study 01",
    detail: "Superconductors and superfluid helium",
    href: "https://github.com/cesaragostino/doft-study01-superconductors",
  },
  {
    name: "Study 02",
    detail: "Structural oscillator model",
    href: "https://github.com/cesaragostino/doft-study02-structural-oscillator",
  },
  {
    name: "Study 05",
    detail: "Recursive oscillator networks",
    href: "https://github.com/cesaragostino/doft-study05-internal-string-layers-below-quark",
  },
  {
    name: "Study 06",
    detail: "Fundamental lock dynamics · active",
    href: "https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics",
  },
];

function Arrow() {
  return <span aria-hidden="true">↗</span>;
}

export default function Home() {
  return (
    <main>
      <div className="status-strip">
        <div className="page-shell status-strip-inner">
          <span>Independent research program</span>
          <span className="status-strip-divider" aria-hidden="true" />
          <span>Current through Study 06</span>
          <span className="status-strip-date">Reviewed 24 July 2026</span>
        </div>
      </div>

      <header className="site-header page-shell">
        <a className="wordmark" href="#top" aria-label="DOFT home">
          <span className="wordmark-mark" aria-hidden="true">
            D
          </span>
          <span>
            <strong>DOFT</strong>
            <small>Delayed Oscillator Field Theory</small>
          </span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#proposition">Theory</a>
          <a href="#evidence">Evidence</a>
          <Link href="/dynamics">Dynamics</Link>
          <a href="#program">Program</a>
          <a href="#method">Method</a>
        </nav>
        <a
          className="header-link"
          href="https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics"
        >
          Study 06 <Arrow />
        </a>
      </header>

      <section className="hero page-shell" id="top">
        <div className="hero-copy">
          <p className="eyebrow">A constructive research hypothesis</p>
          <h1>
            What if persistence is a{" "}
            <em>dynamical achievement?</em>
          </h1>
          <p className="hero-lede">
            DOFT studies deterministic oscillator networks in which delay and
            memory make the present depend on the path taken to reach it. The
            aim is to understand how coherent structures form, acquire an
            internal history, interact, and fail.
          </p>
          <div
            className="generative-rule"
            aria-label="DOFT iterative generative protocol"
          >
            <strong>Randomness proposes. Dynamics selects.</strong>
            <p>
              Initial onions are drawn from a declared ensemble and evolved
              deterministically—not selected for matching a target number.
              Survivors are connected and become the next initial condition.
            </p>
            <span>
              Wave 1 · onions → dynamical selection → waves 2–N · connected
              structures
            </span>
          </div>
          <div className="hero-actions">
            <a className="button button-primary" href="#evidence">
              See the current evidence <span aria-hidden="true">↓</span>
            </a>
            <Link className="text-link" href="/dynamics">
              See the dynamics in depth <Arrow />
            </Link>
          </div>
          <p className="scope-note">
            Working theory, not established fundamental physics. The website
            distinguishes measurements, model-dependent interpretation, and
            open conjecture.
          </p>
        </div>

        <figure className="hero-system" aria-labelledby="hero-system-caption">
          <div className="system-stage">
            <Image
              src={assetPath("/doft-social-card.jpg")}
              width={1200}
              height={630}
              sizes="(max-width: 820px) calc(100vw - 32px), 50vw"
              priority
              unoptimized
              alt="Abstract delayed oscillator traces resolving into two coupled memory-bearing structures"
            />
          </div>
          <figcaption id="hero-system-caption">
            <span>DOFT conceptual field</span>
            Delay, memory, and retained relation. Visual identity—not measured
            data.
          </figcaption>
        </figure>
      </section>

      <section className="proposition section page-shell" id="proposition">
        <div className="section-heading split-heading">
          <div>
            <p className="eyebrow">The proposition</p>
            <h2>Structure is a relationship that keeps a history.</h2>
          </div>
          <p>
            The basic object is not an isolated particle analogue. It is a
            layered oscillator—informally, an <em>onion</em>—whose present
            dynamics retain information about prior phase relations and
            exchanges.
          </p>
        </div>

        <div className="constructive-line" aria-label="DOFT constructive logic">
          <div>
            <span>01</span>
            <strong>Oscillation</strong>
            <p>Supplies phase, frequency, and modes.</p>
          </div>
          <i aria-hidden="true">+</i>
          <div>
            <span>02</span>
            <strong>Delay</strong>
            <p>Makes interaction depend on a finite past.</p>
          </div>
          <i aria-hidden="true">+</i>
          <div>
            <span>03</span>
            <strong>Memory</strong>
            <p>Lets repeated relations alter future response.</p>
          </div>
          <i aria-hidden="true">→</i>
          <div className="constructive-result">
            <span>?</span>
            <strong>Persistent structure</strong>
            <p>A hypothesis to test, not an assumption.</p>
          </div>
        </div>

        <div className="use-grid">
          <article>
            <p className="mini-label">Scientific use</p>
            <h3>A causal test bench for emergence</h3>
            <p>
              Deterministic twin runs can share their entire past and differ
              by one intervention. That makes formation, interaction, and
              failure accessible to controlled counterfactual tests.
            </p>
          </article>
          <article>
            <p className="mini-label">Practical use</p>
            <h3>Hidden-state sensing and early warning</h3>
            <p>
              The program develops observables for internal age, phase-sector
              organization, boundary drain, and precursors that appear before
              a coherent state is lost.
            </p>
          </article>
          <article>
            <p className="mini-label">Long horizon</p>
            <h3>From analogies to discriminants</h3>
            <p>
              DOFT is compared with delayed resonators, synchronization,
              bright/dark modes, and dissipative symmetry breaking only when
              a measurable test can tell the descriptions apart.
            </p>
          </article>
        </div>
      </section>

      <section className="evidence-section section" id="evidence">
        <div className="page-shell">
          <div className="section-heading split-heading evidence-heading">
            <div>
              <p className="eyebrow">Current evidence</p>
              <h2>What the program can defend today.</h2>
            </div>
            <p>
              Study 06 has moved the program from pattern finding toward
              event-resolved, paired causal experiments. These statements are
              intentionally narrower than the theory’s ambition.
            </p>
          </div>

          <div className="evidence-list">
            {evidence.map((item) => (
              <article className="evidence-item" key={item.number}>
                <div className="evidence-number">{item.number}</div>
                <div>
                  <span className="evidence-label">{item.label}</span>
                  <h3>{item.title}</h3>
                </div>
                <p>{item.text}</p>
              </article>
            ))}
          </div>

          <div className="result-grid">
            <figure className="lifetime-figure">
              <div className="figure-heading">
                <div>
                  <p className="mini-label">Paired counterfactuals</p>
                  <h3>The link is not neutral.</h3>
                </div>
                <div className="legend" aria-label="Chart legend">
                  <span>
                    <i className="legend-connected" /> connected
                  </span>
                  <span>
                    <i className="legend-sham" /> no link
                  </span>
                </div>
              </div>
              <p className="figure-intro">
                Lifetime of otherwise paired branches. In each pair, the
                connected branch fails first.
              </p>
              <div className="lifetime-axis" aria-hidden="true">
                <span>90</span>
                <span>110</span>
                <span>130</span>
              </div>
              <div className="lifetime-chart">
                {lifetimePairs.map((pair) => {
                  const connectedPosition =
                    ((pair.connected - 90) / 42) * 100;
                  const shamPosition = ((pair.sham - 90) / 42) * 100;
                  return (
                    <div className="lifetime-row" key={pair.label}>
                      <span className="lifetime-label">{pair.label}</span>
                      <div
                        className="lifetime-track"
                        role="img"
                        aria-label={`${pair.label}: connected lifetime ${pair.connected.toFixed(1)}, no-link lifetime ${pair.sham.toFixed(1)} model time units`}
                      >
                        <div
                          className="lifetime-span"
                          style={{
                            left: `${connectedPosition}%`,
                            width: `${shamPosition - connectedPosition}%`,
                          }}
                        />
                        <span
                          className="lifetime-dot connected-dot"
                          style={{ left: `${connectedPosition}%` }}
                        >
                          <b>{pair.connected.toFixed(1)}</b>
                        </span>
                        <span
                          className="lifetime-dot sham-dot"
                          style={{ left: `${shamPosition}%` }}
                        >
                          <b>{pair.sham.toFixed(1)}</b>
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
              <figcaption>
                Study 06, paired draws 3–4. Time is in model units. This result
                establishes a causal effect inside the current model and
                parameter family; it is not yet a general law.
              </figcaption>
            </figure>

            <aside className="evidence-ledger">
              <p className="mini-label">Evidence ledger</p>
              <div>
                <strong>45/46</strong>
                <span>failures preceded by the registered precursor</span>
              </div>
              <div>
                <strong>4/4</strong>
                <span>draws with same-sign differential clock splitting</span>
              </div>
              <div>
                <strong>0.0</strong>
                <span>maximum paired difference before intervention</span>
              </div>
              <div>
                <strong>−0.093</strong>
                <span>
                  measured decay, matching the exact quadratic-eigenvalue mode
                </span>
              </div>
              <p className="ledger-note">
                Independent unit: one draw (an independently seeded
                realization)—not thousands of autocorrelated samples inside a
                trajectory.
              </p>
            </aside>
          </div>
        </div>
      </section>

      <section className="boundary-section">
        <div className="page-shell boundary-grid">
          <div>
            <p className="eyebrow">Claim boundary</p>
            <h2>A model can be interesting before it is fundamental.</h2>
          </div>
          <div className="boundary-copy">
            <p>
              DOFT currently demonstrates nontrivial dynamics in a constructed
              deterministic system. It has not established a new particle
              ontology, reproduced the Standard Model, or received
              experimental confirmation in matter.
            </p>
            <p>
              The near-term standard is therefore sharper and more useful:
              find causal invariants, map failure conditions, and test whether
              the same discriminants survive new seeds, topologies, and
              dynamical regimes.
            </p>
          </div>
        </div>
      </section>

      <section className="program section page-shell" id="program">
        <div className="section-heading split-heading">
          <div>
            <p className="eyebrow">The research program</p>
            <h2>Progress includes the results that did not survive.</h2>
          </div>
          <p>
            Each study changed the question. The central repository keeps the
            useful findings, the invalidated claims, and the evidence needed
            to tell them apart.
          </p>
        </div>

        <div className="study-list">
          {studies.map((study) => {
            const content = (
              <>
                <span className="study-id">{study.id}</span>
                <div className="study-title">
                  <h3>{study.title}</h3>
                  <span>{study.status}</span>
                </div>
                <p>{study.summary}</p>
                <span className="study-arrow" aria-hidden="true">
                  {study.href ? "↗" : "—"}
                </span>
              </>
            );

            return study.href ? (
              <a className="study-row" href={study.href} key={study.id}>
                {content}
              </a>
            ) : (
              <div className="study-row" key={study.id}>
                {content}
              </div>
            );
          })}
        </div>
      </section>

      <section className="method-section section" id="method">
        <div className="page-shell">
          <div className="section-heading split-heading">
            <div>
              <p className="eyebrow">How claims are made</p>
              <h2>The method is part of the result.</h2>
            </div>
            <p>
              Study 06 uses a deliberately adversarial workflow. A failed
              prediction, a broken instrument, and a surviving causal claim
              must all remain equally inspectable.
            </p>
          </div>

          <ol className="method-grid">
            {methodSteps.map(([number, title, description]) => (
              <li key={number}>
                <span>{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </li>
            ))}
          </ol>

          <div className="retraction-note">
            <span className="retraction-mark" aria-hidden="true">
              ×
            </span>
            <div>
              <p className="mini-label">A live correction record</p>
              <h3>Claims are allowed to die in public.</h3>
            </div>
            <p>
              “Same mathematical form” was withdrawn as “same law.”
              Instantaneous energy failed as a coordinate of instability.
              A proposed one-age rule broke under sustained asymmetry. Large
              within-run sigma counts were rejected as independent evidence.
            </p>
          </div>
        </div>
      </section>

      <section className="north section page-shell">
        <div className="north-title">
          <p className="eyebrow">North of the work</p>
          <h2>From a working laboratory to a portable physics claim.</h2>
        </div>
        <div className="north-columns">
          <div>
            <span>Now</span>
            <h3>Resolve the interaction mechanism</h3>
            <p>
              Separate node age, sector mixing, boundary drain, and
              event-locked response with multichannel observables and
              sub-time-unit sampling.
            </p>
          </div>
          <div>
            <span>Next</span>
            <h3>Test transportability</h3>
            <p>
              Ask which precursors, clocks, and causal link signatures survive
              new draws, asymmetric pairs, larger networks, and alternate
              failure modes.
            </p>
          </div>
          <div>
            <span>Then</span>
            <h3>Earn the physical analogy</h3>
            <p>
              Compare against known delayed resonators and dissipative
              systems using discriminating experiments—before attaching
              fundamental interpretation.
            </p>
          </div>
        </div>
      </section>

      <section className="repository-section" id="repositories">
        <div className="page-shell repository-grid">
          <div>
            <p className="eyebrow">Research record</p>
            <h2>Follow the evidence to its source.</h2>
            <p>
              The central index summarizes the program. Study repositories
              retain their code, data, logs, and exact historical context.
            </p>
          </div>
          <div className="repository-list">
            {repositories.map((repository) => (
              <a href={repository.href} key={repository.name}>
                <span>
                  <strong>{repository.name}</strong>
                  <small>{repository.detail}</small>
                </span>
                <Arrow />
              </a>
            ))}
          </div>
        </div>
      </section>

      <footer>
        <div className="page-shell footer-grid">
          <div className="footer-brand">
            <strong>DOFT</strong>
            <p>
              Delayed Oscillator Field Theory
              <br />
              An independent, open research program.
            </p>
          </div>
          <div>
            <span>Read</span>
            <a href="https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/tree/main/docs">
              Documentation
            </a>
            <a href="https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/tree/main/references">
              References
            </a>
            <a href="https://doi.org/10.5281/zenodo.16965707">
              Citation record
            </a>
          </div>
          <div>
            <span>Source</span>
            <a href="https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory">
              GitHub
            </a>
            <a href="https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics">
              Active study
            </a>
            <a href="https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory/blob/main/LICENSE">
              MIT License
            </a>
          </div>
          <div className="footer-meta">
            <p>
              Research status: active
              <br />
              Last evidence review: 24 July 2026
            </p>
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
