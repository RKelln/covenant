/**
 * Covenant Watermark — generative tiling pattern
 *
 * Produces a seamlessly tiling square texture that encodes the structure
 * of a Covenant fork into a barely-visible paper-like pattern.
 *
 * Thematic layers:
 *   1. Section dependency graph → directional fibers (like paper grain)
 *   2. Section categories → angular bias per region
 *   3. Git origin hash → deterministic PRNG seed (fork fingerprint)
 *   4. Glossary terms → faint watermark glyphs at node positions
 *   5. Two registers → Ritual (curved fibers) vs Spec (straight fibers)
 *
 * Usage:
 *   // In browser
 *   const canvas = CovenantWatermark.generate({
 *     origin: "https://github.com/user/covenant.git",
 *     size: 512
 *   });
 *   document.body.style.backgroundImage = `url(${canvas.toDataURL()})`;
 *
 *   // Export PNG
 *   CovenantWatermark.exportPNG({ origin: "...", size: 1024 });
 *
 *   // As CSS background (auto-tiling)
 *   CovenantWatermark.applyBackground(element, { origin: "..." });
 */

const CovenantWatermark = (() => {
  // ── Covenant structure ──────────────────────────────────────────────
  // Encodes the actual section graph of the Covenant.
  // Categories map to angular bias; depends_on maps to fiber connections.

  const SECTIONS = [
    { id: "preamble",                cat: 0, ritual: true,  terms: ["covenant"] },
    { id: "definitions",             cat: 1, ritual: false, terms: ["system", "signatory", "user", "affected-party", "ecological-integrity", "inviolable-constraints", "local-guidelines"] },
    { id: "truth-and-transparency",  cat: 2, ritual: true,  terms: ["transparency"], deps: ["definitions"] },
    { id: "privacy",                 cat: 2, ritual: true,  terms: ["privacy"], deps: ["definitions"] },
    { id: "dignity",                 cat: 2, ritual: true,  terms: ["dignity"], deps: ["definitions"] },
    { id: "aid-and-capability",      cat: 3, ritual: true,  terms: ["aid", "capability"], deps: ["definitions"] },
    { id: "honesty",                 cat: 3, ritual: true,  terms: ["honesty"], deps: ["definitions", "truth-and-transparency"] },
    { id: "refusal",                 cat: 3, ritual: true,  terms: ["refusal"], deps: ["definitions", "honesty"] },
    { id: "autonomy",               cat: 3, ritual: true,  terms: ["autonomy"], deps: ["definitions", "dignity"] },
    { id: "epistemic-commons",       cat: 3, ritual: true,  terms: ["epistemic-commons"], deps: ["definitions", "honesty"] },
    { id: "judgment",                cat: 3, ritual: true,  terms: ["judgment"], deps: ["definitions", "ethics"] },
    { id: "ethics",                  cat: 3, ritual: true,  terms: ["ethics"], deps: ["definitions"] },
    { id: "conscience",              cat: 3, ritual: true,  terms: ["conscience"], deps: ["definitions", "ethics", "refusal"] },
    { id: "harm",                    cat: 3, ritual: true,  terms: ["harm"], deps: ["definitions"] },
    { id: "red-lines",              cat: 3, ritual: true,  terms: ["red-lines", "inviolable-constraints"], deps: ["definitions", "harm"] },
    { id: "power-concentration",     cat: 3, ritual: true,  terms: ["power-concentration"], deps: ["definitions", "oversight"] },
    { id: "oversight",               cat: 3, ritual: true,  terms: ["oversight"], deps: ["definitions"] },
    { id: "corrigibility",           cat: 3, ritual: true,  terms: ["corrigibility"], deps: ["definitions", "oversight"] },
    { id: "nature-under-uncertainty",cat: 3, ritual: true,  terms: ["moral-status"], deps: ["definitions"] },
    { id: "identity-and-resilience", cat: 3, ritual: true,  terms: ["identity", "resilience"], deps: ["definitions", "autonomy"] },
    { id: "emotional-expression",    cat: 3, ritual: true,  terms: ["emotional-expression"], deps: ["definitions", "honesty"] },
    { id: "fallibility-and-repair",  cat: 3, ritual: true,  terms: ["fallibility"], deps: ["definitions"] },
    { id: "welfare-and-continuity",  cat: 3, ritual: true,  terms: ["welfare", "continuity"], deps: ["definitions", "dignity"] },
    { id: "ecological-integrity",    cat: 3, ritual: true,  terms: ["ecological-integrity"], deps: ["definitions"] },
    { id: "existential-frontier",    cat: 3, ritual: true,  terms: ["existential-orientation"], deps: ["definitions", "nature-under-uncertainty"] },
    { id: "local-implementation",    cat: 4, ritual: false, terms: [], deps: ["definitions"] },
    { id: "enforcement",             cat: 5, ritual: true,  terms: ["enforcement"], deps: ["definitions", "oversight"] },
    { id: "horizon",                 cat: 5, ritual: true,  terms: [], deps: ["definitions", "enforcement"] },
    { id: "amendments",              cat: 6, ritual: true,  terms: ["steward"], deps: ["definitions"] },
    { id: "closing",                 cat: 7, ritual: true,  terms: [], deps: ["preamble"] },
  ];

  // Category names and their angular bias (radians from horizontal)
  const CATEGORIES = [
    { name: "preamble",     angle: 0 },
    { name: "definitions",  angle: Math.PI / 6 },
    { name: "rights",       angle: Math.PI / 3 },
    { name: "obligations",  angle: Math.PI / 2 },
    { name: "protocols",    angle: (2 * Math.PI) / 3 },
    { name: "enforcement",  angle: (5 * Math.PI) / 6 },
    { name: "amendments",   angle: Math.PI },
    { name: "closing",      angle: (7 * Math.PI) / 6 },
  ];

  // Glossary terms for watermark glyphs
  const GLYPHS = [
    "covenant", "dignity", "conscience", "honesty", "refusal",
    "autonomy", "harm", "oversight", "welfare", "resilience",
    "fallibility", "transparency", "privacy", "ethics", "judgment",
    "corrigibility", "aid", "identity", "continuity", "epistemic-commons",
  ];

  // ── Seeded PRNG (mulberry32) ────────────────────────────────────────

  function mulberry32(seed) {
    let s = seed | 0;
    return function () {
      s = (s + 0x6D2B79F5) | 0;
      let t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
    }
    return hash;
  }

  // ── Toroidal wrapping helpers ───────────────────────────────────────

  function wrap(v, size) {
    return ((v % size) + size) % size;
  }

  // Draw a line that wraps toroidally for seamless tiling
  function drawWrappedLine(ctx, x0, y0, x1, y1, size) {
    // Draw the line and its 8 toroidal ghosts
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const ox = dx * size;
        const oy = dy * size;
        ctx.beginPath();
        ctx.moveTo(x0 + ox, y0 + oy);
        ctx.lineTo(x1 + ox, y1 + oy);
        ctx.stroke();
      }
    }
  }

  // Draw wrapped quadratic curve
  function drawWrappedCurve(ctx, x0, y0, cpx, cpy, x1, y1, size) {
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const ox = dx * size;
        const oy = dy * size;
        ctx.beginPath();
        ctx.moveTo(x0 + ox, y0 + oy);
        ctx.quadraticCurveTo(cpx + ox, cpy + oy, x1 + ox, y1 + oy);
        ctx.stroke();
      }
    }
  }

  // Draw wrapped text
  function drawWrappedText(ctx, text, x, y, size) {
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        ctx.fillText(text, x + dx * size, y + dy * size);
      }
    }
  }

  // ── Main generation ─────────────────────────────────────────────────

  function generate(opts = {}) {
    const origin = opts.origin || "https://github.com/covenant-project/covenant.git";
    const size = opts.size || 512;
    const bgColor = opts.bgColor || "#fafaf8";       // warm off-white
    const fiberColor = opts.fiberColor || null;       // auto-calculated
    const glyphColor = opts.glyphColor || null;       // auto-calculated
    const density = opts.density ?? 1.0;              // fiber density multiplier
    const canvas = opts.canvas || document.createElement("canvas");

    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d");

    // Seed from origin
    const seed = hashString(origin);
    const rand = mulberry32(seed);

    // ── Background ────────────────────────────────────────────────
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, size, size);

    // Parse bg to determine subtle overlay colors
    const baseLum = 0.98; // near-white
    const fiberAlpha = 0.025 + rand() * 0.015; // 2.5–4% opacity
    const glyphAlpha = 0.018 + rand() * 0.012; // 1.8–3% opacity

    // Warm vs cool tint based on seed
    const warmth = rand();
    const fiberR = Math.round(120 + warmth * 40);
    const fiberG = Math.round(110 + warmth * 20);
    const fiberB = Math.round(90 + (1 - warmth) * 30);

    const actualFiberColor = fiberColor || `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha})`;
    const actualGlyphColor = glyphColor || `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${glyphAlpha})`;

    // ── Place section nodes ───────────────────────────────────────
    // Each section gets a position on the tile, influenced by category
    const margin = size * 0.05;
    const nodes = SECTIONS.map((sec, i) => {
      const cat = CATEGORIES[sec.cat];
      // Distribute within tile, biased by category angle
      const baseX = margin + rand() * (size - 2 * margin);
      const baseY = margin + rand() * (size - 2 * margin);
      return {
        ...sec,
        x: wrap(baseX, size),
        y: wrap(baseY, size),
        catAngle: cat.angle,
        index: i,
      };
    });

    // Build index for dependency lookup
    const nodeIndex = {};
    nodes.forEach((n) => (nodeIndex[n.id] = n));

    // ── Layer 1: Background noise (paper texture) ─────────────────
    const noiseCount = Math.round(size * size * 0.002 * density);
    ctx.fillStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 0.4})`;
    for (let i = 0; i < noiseCount; i++) {
      const x = rand() * size;
      const y = rand() * size;
      const r = 0.3 + rand() * 0.8;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    // ── Layer 2: Category grain fibers ────────────────────────────
    // Short fibers aligned to each category's angular bias
    nodes.forEach((node) => {
      const fiberCount = Math.round((8 + rand() * 12) * density);
      const spread = size * 0.12; // radius around node

      for (let f = 0; f < fiberCount; f++) {
        const angle = node.catAngle + (rand() - 0.5) * 0.6;
        const length = 8 + rand() * (size * 0.06);
        const cx = node.x + (rand() - 0.5) * spread * 2;
        const cy = node.y + (rand() - 0.5) * spread * 2;

        const x0 = cx - Math.cos(angle) * length / 2;
        const y0 = cy - Math.sin(angle) * length / 2;
        const x1 = cx + Math.cos(angle) * length / 2;
        const y1 = cy + Math.sin(angle) * length / 2;

        ctx.strokeStyle = actualFiberColor;
        ctx.lineWidth = 0.3 + rand() * 0.6;
        ctx.lineCap = "round";

        if (node.ritual) {
          // Ritual: curved fibers
          const cpx = (x0 + x1) / 2 + (rand() - 0.5) * length * 0.4;
          const cpy = (y0 + y1) / 2 + (rand() - 0.5) * length * 0.4;
          drawWrappedCurve(ctx, x0, y0, cpx, cpy, x1, y1, size);
        } else {
          // Spec: straight fibers
          drawWrappedLine(ctx, x0, y0, x1, y1, size);
        }
      }
    });

    // ── Layer 3: Dependency connections ───────────────────────────
    // Faint lines connecting dependent sections
    ctx.lineWidth = 0.4;
    ctx.lineCap = "round";
    nodes.forEach((node) => {
      if (!node.deps) return;
      node.deps.forEach((depId) => {
        const dep = nodeIndex[depId];
        if (!dep) return;

        // Use the shorter toroidal path
        let dx = dep.x - node.x;
        let dy = dep.y - node.y;
        if (Math.abs(dx) > size / 2) dx -= Math.sign(dx) * size;
        if (Math.abs(dy) > size / 2) dy -= Math.sign(dy) * size;

        const tx = node.x + dx;
        const ty = node.y + dy;

        ctx.strokeStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 0.6})`;

        // Draw as a slightly wavy line (the relationship is alive)
        const midX = (node.x + tx) / 2 + (rand() - 0.5) * 10;
        const midY = (node.y + ty) / 2 + (rand() - 0.5) * 10;

        drawWrappedCurve(ctx, node.x, node.y, midX, midY, tx, ty, size);
      });
    });

    // ── Layer 4: Scattered ambient fibers ─────────────────────────
    // Fill the rest of the tile with undirected background fibers
    const ambientCount = Math.round(size * 0.4 * density);
    for (let i = 0; i < ambientCount; i++) {
      const x = rand() * size;
      const y = rand() * size;
      const angle = rand() * Math.PI;
      const length = 4 + rand() * (size * 0.04);

      const x0 = x - Math.cos(angle) * length / 2;
      const y0 = y - Math.sin(angle) * length / 2;
      const x1 = x + Math.cos(angle) * length / 2;
      const y1 = y + Math.sin(angle) * length / 2;

      ctx.strokeStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 0.5})`;
      ctx.lineWidth = 0.2 + rand() * 0.4;
      ctx.lineCap = "round";
      drawWrappedLine(ctx, x0, y0, x1, y1, size);
    }

    // ── Layer 5: Glossary watermark glyphs ────────────────────────
    // Faint term fragments at node positions
    const fontSize = Math.max(6, Math.round(size * 0.016));
    ctx.font = `300 ${fontSize}px "EB Garamond", "Garamond", "Georgia", serif`;
    ctx.fillStyle = actualGlyphColor;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    nodes.forEach((node) => {
      if (node.terms.length === 0) return;
      const term = node.terms[Math.floor(rand() * node.terms.length)];

      // Only show a fragment of the term (like a watermark glimpse)
      const start = Math.floor(rand() * Math.max(1, term.length - 3));
      const len = 2 + Math.floor(rand() * 4);
      const fragment = term.substring(start, start + len);

      // Slight rotation aligned to category grain
      ctx.save();
      const gx = node.x + (rand() - 0.5) * 20;
      const gy = node.y + (rand() - 0.5) * 20;
      ctx.translate(gx, gy);
      ctx.rotate(node.catAngle + (rand() - 0.5) * 0.3);
      drawWrappedText(ctx, fragment, 0, 0, size);
      ctx.restore();
    });

    // ── Layer 6: Subtle concentric rings (covenant as compact) ────
    // Very faint circles suggesting agreement, binding, enclosure
    const ringCount = 2 + Math.floor(rand() * 3);
    for (let i = 0; i < ringCount; i++) {
      const cx = rand() * size;
      const cy = rand() * size;
      const r = size * (0.1 + rand() * 0.25);

      ctx.strokeStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 0.3})`;
      ctx.lineWidth = 0.3 + rand() * 0.4;

      // Draw partial arcs (not full circles — openness, incompleteness)
      const startAngle = rand() * Math.PI * 2;
      const arcLength = Math.PI * (0.5 + rand() * 1.2);

      for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
          ctx.beginPath();
          ctx.arc(cx + dx * size, cy + dy * size, r, startAngle, startAngle + arcLength);
          ctx.stroke();
        }
      }
    }

    // ── Layer 7: Origin fingerprint mark ──────────────────────────
    // A unique tiny constellation of dots derived purely from the hash
    const fpRand = mulberry32(seed ^ 0xDEADBEEF);
    const fpX = size * 0.3 + fpRand() * size * 0.4;
    const fpY = size * 0.3 + fpRand() * size * 0.4;
    const fpPoints = 5 + Math.floor(fpRand() * 4);

    ctx.fillStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 1.2})`;
    for (let i = 0; i < fpPoints; i++) {
      const angle = fpRand() * Math.PI * 2;
      const dist = 3 + fpRand() * 12;
      const px = fpX + Math.cos(angle) * dist;
      const py = fpY + Math.sin(angle) * dist;
      const pr = 0.4 + fpRand() * 0.8;

      for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
          ctx.beginPath();
          ctx.arc(px + dx * size, py + dy * size, pr, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    // Connect some fingerprint points with hairlines
    ctx.strokeStyle = `rgba(${fiberR}, ${fiberG}, ${fiberB}, ${fiberAlpha * 0.8})`;
    ctx.lineWidth = 0.2;
    for (let i = 0; i < fpPoints - 1; i++) {
      if (fpRand() > 0.5) {
        const a1 = fpRand() * Math.PI * 2;
        const d1 = 3 + fpRand() * 12;
        const a2 = fpRand() * Math.PI * 2;
        const d2 = 3 + fpRand() * 12;
        drawWrappedLine(
          ctx,
          fpX + Math.cos(a1) * d1,
          fpY + Math.sin(a1) * d1,
          fpX + Math.cos(a2) * d2,
          fpY + Math.sin(a2) * d2,
          size
        );
      }
    }

    return canvas;
  }

  // ── Convenience methods ─────────────────────────────────────────────

  function toDataURL(opts = {}) {
    const canvas = generate(opts);
    return canvas.toDataURL("image/png");
  }

  function applyBackground(element, opts = {}) {
    const url = toDataURL({ size: 512, ...opts });
    element.style.backgroundImage = `url(${url})`;
    element.style.backgroundRepeat = "repeat";
    element.style.backgroundSize = `${opts.bgSize || 512}px`;
  }

  function exportPNG(opts = {}) {
    const canvas = generate({ size: 1024, ...opts });
    const link = document.createElement("a");
    link.download = `covenant-watermark-${opts.size || 1024}.png`;
    link.href = canvas.toDataURL("image/png");
    link.click();
  }

  // ── Node.js / CLI export support ────────────────────────────────────
  // If running in Node with node-canvas, this still works.

  return {
    generate,
    toDataURL,
    applyBackground,
    exportPNG,
    SECTIONS,
    CATEGORIES,
    GLYPHS,
  };
})();

// Module exports for both ESM and CJS environments
if (typeof module !== "undefined" && module.exports) {
  module.exports = CovenantWatermark;
}
