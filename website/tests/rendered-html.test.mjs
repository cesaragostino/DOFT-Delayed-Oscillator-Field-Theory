import assert from "node:assert/strict";
import { access } from "node:fs/promises";
import test from "node:test";

async function render(pathname = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: handler } = await import(workerUrl.href);
  const request = new Request(`http://localhost${pathname}`, {
    headers: { accept: "text/html" },
  });

  if (typeof handler === "function") {
    return handler(request);
  }

  return handler.fetch(request);
}

test("server-renders the DOFT research overview", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(
    html,
    /<title>DOFT — Delayed Oscillator Field Theory<\/title>/i,
  );
  assert.match(html, /What if persistence is a/);
  assert.match(html, /Randomness proposes\. Dynamics selects\./);
  assert.match(html, /not selected for matching a target number/);
  assert.match(html, /Wave 1 · onions/);
  assert.match(html, /waves 2–N · connected/);
  assert.match(html, /What the program can defend today/);
  assert.match(html, /The link is not neutral/);
  assert.match(html, /Progress includes the results that did not survive/);
  assert.match(html, /The method is part of the result/);
  assert.match(html, /id="repo-access"/);
  assert.match(html, /Reviewed 10 November 2026/);
  assert.match(html, /Last evidence review: 10 November 2026/);
  assert.match(html, /doft-social-card\.jpg/);
  assert.match(html, /DOFT conceptual field/);
  assert.match(html, /href="\/dynamics"/);
  assert.match(html, /mailto:cesar\.agostino@gmail\.com/);
  assert.match(html, /AI collaborators/);
  assert.match(html, /OpenAI/);
  assert.match(html, /Anthropic/);
  assert.doesNotMatch(html, /codex-preview|Building your site|SkeletonPreview/i);
});

test("server-renders the Study 06 dynamics page", async () => {
  const response = await render("/dynamics");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /Dynamics in Depth — DOFT/);
  assert.match(html, /begin to look/);
  assert.match(html, /particle-like/);
  assert.match(html, /hold-vs-energy\.png/);
  assert.match(html, /escape-law\.png/);
  assert.match(html, /instability-pulse\.png/);
  assert.match(html, /spectroscopic-age\.png/);
  assert.match(html, /causal-splitting\.png/);
  assert.match(html, /Interesting dynamics are not yet a particle theory/);
  assert.match(html, /5e2889b/);
  assert.match(html, /mailto:cesar\.agostino@gmail\.com/);
  assert.match(html, /AI collaborators/);
});

test("publishes the November 2026 evidence review without retired claims", async () => {
  const response = await render();
  const html = await response.text();
  assert.match(html, /relational map of delays, not a map of space/);
  assert.match(html, /became a sealed library of 373/);
  assert.match(html, /one common relational structure/);
  assert.match(html, /What a kick propagates: a linear cone, ordered by delay\./);
  assert.match(html, /found nothing that moves/);
  assert.match(html, /54 of 96 cells/);
  assert.match(html, /held from this page while an\s+intellectual-property review is completed/);
  assert.match(html, /Being closed now:/);
  assert.match(html, /Not closed:/);
  // held pending the intellectual-property review (owner decision, 5 November 2026)
  assert.doesNotMatch(html, /The vacuum is a regime/);
  assert.doesNotMatch(html, /The loop must be live/);
  assert.doesNotMatch(html, /LAZO|τ̇|clamp the epoch/i);
  // evidence map rendered from the exported notebook record
  assert.match(html, /Evidence map · reviewed (<!-- -->)?10 November 2026/);
  assert.match(html, /Sixteen stations on the road, scored on seven criteria\./);
  assert.match(html, /href="#north"/);
  assert.match(html, /Before particles/);
  assert.match(html, /Mobility: an organization that travels across the network/);
  assert.equal((html.match(/class="map-row"/g) ?? []).length, 16);
  assert.equal((html.match(/class="map-cell yes"/g) ?? []).length, 54 + 1);
  // the rivals table shares the "not applicable" cell: 42 cells + its own legend entry
  assert.equal((html.match(/class="map-cell na"/g) ?? []).length, 16 + 1 + 42 + 1);
  // rivals table (the negative ledger), rendered from the exported notebook record (10 November 2026)
  assert.match(html, /Rivals table · reviewed (<!-- -->)?10 November 2026/);
  assert.match(html, /The same sixteen stations, against seven cheaper explanations\./);
  assert.match(html, /Neither is read without the other\./);
  assert.match(html, /they are not added into one score\./);
  assert.equal((html.match(/class="map-row rivals-row"/g) ?? []).length, 16);
  assert.equal((html.match(/class="map-cell wins"/g) ?? []).length, 5 + 1);
  assert.equal((html.match(/class="map-cell partial"/g) ?? []).length, 16 + 1);
  assert.equal((html.match(/class="map-cell excluded"/g) ?? []).length, 6 + 1);
  assert.equal((html.match(/class="map-cell testing"/g) ?? []).length, 1 + 1);
  // the notebook's section numbers and notes do not travel to the page
  assert.doesNotMatch(html, /§\s?2[0-9]{2}/);
  assert.doesNotMatch(html, /a universe with no space\./);
  assert.doesNotMatch(html, /multi-source tomography is the\s+pre-registered next test/);
  assert.doesNotMatch(html, /href="\/lab\/emergent\/"/);

  const { readFile } = await import("node:fs/promises");
  const tauLab = await readFile(new URL("../public/lab/caldo3d/index.html", import.meta.url), "utf8");
  assert.doesNotMatch(tauLab, /el espacio emergió|space <b>emerged<\/b>/);
  assert.match(tauLab, /It is not a map of space/);
  assert.match(tauLab, /No es un mapa espacial/);
  assert.doesNotMatch(tauLab, /lab\/emergent/);

  // a literal backslash-n appended by a patch script once folded into the next
  // selector ("n .north-lede") and left the North lede unstyled (5 November 2026)
  const stylesheet = await readFile(new URL("../app/globals.css", import.meta.url), "utf8");
  assert.doesNotMatch(stylesheet, /\\[nrt]/);

  // papers archived on Zenodo (added 5 November 2026)
  for (const record of ["17620713", "17784477", "18214459", "17014532"]) {
    assert.match(html, new RegExp(`href="https://zenodo\\.org/records/${record}"`));
  }
  assert.match(html, /Papers · archived on Zenodo/);
  assert.match(html, /href="#papers"/);
  assert.match(stylesheet, /^\.north-lede \{/m);
});

test("ships the project social preview and no disposable starter assets", async () => {
  const assets = [
    "../public/doft-social-card.jpg",
    "../public/figures/hold-vs-energy.png",
    "../public/figures/escape-law.png",
    "../public/figures/instability-pulse.png",
    "../public/figures/spectroscopic-age.png",
    "../public/figures/causal-splitting.png",
  ];
  await Promise.all(assets.map((asset) => access(new URL(asset, import.meta.url))));
  await assert.rejects(
    access(new URL("../app/_sites-preview/SkeletonPreview.tsx", import.meta.url)),
  );
  await assert.rejects(
    access(new URL("../public/favicon.svg", import.meta.url)),
  );
});
