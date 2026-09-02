(function () {
  var geo = document.getElementById("geo");
  var anchor = document.getElementById("anchor");
  var go = document.getElementById("go");
  var kid = document.getElementById("kid-plain");
  var verifyLine = document.getElementById("verify-line");
  var viewSimple = document.getElementById("view-simple");
  var viewAdvanced = document.getElementById("view-advanced");
  var fields = {
    geo: document.getElementById("out-geo"),
    time: document.getElementById("out-time"),
    date: document.getElementById("out-date"),
    lang: document.getElementById("out-lang"),
    dialect: document.getElementById("out-dialect")
  };
  var lastAdvisory = null;

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
    lastAdvisory = null;
  }

  function setView(simple) {
    document.body.classList.toggle("simple", simple);
    viewSimple.classList.toggle("on", simple);
    viewAdvanced.classList.toggle("on", !simple);
    viewSimple.setAttribute("aria-pressed", String(simple));
    viewAdvanced.setAttribute("aria-pressed", String(!simple));
  }

  viewSimple.addEventListener("click", function () { setView(true); });
  viewAdvanced.addEventListener("click", function () { setView(false); });

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
      lastAdvisory = {
        product: "ChronoLock",
        author: "Aziel Eliab",
        version: "0.1.0",
        geo: query,
        geo_location_chosen: adv.geo_location_chosen,
        optimal_time: adv.optimal_time,
        optimal_date: adv.optimal_date,
        primary_language: adv.primary_language,
        dialect_section: adv.dialect_section
      };
      kid.textContent = "Calm morning time named. Five fields. It did not post.";
    }).catch(function () {
      clearAdvisory();
      kid.textContent = "Could not advise. Type a place and try again.";
    }).finally(function () {
      go.disabled = false;
    });
  });

  function downloadJson(filename, obj) {
    var blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function bindFileImport(inputId, onObj) {
    var el = document.getElementById(inputId);
    if (!el) return;
    el.addEventListener("change", function () {
      var f = el.files && el.files[0];
      if (!f) return;
      var reader = new FileReader();
      reader.onload = function () {
        try { onObj(JSON.parse(String(reader.result || "{}"))); }
        catch (e) { kid.textContent = "That file was not JSON."; }
      };
      reader.readAsText(f);
    });
  }

  bindFileImport("import-json", function (obj) {
    var payload = obj.payload && typeof obj.payload === "object" ? obj.payload : obj;
    var g = payload.geo || payload.geo_location_chosen || obj.geo || "";
    if (g) document.getElementById("geo").value = g;
    if (payload.geo_location_chosen) fill(fields.geo, payload.geo_location_chosen);
    if (payload.optimal_time) fill(fields.time, payload.optimal_time);
    if (payload.optimal_date) fill(fields.date, payload.optimal_date);
    if (payload.primary_language) fill(fields.lang, payload.primary_language);
    if (payload.dialect_section) fill(fields.dialect, payload.dialect_section);
    lastAdvisory = obj;
    kid.textContent = "Imported JSON. Author stays Aziel Eliab.";
  });

  var ex = document.getElementById("export-json");
  if (ex) ex.addEventListener("click", function () {
    var payload = lastAdvisory || {
      product: "ChronoLock",
      author: "Aziel Eliab",
      version: "0.1.0",
      geo: (document.getElementById("geo").value || ""),
      geo_location_chosen: document.getElementById("out-geo").textContent,
      optimal_time: document.getElementById("out-time").textContent,
      optimal_date: document.getElementById("out-date").textContent,
      primary_language: document.getElementById("out-lang").textContent,
      dialect_section: document.getElementById("out-dialect").textContent
    };
    downloadJson("chronolock-advisory.json", payload);
    kid.textContent = "Exported JSON. Share the file, not a hidden store.";
  });

  var ver = document.getElementById("verify");
  if (ver) ver.addEventListener("click", function () {
    fetch("/api/doctor").then(function (r) { return r.json(); }).then(function (d) {
      verifyLine.textContent = d.plain || (d.ok ? "Checks passed." : "Checks failed.");
      kid.textContent = d.ok
        ? "Verify: all checks passed. ChronoLock is ready. It does not post."
        : "Verify: some checks failed.";
    }).catch(function () {
      verifyLine.textContent = "Could not verify on this computer.";
    });
  });
})();
