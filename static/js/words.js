/* Word weeks: say each word into the microphone (British English) and a spelling game. */
(function () {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const bn = document.documentElement.dataset.lang === "bn";
  const clean = s => (s || "").toLowerCase().replace(/[^a-z' ]/g, "").trim();

  document.querySelectorAll("[data-mic]").forEach(btn => {
    btn.addEventListener("click", () => {
      const row = btn.closest(".word-row");
      if (!SR) { alert(bn ? "এই ব্রাউজার শুনতে পারে না। Chrome ব্যবহার করুন, অথবা জোরে বলে নিজে মিলিয়ে নিন।" :
                       "This browser cannot listen. Use Chrome, or say it aloud and check yourself."); return; }
      const rec = new SR(); rec.lang = "en-GB"; rec.interimResults = false; rec.maxAlternatives = 5;
      row.classList.add("is-listening");
      rec.onresult = e => {
        const target = clean(btn.dataset.mic);
        const heard = Array.from(e.results[0]).map(a => clean(a.transcript));
        const ok = heard.some(h => h === target || h.split(" ").includes(target));
        row.classList.toggle("is-right", ok); row.classList.toggle("is-wrong", !ok);
        row.querySelector(".word-ok").hidden = !ok;
        if (!ok) { row.title = (bn ? "শোনা গেল: " : "Heard: ") + (heard[0] || "?"); window.feSay && window.feSay(btn.dataset.mic, 0.75); }
      };
      rec.onend = () => row.classList.remove("is-listening");
      rec.onerror = () => row.classList.remove("is-listening");
      rec.start();
    });
  });

  // Bangla meanings stay hidden until asked for: English first.
  document.querySelectorAll("[data-bn-toggle]").forEach(btn => btn.addEventListener("click", () => {
    const m = btn.nextElementSibling; m.hidden = !m.hidden;
    btn.setAttribute("aria-expanded", String(!m.hidden)); btn.classList.toggle("is-on", !m.hidden);
  }));
  const all = document.querySelector("[data-bn-all]");
  if (all) all.addEventListener("click", () => {
    const show = all.getAttribute("aria-pressed") !== "true";
    all.setAttribute("aria-pressed", String(show)); all.classList.toggle("is-on", show);
    document.querySelectorAll("[data-bn-toggle]").forEach(b => {
      b.nextElementSibling.hidden = !show; b.classList.toggle("is-on", show); b.setAttribute("aria-expanded", String(show));
    });
  });

  const box = document.getElementById("spell");
  if (!box) return;
  const words = (box.dataset.spell || "").split("|").filter(Boolean).sort(() => Math.random() - 0.5);
  const $ = s => box.querySelector(s);
  let i = 0, score = 0, tried = false;
  $("[data-spell-total]").textContent = words.length;
  const say = () => words[i] && window.feSay && window.feSay(words[i], 0.8);
  $("[data-spell-play]").addEventListener("click", say);
  function next() {
    i += 1; tried = false; $("[data-spell-input]").value = ""; $("[data-spell-n]").textContent = i;
    if (i >= words.length) {
      $("[data-spell-msg]").textContent = (bn ? "শেষ! " : "Finished! ") + score + "/" + words.length;
      const f = $("[data-spell-form]"); f.hidden = false;
      f.querySelector("[name=score]").value = score; f.querySelector("[name=total]").value = words.length;
    } else { setTimeout(say, 500); }
  }
  function check() {
    if (i >= words.length) return;
    const typed = $("[data-spell-input]").value.trim().toLowerCase();
    const right = words[i].toLowerCase();
    const msg = $("[data-spell-msg]");
    if (typed === right) {
      if (!tried) score += 1;
      $("[data-spell-score]").textContent = score;
      msg.textContent = "✓ " + words[i]; msg.className = "mt-2 min-h-[1.5rem] text-sm font-bold text-brand-700";
      next();
    } else if (!tried) {
      tried = true;
      msg.textContent = bn ? "আরেকবার শুনে চেষ্টা করুন।" : "Not quite — listen again and try once more.";
      msg.className = "mt-2 min-h-[1.5rem] text-sm font-bold text-amber-700"; say();
    } else {
      msg.textContent = (bn ? "সঠিক বানান: " : "The spelling is: ") + words[i];
      msg.className = "mt-2 min-h-[1.5rem] text-sm font-bold text-rose-700";
      setTimeout(next, 1400);
    }
  }
  $("[data-spell-check]").addEventListener("click", check);
  $("[data-spell-input]").addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); check(); } });
})();
