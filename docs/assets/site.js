function renderPlaceholder(container, message) {
  container.innerHTML = "";
  const box = document.createElement("div");
  box.className = "embed-placeholder";
  box.textContent = message;
  container.appendChild(box);
}

function renderJson(container, data, source) {
  const pre = document.createElement("pre");
  pre.className = "code-block";
  pre.textContent = JSON.stringify(data, null, 2);
  container.innerHTML = "";
  container.appendChild(pre);

  if (data && typeof data === "object" && !Array.isArray(data)) {
    const keys = Object.keys(data);
    if (keys.length > 0) {
      const table = document.createElement("table");
      table.className = "kv-table";
      const body = document.createElement("tbody");
      for (const key of keys.slice(0, 8)) {
        const row = document.createElement("tr");
        const keyCell = document.createElement("th");
        keyCell.textContent = key;
        const valueCell = document.createElement("td");
        valueCell.textContent =
          typeof data[key] === "object" ? JSON.stringify(data[key]) : String(data[key]);
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        body.appendChild(row);
      }
      table.appendChild(body);
      container.appendChild(table);
    }
  }

  const footer = document.createElement("p");
  footer.className = "embed-note";
  footer.textContent = `Loaded from ${source}`;
  container.appendChild(footer);
}

function loadJsonEmbed(panel) {
  const target = panel.querySelector(".embed-target");
  const source = panel.dataset.jsonSrc;
  if (!source) {
    return;
  }

  fetch(source, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
    })
    .then((data) => renderJson(target, data, source))
    .catch(() => {
      renderPlaceholder(target, `Waiting for JSON output at ${source}`);
    });
}

function loadHtmlEmbed(panel) {
  const target = panel.querySelector(".embed-target");
  const source = panel.dataset.htmlSrc;
  if (!source) {
    return;
  }

  fetch(source, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const iframe = document.createElement("iframe");
      iframe.title = "Embedded experiment report";
      iframe.loading = "lazy";
      iframe.src = source;
      target.innerHTML = "";
      target.appendChild(iframe);
    })
    .catch(() => {
      renderPlaceholder(target, `Waiting for HTML output at ${source}`);
    });
}

function initEmbeds() {
  document.querySelectorAll(".embed-panel[data-json-src]").forEach(loadJsonEmbed);
  document.querySelectorAll(".embed-panel[data-html-src]").forEach(loadHtmlEmbed);
}

document.addEventListener("DOMContentLoaded", initEmbeds);
