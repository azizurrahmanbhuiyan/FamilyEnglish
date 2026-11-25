/* FamilyEnglish short videos: a swipeable feed. Each short plays one line (animated scene read in a
   British voice with word highlighting, or a real video clip). Then the learner says it back and sees
   which words were clear. */
(function () {
  "use strict";
  var C = JSON.parse(document.getElementById("sh-config").textContent);
  var LANG = C.lang || "en", I18N = C.i18n || {};
  var feed = document.getElementById("sh-feed");
  var startBox = document.getElementById("sh-start");
  var todayEl = document.querySelector("#sh-today b");
  var ICONS = document.getElementById("tpl-icons").content;
  var csrf = (document.querySelector("[name=csrfmiddlewaretoken]") || {}).value || "";
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var items = [], offset = 0, more = true, loading = false, active = null, unlocked = false, rec = null;
  var slow = false, showBn = false, hideText = false;

  // UI words: English and Bangla are written in the code; other languages come from the server (C.i18n).
  function t(en, bn) { return LANG === "bn" ? (bn || en) : LANG === "en" ? en : (I18N[en] || en); }
  // Lesson help text: the server already put it in the learner's language as `native`.
  function n(en, native) { return LANG === "en" ? en : (native || I18N[en] || en); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function icon(n) { var x = ICONS.querySelector('[data-i="' + n + '"]'); return x ? x.innerHTML : ""; }
  function h(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
  function post(url, data) {
    return fetch(url, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-CSRFToken": csrf }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); }).catch(function () { return {}; });
  }
  function cls(s) { return s >= 80 ? "ok" : s >= 60 ? "mid" : "bad"; }

  // ------------------------------------------------------------------ loading
  function load() {
    if (loading || !more) return Promise.resolve();
    loading = true;
    var url = C.feedUrl + "?t=" + encodeURIComponent(C.topic) + "&o=" + offset + (offset === 0 && C.start ? "&s=" + encodeURIComponent(C.start) : "");
    return fetch(url, { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (d) {
      loading = false; more = d.more; offset = d.next;
      d.items.forEach(function (s) { items.push(s); feed.appendChild(card(s)); });
      if (!more) feed.appendChild(h('<div class="sh-end"><p class="text-5xl">🎉</p><p class="text-xl font-extrabold">' +
        t("You've seen every short in this topic!", "এই বিষয়ের সব ভিডিও দেখেছেন!") + '</p><a class="s-btn" href="?t=all">' + t("See more shorts", "আরও ভিডিও") + "</a></div>"));
    }).catch(function () { loading = false; });
  }

  // ------------------------------------------------------------------ one card
  function card(s) {
    var c = h('<section class="sh-card' + (s.kind === "video" ? " is-video" : "") + '" data-id="' + esc(s.id) + '"></section>');
    c._s = s;
    c.appendChild(h('<div class="sh-bg" style="--a:' + s.sky[0] + ";--b:" + s.sky[1] + '"></div>'));
    c.appendChild(h('<div class="sh-top"><span class="sh-chip">' + esc(s.scene) + " " + esc(n(s.context, s.context_bn)) + "</span>" +
      (s.mastered ? '<span class="sh-done">' + icon("ok") + "</span>" : "") + "</div>"));
    if (s.kind === "video") {
      c.appendChild(h('<div class="sh-video"><iframe title="' + esc(s.context) + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'));
    }
    var words = s.line.split(/\s+/).map(function (w, i) { return '<span data-w="' + i + '">' + esc(w) + "</span>"; }).join(" ");
    var scene = h('<div class="sh-scene">' + (s.kind === "video" ? "" : '<div class="sh-emoji">' + esc(s.scene) + '</div><div class="sh-speaker">' + esc(s.speaker) + "</div>") +
      '<div class="sh-bubble"><p class="sh-line' + (hideText ? " is-hidden" : "") + '">' + words + "</p>" +
      (s.bn ? '<p class="sh-bn"' + (showBn ? "" : " hidden") + ">" + esc(s.bn) + "</p>" : "") + "</div></div>");
    c.appendChild(scene);
    var rail = h('<div class="sh-rail"></div>');
    var bReplay = h('<button type="button" title="' + t("Play again", "আবার শুনুন") + '">' + icon("replay") + "</button>");
    var bSlow = h('<button type="button" class="' + (slow ? "is-on" : "") + '" title="' + t("Slow", "ধীরে") + '">' + icon("snail") + "</button>");
    var bText = h('<button type="button" class="' + (hideText ? "is-on" : "") + '" title="' + t("Hide the words — listen only", "শব্দ লুকান — শুধু শুনুন") + '">Aa</button>');
    var bBn = s.bn ? h('<button type="button" class="' + (showBn ? "is-on" : "") + '" title="বাংলা">বাং</button>') : null;
    var bMark = h('<button type="button" title="' + t("Save to My Words", "আমার শব্দে রাখুন") + '">' + icon("bookmark") + "</button>");
    bReplay.onclick = function () { play(c, true); };
    bSlow.onclick = function () { slow = !slow; document.querySelectorAll(".sh-rail .js-slow").forEach(function (b) { b.classList.toggle("is-on", slow); }); play(c, true); };
    bSlow.classList.add("js-slow");
    bText.onclick = function () {
      hideText = !hideText;
      document.querySelectorAll(".sh-line").forEach(function (l) { l.classList.toggle("is-hidden", hideText); });
      document.querySelectorAll(".sh-rail .js-text").forEach(function (b) { b.classList.toggle("is-on", hideText); });
    };
    bText.classList.add("js-text");
    if (bBn) {
      bBn.classList.add("js-bn");
      bBn.onclick = function () {
        showBn = !showBn;
        document.querySelectorAll(".sh-bn").forEach(function (p) { p.hidden = !showBn; });
        document.querySelectorAll(".sh-rail .js-bn").forEach(function (b) { b.classList.toggle("is-on", showBn); });
      };
    }
    bMark.onclick = function () { post(C.bookmarkUrl, { text: s.line, bn: s.bn }).then(function (r) { bMark.classList.toggle("is-on", !!r.saved); }); };
    [bReplay, bSlow, bText, bBn, bMark].forEach(function (b) { if (b) rail.appendChild(b); });
    c.appendChild(rail);
    var bottom = h('<div class="sh-bottom"><div class="sh-result"></div><p class="sh-hint">' +
      (SR ? t("Your turn — say it back", "এবার আপনি বলুন") : t("Say it aloud, then tap", "জোরে বলুন, তারপর চাপুন")) + "</p></div>");
    var mic = h('<button type="button" class="sh-mic" aria-label="' + t("Say it back", "বলুন") + '">' + icon("mic") + "</button>");
    mic.onclick = function () { sayBack(c, mic); };
    if (!SR) mic.innerHTML = "✓";
    bottom.appendChild(mic);
    c.appendChild(bottom);
    observer.observe(c);
    return c;
  }

  // ------------------------------------------------------------------ playing
  function stopAll() {
    if (window.speechSynthesis) speechSynthesis.cancel();
    try { rec && rec.abort(); } catch (e) { /* ignore */ }
    document.querySelectorAll(".sh-card.is-talking").forEach(function (c) { c.classList.remove("is-talking"); });
    document.querySelectorAll(".sh-card iframe[src]").forEach(function (f) { f.removeAttribute("src"); });
  }
  function voice() { return window.feVoice ? window.feVoice() : null; }
  function highlight(c, i) {
    c.querySelectorAll(".sh-line span").forEach(function (sp) { sp.classList.toggle("is-now", +sp.dataset.w === i); });
  }
  function play(c, force) {
    if (!unlocked) return;
    var s = c._s;
    stopAll();
    if (s.kind === "video") {
      var f = c.querySelector("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(s.youtube) + "?autoplay=1&playsinline=1&rel=0&modestbranding=1&start=" +
        (s.start || 0) + (s.end ? "&end=" + s.end : "");
      return;
    }
    if (!window.speechSynthesis) return;
    var u = new SpeechSynthesisUtterance(s.line);
    var v = voice(); if (v) u.voice = v;
    u.lang = "en-GB"; u.rate = slow ? 0.6 : 0.9;
    var starts = [], pos = 0;
    s.line.split(/\s+/).forEach(function (w) { var at = s.line.indexOf(w, pos); starts.push(at); pos = at + w.length; });
    var gotBoundary = false, timer = null;
    u.onboundary = function (e) {
      if (e.name && e.name !== "word") return;
      gotBoundary = true;
      var idx = 0; for (var k = 0; k < starts.length; k++) if (starts[k] <= e.charIndex) idx = k;
      highlight(c, idx);
    };
    u.onstart = function () {
      c.classList.add("is-talking");
      var i = 0, per = (slow ? 620 : 400);
      timer = setInterval(function () { if (gotBoundary) return clearInterval(timer); highlight(c, i++); if (i > starts.length) clearInterval(timer); }, per);
    };
    u.onend = u.onerror = function () { clearInterval(timer); c.classList.remove("is-talking"); highlight(c, -1); };
    setTimeout(function () { speechSynthesis.speak(u); }, force ? 0 : 350);
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && e.intersectionRatio >= 0.6 && active !== e.target) {
        active = e.target;
        play(active);
        var i = Array.prototype.indexOf.call(feed.querySelectorAll(".sh-card"), active);
        if (i >= items.length - 3) load();
      }
    });
  }, { root: feed, threshold: [0.6] });

  // ------------------------------------------------------------------ saying it back
  function sayBack(c, mic) {
    var s = c._s;
    if (!SR) return send(c, "", null, 70, 5);
    if (mic.classList.contains("is-listening")) { try { rec.stop(); } catch (e) { /* ignore */ } return; }
    stopAll();
    var t0 = Date.now(), got = false;
    rec = new SR(); rec.lang = "en-GB"; rec.interimResults = false; rec.maxAlternatives = 3;
    mic.classList.add("is-listening"); mic.innerHTML = icon("stop");
    var hint = c.querySelector(".sh-hint");
    hint.textContent = t("Listening…", "শুনছি…");
    rec.onresult = function (e) {
      got = true;
      var best = e.results[0][0], target = s.line.toLowerCase(), bestHit = -1;
      for (var i = 0; i < e.results[0].length; i++) {
        var a = e.results[0][i], hit = 0;
        a.transcript.toLowerCase().split(/\s+/).forEach(function (w) { if (target.indexOf(w) >= 0) hit++; });
        if (hit > bestHit) { bestHit = hit; best = a; }
      }
      send(c, best.transcript, best.confidence, null, (Date.now() - t0) / 1000);
    };
    rec.onerror = function (e) {
      if (got) return;
      hint.textContent = e.error === "not-allowed" ? t("Please allow the microphone.", "মাইক্রোফোন চালু করুন।") : t("I didn't hear you. Tap and try again.", "শুনতে পাইনি। আবার চেষ্টা করুন।");
    };
    rec.onend = function () { mic.classList.remove("is-listening"); mic.innerHTML = icon("mic"); };
    try { rec.start(); } catch (e) { mic.classList.remove("is-listening"); mic.innerHTML = icon("mic"); }
  }

  function send(c, said, conf, selfScore, secs) {
    var s = c._s;
    post(C.tryUrl, { id: s.id, said: said, confidence: conf, score: selfScore, seconds: Math.round(secs || 5) }).then(function (r) {
      if (r.locked) return lock(c);
      if (todayEl && r.today != null) todayEl.textContent = r.today;
      var line = c.querySelector(".sh-line");
      if (r.marks && r.marks.length) {
        line.innerHTML = r.marks.map(function (m, i) { return '<span data-w="' + i + '" class="' + (m.ok ? "ok" : "bad") + '">' + esc(m.w) + "</span>"; }).join(" ");
      }
      var res = c.querySelector(".sh-result");
      res.innerHTML = '<span class="sh-score ' + cls(r.score) + '">' + r.score + "%</span>" + (r.xp ? "<span>⚡ +" + r.xp + " XP</span>" : "");
      var hint = c.querySelector(".sh-hint");
      hint.textContent = r.score >= 80 ? t("Brilliant!", "দারুণ!") : r.score >= 60 ? t("Nearly — try the red words again.", "প্রায় হয়েছে — লাল শব্দগুলো আবার বলুন।")
        : t("Listen again (slowly), then try.", "আবার ধীরে শুনুন, তারপর চেষ্টা করুন।");
      if (r.score >= 70 && !c.querySelector(".sh-done")) c.querySelector(".sh-top").appendChild(h('<span class="sh-done">' + icon("ok") + "</span>"));
      if (!c.querySelector(".sh-next")) {
        var next = h('<button type="button" class="sh-next">' + t("Next", "পরের") + " " + icon("down") + "</button>");
        next.onclick = function () { var n = c.nextElementSibling; if (n) n.scrollIntoView({ behavior: "smooth" }); };
        c.querySelector(".sh-bottom").appendChild(next);
      }
    });
  }

  function lock(c) {
    stopAll();
    c.querySelectorAll(".sh-scene, .sh-rail, .sh-bottom, .sh-video").forEach(function (x) { x.remove(); });
    c.appendChild(h('<div class="sh-lock"><span class="text-5xl">' + icon("lock") + '</span><p class="text-2xl font-extrabold">' +
      t("That's your 5 free shorts today!", "আজকের ৫টি ফ্রি ভিডিও শেষ!") + '</p><p class="s-sub">' +
      t("Come back tomorrow, or get the family plan for every short, lesson and coach.", "কাল আবার আসুন, বা সব ভিডিও, পাঠ ও কোচের জন্য ফ্যামিলি প্ল্যান নিন।") +
      '</p><a class="s-btn" href="' + esc(C.payUrl) + '">' + t("See the family plan", "ফ্যামিলি প্ল্যান দেখুন") + "</a></div>"));
  }

  // ------------------------------------------------------------------ start
  document.getElementById("sh-go").onclick = function () {
    unlocked = true;
    startBox.hidden = true;
    if (window.speechSynthesis) { var warm = new SpeechSynthesisUtterance(" "); warm.volume = 0; speechSynthesis.speak(warm); }
    if (active) play(active, true);
  };
  document.addEventListener("keydown", function (e) {
    if (!active || !unlocked) return;
    if (e.key === "ArrowDown" && active.nextElementSibling) { e.preventDefault(); active.nextElementSibling.scrollIntoView({ behavior: "smooth" }); }
    if (e.key === "ArrowUp" && active.previousElementSibling) { e.preventDefault(); active.previousElementSibling.scrollIntoView({ behavior: "smooth" }); }
    if (e.key === " ") { e.preventDefault(); sayBack(active, active.querySelector(".sh-mic")); }
  });
  document.addEventListener("visibilitychange", function () { if (document.hidden) stopAll(); });
  load();
})();
