/*
 * Loads gtag.js (GA4 + Google Ads) and fbevents.js (Meta Pixel) on first
 * user interaction, or after a fallback delay for users who never interact.
 * Keeps the heavy third-party payload off the critical rendering path —
 * queued gtag()/fbq() calls from the head stub are processed automatically
 * once these scripts arrive.
 */
(function () {
  var loaded = false;

  function loadScript(src) {
    var s = document.createElement("script");
    s.async = true;
    s.src = src;
    s.setAttribute("data-cfasync", "false");
    document.head.appendChild(s);
  }

  function loadAll() {
    if (loaded) return;
    loaded = true;
    loadScript("https://www.googletagmanager.com/gtag/js?id=G-KBGPKYML9T");
    loadScript("https://connect.facebook.net/en_US/fbevents.js");
    events.forEach(function (evt) {
      window.removeEventListener(evt, loadAll, { passive: true });
    });
    clearTimeout(fallback);
  }

  var events = ["scroll", "keydown", "click", "touchstart", "mousemove"];
  events.forEach(function (evt) {
    window.addEventListener(evt, loadAll, { passive: true, once: true });
  });

  var fallback = setTimeout(loadAll, 5000);
})();
