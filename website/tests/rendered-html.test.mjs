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
  assert.match(html, /What the program can defend today/);
  assert.match(html, /The link is not neutral/);
  assert.match(html, /Progress includes the results that did not survive/);
  assert.match(html, /The method is part of the result/);
  assert.match(html, /doft-study06-fundamental-lock-dynamics/);
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
