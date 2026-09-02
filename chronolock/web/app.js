(function () {
  var geo = document.getElementById("geo");
  var anchor = document.getElementById("anchor");
  var go = document.getElementById("go");
  var fields = {
    geo: document.getElementById("out-geo"),
    time: document.getElementById("out-time"),
    date: document.getElementById("out-date"),
    lang: document.getElementById("out-lang"),
    dialect: document.getElementById("out-dialect")
  };

  function fill(el, value) {
    el.textContent = value || "—";
    if (value) el.classList.remove("empty");
    else el.classList.add("empty");
  }

  function clearAdvisory() {
    fill(fields.geo, "");
    fill(fields.time, "");
    fill(fields.date, "");
    fill(fields.lang, "");
    fill(fields.dialect, "");
  }

  fetch("/api/anchors").then(function (r) { return r.json(); }).then(function (names) {
    names.forEach(function (name) {
      var opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      anchor.appendChild(opt);
    });
  });

  fetch("/api/zones").then(function (r) { return r.json(); }).then(function (rows) {
    var body = document.getElementById("zones-body");
    body.textContent = "";
    rows.forEach(function (row) {
      var tr = document.createElement("tr");
      ["region", "iana", "local_date", "local_time", "utc_offset"].forEach(function (k) {
        var td = document.createElement("td");
        td.textContent = row[k] || "";
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
  });

  document.getElementById("advise-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var text = (geo.value || "").trim();
    var picked = (anchor.value || "").trim();
    var query = text || picked;
    go.disabled = true;
    fetch("/api/advise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ geo: query })
    }).then(function (r) { return r.json(); }).then(function (adv) {
      fill(fields.geo, adv.geo_location_chosen);
      fill(fields.time, adv.optimal_time);
      fill(fields.date, adv.optimal_date);
      fill(fields.lang, adv.primary_language);
      fill(fields.dialect, adv.dialect_section);
    }).catch(function () {
      clearAdvisory();
    }).finally(function () {
      go.disabled = false;
    });
  });

  function downloadJson(filename, obj) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }
  function bindFileImport(inputId, onObj) {
    const el = document.getElementById(inputId);
    if (!el) return;
    el.addEventListener("change", function () {
      const f = el.files && el.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = function () {
        try { onObj(JSON.parse(String(reader.result || "{}"))); }
        catch (e) { console.error(e); }
      };
      reader.readAsText(f);
    });
  }

  var lastAdvisory = null;
  bindFileImport("import-json", function (obj) {
    var g = obj.geo || obj.geo_location_chosen || "";
    if (g) document.getElementById("geo").value = g;
    if (obj.geo_location_chosen) fill(fields.geo, obj.geo_location_chosen);
    if (obj.optimal_time) fill(fields.time, obj.optimal_time);
    if (obj.optimal_date) fill(fields.date, obj.optimal_date);
    if (obj.primary_language) fill(fields.lang, obj.primary_language);
    if (obj.dialect_section) fill(fields.dialect, obj.dialect_section);
    lastAdvisory = obj;
  });
  var ex = document.getElementById("export-json");
  if (ex) ex.addEventListener("click", function () {
    var payload = lastAdvisory || {
      geo: (document.getElementById("geo").value || ""),
      geo_location_chosen: document.getElementById("out-geo").textContent,
      optimal_time: document.getElementById("out-time").textContent,
      optimal_date: document.getElementById("out-date").textContent,
      primary_language: document.getElementById("out-lang").textContent,
      dialect_section: document.getElementById("out-dialect").textContent
    };
    downloadJson("chronolock-advisory.json", payload);
  });
})();
