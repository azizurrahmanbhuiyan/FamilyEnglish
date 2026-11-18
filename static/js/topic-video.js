/* FamilyEnglish topic video player.
 * Plays a lesson's scenes (built in learning/video.py) as a short narrated video:
 * animated cards, story-style progress bars, the browser's own voice, captions.
 * Nothing autoplays: the learner presses Play. Without a voice it still plays on a timer. */
(function () {
  const root = document.querySelector("[data-topic-video]");
  const dataEl = document.getElementById("tv-scenes");
  if (!root || !dataEl) return;

  const scenes = JSON.parse(dataEl.textContent);
  const synth = window.speechSynthesis;
  const stage = root.querySelector(".tv-stage");
  const bars = root.querySelector(".tv-bars");
  const cover = root.querySelector(".tv-cover");
  const caption = root.querySelector(".tv-caption");
  const btnPlay = root.querySelector("[data-act=play]");
  const btnSlow = root.querySelector("[data-act=slow]");
  const btnCc = root.querySelector("[data-act=cc]");
  const timeEl = root.querySelector(".tv-time");
  const totalMs = scenes.reduce((a, s) => a + s.ms, 0);

  // Captions repeat the words on screen, so on small phones they start off (CC turns them on).
  let idx = 0, playing = false, slow = false, cc = !window.matchMedia("(max-width: 560px)").matches;
  let timer = null, token = 0;
  btnCc.setAttribute("aria-pressed", String(cc));
  let sceneStart = 0, raf = null;

  scenes.forEach(() => { const i = document.createElement("i"); i.appendChild(document.createElement("b")); bars.appendChild(i); });
  const fills = [...bars.querySelectorAll("b")];

  function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function fmt(ms) { const s = Math.round(ms / 1000); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }
  function elapsedBefore(i) { return scenes.slice(0, i).reduce((a, s) => a + s.ms, 0); }

  function render(i) {
    const s = scenes[i];
    stage.querySelectorAll(".tv-scene").forEach(n => n.remove());
    const box = el("div", "tv-scene");
    if (s.eyebrow) box.appendChild(el("span", "tv-eyebrow", s.eyebrow));
    if (s.big) box.appendChild(el("div", "tv-big" + (s.big.length > 5 ? " is-long" : ""), s.big));
    if (s.kind === "recap" && s.chips) {
      const row = el("div", "tv-chips");
      s.chips.forEach((c, n) => { const ch = el("span", "", `${c.big || ""} ${c.text}`); ch.style.animationDelay = (n * 0.12) + "s"; row.appendChild(ch); });
      box.appendChild(row);
    } else if (s.text) {
      const t = el("div", "tv-text");
      if (s.kind === "answer" && s.answer && s.text.includes(s.answer)) {
        const at = s.text.indexOf(s.answer);
        t.appendChild(document.createTextNode(s.text.slice(0, at)));
        t.appendChild(el("mark", "", s.answer));
        t.appendChild(document.createTextNode(s.text.slice(at + s.answer.length)));
      } else {
        t.textContent = s.text;
      }
      box.appendChild(t);
    }
    if (s.sub) box.appendChild(el("div", "tv-sub", s.sub));
    stage.appendChild(box);
    caption.textContent = s.say || "";
    caption.hidden = !cc || !s.say;
    fills.forEach((f, n) => { f.style.width = n < i ? "100%" : "0%"; });
    timeEl.textContent = fmt(elapsedBefore(i)) + " / " + fmt(totalMs);
  }

  function animateBar() {
    cancelAnimationFrame(raf);
    const s = scenes[idx], f = fills[idx];
    const tick = () => {
      if (!playing) return;
      const p = Math.min(0.97, (performance.now() - sceneStart) / (s.ms * (slow ? 1.3 : 1)));
      f.style.width = (p * 100) + "%";
      timeEl.textContent = fmt(elapsedBefore(idx) + p * s.ms) + " / " + fmt(totalMs);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  }

  function voice() { return window.feVoice ? window.feVoice() : null; }

  function playScene() {
    const my = ++token;
    clearTimeout(timer);
    render(idx);
    sceneStart = performance.now();
    animateBar();
    const s = scenes[idx];
    const next = () => { if (my !== token || !playing) return; fills[idx].style.width = "100%"; advance(); };
    const minMs = Math.min(s.ms, 1800);
    if (synth && s.say) {
      synth.cancel();
      const u = new SpeechSynthesisUtterance(s.say);
      const v = voice(); if (v) { u.voice = v; u.lang = v.lang; } else { u.lang = "en-GB"; }
      u.rate = slow ? 0.65 : 0.85;
      let ended = false;
      u.onend = u.onerror = () => {
        if (ended) return; ended = true;
        const wait = Math.max(700, minMs - (performance.now() - sceneStart));
        timer = setTimeout(next, wait);
      };
      synth.speak(u);
      // Safety net: some browsers never fire onend.
      timer = setTimeout(() => { if (!ended) { ended = true; next(); } }, s.ms * (slow ? 2.2 : 1.8) + 2000);
    } else {
      timer = setTimeout(next, s.ms * (slow ? 1.3 : 1));
    }
  }

  function advance() {
    if (idx < scenes.length - 1) { idx += 1; playScene(); }
    else { stop(true); }
  }

  function play() {
    if (idx >= scenes.length - 1 && fills[fills.length - 1].style.width === "100%") idx = 0;
    playing = true; cover.hidden = true;
    btnPlay.textContent = "❚❚"; btnPlay.setAttribute("aria-label", "Pause");
    playScene();
  }

  function stop(finished) {
    playing = false; token++; clearTimeout(timer); cancelAnimationFrame(raf);
    if (synth) synth.cancel();
    btnPlay.textContent = "▶"; btnPlay.setAttribute("aria-label", "Play");
    if (finished) {
      fills.forEach(f => { f.style.width = "100%"; });
      timeEl.textContent = fmt(totalMs) + " / " + fmt(totalMs);
      cover.hidden = false;
      cover.querySelector(".tv-cover-btn").textContent = "↻";
      cover.querySelector(".tv-cover-title").textContent = "Watch again, or scroll down to practise";
      try { localStorage.setItem("fe-watched-" + root.dataset.lesson, "1"); } catch (e) { /* private mode */ }
      root.dispatchEvent(new CustomEvent("topicvideo:ended", { bubbles: true }));
    }
  }

  function go(delta) {
    idx = Math.max(0, Math.min(scenes.length - 1, idx + delta));
    if (playing) playScene(); else { render(idx); }
  }

  cover.addEventListener("click", () => { idx = cover.querySelector(".tv-cover-btn").textContent === "↻" ? 0 : idx; play(); });
  btnPlay.addEventListener("click", () => (playing ? stop(false) : play()));
  root.querySelector("[data-act=prev]").addEventListener("click", () => go(-1));
  root.querySelector("[data-act=next]").addEventListener("click", () => go(1));
  root.querySelector("[data-act=replay]").addEventListener("click", () => { idx = 0; play(); });
  btnSlow.addEventListener("click", () => {
    slow = !slow; btnSlow.setAttribute("aria-pressed", String(slow));
    if (playing) playScene();
  });
  btnCc.addEventListener("click", () => {
    cc = !cc; btnCc.setAttribute("aria-pressed", String(cc));
    caption.hidden = !cc || !scenes[idx].say;
  });
  const btnFull = root.querySelector("[data-act=full]");
  if (btnFull) btnFull.addEventListener("click", () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (root.requestFullscreen) root.requestFullscreen();
  });
  root.addEventListener("keydown", e => {
    if (e.key === " " || e.key === "k") { e.preventDefault(); playing ? stop(false) : play(); }
    if (e.key === "ArrowRight") go(1);
    if (e.key === "ArrowLeft") go(-1);
  });
  // Stop talking when the learner leaves the page or switches tab.
  document.addEventListener("visibilitychange", () => { if (document.hidden && playing) stop(false); });
  window.addEventListener("pagehide", () => { if (synth) synth.cancel(); });

  render(0);
  caption.hidden = true;
})();
