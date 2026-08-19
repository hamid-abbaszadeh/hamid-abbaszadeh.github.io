---
layout: default
title: Home
nav_exclude: true
permalink: /
---

<div style="display:flex; align-items:baseline; justify-content:space-between; flex-wrap:wrap; gap:12px;">
  <div>
    <h1 style="margin-bottom:4px;">Hamid Abbaszadeh</h1>
    <p class="fs-5 fw-300" style="margin-top:0;">C++ Software Engineer — Portfolio &amp; Documentation</p>
  </div>
  <div>
    <a href="{{ site.baseurl }}/assets/Hamid_Abbaszadeh_Resume.pdf" class="btn btn-primary" download>Download PDF</a>
    <a href="{{ site.baseurl }}/assets/Hamid_Abbaszadeh_Resume.pdf" class="btn" target="_blank" rel="noopener">Open in new tab</a>
  </div>
</div>

<div id="pdf-fullscreen-wrap" style="margin-top:16px; border:1px solid #e5e5e5; border-radius:6px; overflow:hidden; width:100%; height:calc(100vh - 220px); min-height:400px;">
  <iframe
    id="pdf-viewer"
    src="{{ site.baseurl }}/assets/Hamid_Abbaszadeh_Resume.pdf"
    title="Resume PDF"
    style="width:100%; height:100%; border:none; display:block;">
  </iframe>
</div>
<noscript>
  <p><a href="{{ site.baseurl }}/assets/Hamid_Abbaszadeh_Resume.pdf">Your browser can't display the embedded PDF — click here to download it instead.</a></p>
</noscript>

<script>
  // CSS above already guarantees a sensible full-height box on load.
  // This just fine-tunes it against the real measured position, in case
  // your header/title row ends up taller or shorter than the 220px assumed above.
  (function () {
    function sizePdfViewer() {
      var wrap = document.getElementById('pdf-fullscreen-wrap');
      if (!wrap) return;
      var rect = wrap.getBoundingClientRect();
      var bottomMargin = 24;
      var available = window.innerHeight - rect.top - bottomMargin;
      if (available > 300) {
        wrap.style.height = available + 'px';
      }
    }
    window.addEventListener('resize', sizePdfViewer);
    window.addEventListener('load', sizePdfViewer);
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      sizePdfViewer();
    } else {
      document.addEventListener('DOMContentLoaded', sizePdfViewer);
    }
  })();
</script>
