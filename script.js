(function () {
  "use strict";

  var KEY = "python-egitim-hw0";
  var HOME = "baslangic";

  var topicIds = Array.prototype.map.call(
    document.querySelectorAll(".nav-link[data-topic]"),
    function (a) { return a.getAttribute("data-topic"); }
  );
  var done = new Set();
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || "[]");
    if (Array.isArray(saved)) saved.forEach(function (id) { if (topicIds.indexOf(id) > -1) done.add(id); });
  } catch (e) { /* localStorage kullanılamıyor: ilerleme yalnızca bu oturumda tutulur */ }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(Array.from(done))); } catch (e) {}
  }

  var EX_KEY = KEY + "-ornekler";
  var exDone = new Set();
  try {
    var savedEx = JSON.parse(localStorage.getItem(EX_KEY) || "[]");
    if (Array.isArray(savedEx)) savedEx.forEach(function (id) { exDone.add(String(id)); });
  } catch (e) {}
  function saveEx() {
    try { localStorage.setItem(EX_KEY, JSON.stringify(Array.from(exDone))); } catch (e) {}
  }

  /* ---------- İlerleme ---------- */
  function renderProgress() {
    document.querySelectorAll("[data-topic]").forEach(function (el) {
      var id = el.getAttribute("data-topic");
      var isDone = done.has(id);
      if (el.classList.contains("mark")) {
        el.setAttribute("aria-pressed", String(isDone));
        el.textContent = isDone ? "Konu tamamlandı (geri al)" : "Konuyu tamamlandı olarak işaretle";
      } else {
        el.classList.toggle("done", isDone);
      }
    });
    document.querySelectorAll(".ex-mark").forEach(function (btn) {
      var isDone = exDone.has(btn.getAttribute("data-ex"));
      btn.setAttribute("aria-pressed", String(isDone));
      btn.textContent = isDone ? "Örnek tamamlandı (geri al)" : "Örneği tamamladım";
      btn.closest(".example").classList.toggle("done", isDone);
    });
    document.querySelectorAll(".topic-count").forEach(function (el) {
      var prefix = el.getAttribute("data-count") + "-";
      var n = Array.from(exDone).filter(function (id) { return id.indexOf(prefix) === 0; }).length;
      el.textContent = n + " / " + el.getAttribute("data-total") + " örnek tamamlandı";
    });
    document.getElementById("progress-bar").style.width = (done.size / topicIds.length * 100) + "%";
    document.getElementById("progress-text").textContent =
      done.size + " / " + topicIds.length + " konu tamamlandı";
  }

  document.querySelectorAll(".mark").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-topic");
      if (done.has(id)) done.delete(id); else done.add(id);
      save();
      renderProgress();
    });
  });

  document.querySelectorAll(".ex-mark").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-ex");
      if (exDone.has(id)) exDone.delete(id); else exDone.add(id);
      saveEx();
      renderProgress();
    });
  });

  document.querySelectorAll(".reveal").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".output");
      var open = box.classList.toggle("revealed");
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Cevabı gizle" : "Cevabı göster";
    });
  });

  document.getElementById("reset").addEventListener("click", function () {
    if ((done.size || exDone.size) && window.confirm("Tüm ilerleme silinsin mi?")) {
      done.clear();
      exDone.clear();
      save();
      saveEx();
      renderProgress();
    }
  });

  /* ---------- Konu gösterimi ---------- */
  function showView() {
    var id = decodeURIComponent(location.hash.slice(1));
    if (id !== HOME && topicIds.indexOf(id) === -1) id = HOME;
    document.querySelectorAll(".view").forEach(function (v) {
      v.classList.toggle("active", v.id === "view-" + id);
    });
    document.querySelectorAll(".nav-link").forEach(function (a) {
      var current = a.getAttribute("data-topic") === id;
      a.classList.toggle("active", current);
      if (current) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    var title = document.querySelector("#view-" + id + " h1, #view-" + id + " h2");
    document.title = (title ? title.textContent + " | " : "") + "Python alıştırmaları";
    window.scrollTo(0, 0);
    closeMenu();
  }
  window.addEventListener("hashchange", showView);

  /* ---------- Mobil menü ---------- */
  var sidebar = document.getElementById("sidebar");
  var scrim = document.getElementById("scrim");
  var menuBtn = document.getElementById("menu-btn");

  function openMenu() {
    sidebar.classList.add("open");
    scrim.hidden = false;
    menuBtn.setAttribute("aria-expanded", "true");
  }
  function closeMenu() {
    sidebar.classList.remove("open");
    scrim.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
  }
  menuBtn.addEventListener("click", function () {
    if (sidebar.classList.contains("open")) closeMenu(); else openMenu();
  });
  scrim.addEventListener("click", closeMenu);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

  /* ---------- Python sözdizimi renklendirme ---------- */
  var KEYWORDS = new Set(("def return if elif else for while in not and or is import from as try except finally " +
    "raise with class lambda pass break continue yield None True False").split(" "));
  var BUILTINS = new Set(("print len range sorted sum max min abs list set dict tuple int float str isinstance " +
    "enumerate zip all any reversed divmod round map").split(" "));
  var TOKEN = /(#[^\n]*)|("""[\s\S]*?"""|f?"(?:\\.|[^"\\\n])*"|f?'(?:\\.|[^'\\\n])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|([\s\S])/g;

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function span(cls, text) { return '<span class="' + cls + '">' + escapeHtml(text) + "</span>"; }

  function highlight(src) {
    var out = "", prevWord = "", m;
    TOKEN.lastIndex = 0;
    while ((m = TOKEN.exec(src)) !== null) {
      if (m[1]) out += span("tk-cm", m[1]);
      else if (m[2]) out += span("tk-str", m[2]);
      else if (m[3]) out += span("tk-num", m[3]);
      else if (m[4]) {
        var w = m[4];
        if (prevWord === "def") out += span("tk-fn", w);
        else if (KEYWORDS.has(w)) out += span("tk-kw", w);
        else if (BUILTINS.has(w)) out += span("tk-bi", w);
        else out += escapeHtml(w);
        prevWord = w;
        continue;
      } else {
        out += escapeHtml(m[5]);
        if (!/\s/.test(m[5])) prevWord = "";
        continue;
      }
      prevWord = "";
    }
    return out;
  }

  document.querySelectorAll("pre.code code").forEach(function (el) {
    el.innerHTML = highlight(el.textContent);
  });

  renderProgress();
  showView();
})();
