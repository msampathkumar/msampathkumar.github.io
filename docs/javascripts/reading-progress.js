// Reading progress bar.
//
// Draws a thin horizontal line (styled as #reading-progress in
// stylesheets/extra.css) that fills left-to-right as the reader scrolls a
// page. Works with MkDocs Material's instant navigation: the `document$`
// observable emits on every (including SPA-style) page load, so we re-init the
// per-page state each time while keeping a single scroll listener.
(function () {
  "use strict";

  // Create the bar element once and reuse it across navigations.
  function ensureBar() {
    var bar = document.getElementById("reading-progress");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "reading-progress";
      document.body.appendChild(bar);
    }
    return bar;
  }

  function update() {
    var el = document.documentElement;
    var max = el.scrollHeight - el.clientHeight;
    var pct = max > 0 ? (el.scrollTop / max) * 100 : 0;
    var bar = ensureBar();
    bar.style.width = pct + "%";
  }

  // Attach the scroll/resize listeners exactly once, even though init() runs on
  // every instant-navigation page load.
  var listenersAttached = false;

  function init() {
    ensureBar();
    if (!listenersAttached) {
      window.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update, { passive: true });
      listenersAttached = true;
    }
    update(); // reset for the newly loaded page
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    // Material instant navigation: re-init on every page load.
    window.document$.subscribe(init);
  } else {
    // Fallback when Material's observable is unavailable.
    if (document.readyState !== "loading") {
      init();
    } else {
      document.addEventListener("DOMContentLoaded", init);
    }
    window.addEventListener("load", init);
  }
})();
