const CATEGORY_LABELS = {
  observability: "Observability",
  reference: "Reference",
  runbooks: "Runbooks",
  tools: "Tools",
  onboarding: "Onboarding",
};

function normalize(s) {
  return (s || "").toLowerCase();
}

function matchesQuery(item, q) {
  if (!q) return true;
  const hay = [
    item.title,
    item.summary,
    item.category,
    item.id,
  ]
    .map(normalize)
    .join(" ");
  return hay.includes(q);
}

function renderCard(item) {
  const statusClass =
    item.status === "beta" ? "tag tag-beta" : "tag tag-stable";
  const statusLabel = item.status === "beta" ? "beta" : "stable";
  const updated = item.updated
    ? `<span class="updated">Updated ${item.updated}</span>`
    : "";

  return `
    <a class="card" href="${item.path}" data-id="${item.id}">
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(item.summary)}</p>
      <div class="card-foot">
        <span class="${statusClass}">${statusLabel}</span>
        ${updated}
      </div>
    </a>
  `;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function groupByCategory(items) {
  const groups = new Map();
  for (const item of items) {
    const cat = item.category || "reference";
    if (!groups.has(cat)) groups.set(cat, []);
    groups.get(cat).push(item);
  }
  const order = [
    "observability",
    "reference",
    "runbooks",
    "tools",
    "onboarding",
  ];
  const sortedKeys = [
    ...order.filter((k) => groups.has(k)),
    ...[...groups.keys()].filter((k) => !order.includes(k)).sort(),
  ];
  return sortedKeys.map((key) => ({ key, items: groups.get(key) }));
}

async function loadCatalog() {
  const res = await fetch("data/utilities.json", { cache: "no-cache" });
  if (!res.ok) {
    throw new Error(`Could not load catalog (${res.status})`);
  }
  const data = await res.json();
  if (!Array.isArray(data)) {
    throw new Error("Catalog must be a JSON array");
  }
  return data;
}

function render(items, query) {
  const main = document.getElementById("catalog");
  const countEl = document.getElementById("count-live");
  const filtered = items.filter((item) => matchesQuery(item, query));

  if (countEl) {
    countEl.textContent = `${filtered.length} / ${items.length} utilities`;
  }

  if (!main) return;

  if (filtered.length === 0) {
    main.innerHTML =
      '<p class="empty-state">No utilities match your filter.</p>';
    return;
  }

  const groups = groupByCategory(filtered);
  main.innerHTML = groups
    .map(({ key, items: groupItems }) => {
      const label = CATEGORY_LABELS[key] || key;
      const cards = groupItems.map(renderCard).join("");
      return `
        <section class="category-section" data-category="${escapeHtml(key)}">
          <h2>${escapeHtml(label)}</h2>
          <div class="card-grid">${cards}</div>
        </section>
      `;
    })
    .join("");
}

async function init() {
  const search = document.getElementById("search");
  let catalog = [];

  try {
    catalog = await loadCatalog();
    catalog.sort((a, b) => a.title.localeCompare(b.title));
  } catch (err) {
    const main = document.getElementById("catalog");
    if (main) {
      main.innerHTML = `<p class="hub-error">${escapeHtml(err.message)}</p>`;
    }
    return;
  }

  const run = () => render(catalog, normalize(search?.value.trim()));

  search?.addEventListener("input", run);
  run();
}

init();
