/* FamilyEnglish course: practice cards with instant mistake feedback, microphone input,
 * and listening passages read aloud by the browser. No answers are in the page: each answer
 * is sent to the server, which marks it and explains any mistake. */
(function () {
  const root = document.querySelector("[data-check-url]");
  const csrf = (document.querySelector("input[name=csrfmiddlewaretoken]") || {}).value;
  const bn = document.documentElement.dataset.lang === "bn";
  const T = (en, b) => (bn ? b : en);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- microphone (Chrome / Edge / Android). Other browsers type instead. ---------- */
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  window.feListen = function (onText, button) {
    if (!SR) { alert(T("Your browser can't listen. Please type what you said, or use Chrome.", "আপনার ব্রাউজার শুনতে পারে না। যা বললেন লিখুন, অথবা Chrome ব্যবহার করুন।")); return null; }
    const rec = new SR();
    rec.lang = "en-GB"; rec.interimResults = false; rec.maxAlternatives = 1;
    rec.onresult = e => onText(Array.from(e.results).map(r => r[0].transcript).join(" "));
    rec.onerror = () => button && button.classList.remove("mic-on");
    rec.onend = () => button && button.classList.remove("mic-on");
    if (button) button.classList.add("mic-on");
    rec.start();
    return rec;
  };
  document.querySelectorAll("[data-mic]").forEach(btn => {
    let rec = null;
    btn.addEventListener("click", () => {
      if (rec) { rec.stop(); rec = null; return; }
      const box = btn.closest("[data-card], [data-mic-box]");
      const input = box.querySelector("[data-answer]");
      const heard = box.querySelector("[data-heard]");
      rec = window.feListen(text => {
        rec = null;
        if (btn.hasAttribute("data-append")) input.value = (input.value + " " + text).trim();
        else input.value = text;
        if (heard) heard.textContent = T("I heard: ", "শুনেছি: ") + "“" + text + "”";
        input.dispatchEvent(new Event("input"));
        if (box.hasAttribute("data-card") && !btn.hasAttribute("data-append")) submit(box, text);
      }, btn);
    });
  });

  /* ---------- listening passages ---------- */
  document.querySelectorAll("[data-play-passage]").forEach(btn => {
    btn.addEventListener("click", () => {
      const text = document.getElementById(btn.dataset.playPassage).textContent;
      window.feSay && window.feSay(text, parseFloat(btn.dataset.rate || "0.9"));
    });
  });
  document.querySelectorAll("[data-stop]").forEach(b => b.addEventListener("click", () => window.speechSynthesis && speechSynthesis.cancel()));

  /* ---------- word counters ---------- */
  document.querySelectorAll("textarea[data-answer]").forEach(t => {
    const c = t.closest("[data-card], form, [data-mic-box]").querySelector("[data-count]");
    if (!c) return;
    const upd = () => { c.textContent = (t.value.trim().match(/\S+/g) || []).length; };
    t.addEventListener("input", upd); upd();
  });

  if (!root) return;

  /* ---------- practice cards ---------- */
  const url = root.dataset.checkUrl, source = root.dataset.source || "practice";
  const cards = Array.from(document.querySelectorAll("[data-card]"));
  const tried = new Set();

  function diffHtml(diff) {
    return '<p class="diff mt-1">' + diff.map(d => `<span class="dw dw-${d.s}">${esc(d.w)}</span>`).join("") + "</p>";
  }

  function render(card, r, given) {
    const fb = card.querySelector("[data-fb]");
    card.classList.toggle("is-ok", r.ok); card.classList.toggle("is-bad", !r.ok);
    card.querySelector("[data-state]").textContent = r.ok ? "✅" : "🔁";
    let h = `<div class="fb ${r.ok ? "ok" : "bad"} pop">`;
    if (r.kind === "say" || r.kind === "open") h += `<h4>${r.ok ? "✅" : "💡"} ${T("Score", "স্কোর")}: ${r.score}/100 ${r.ai ? '<span class="text-xs font-bold">· AI coach</span>' : ""}</h4>`;
    else h += `<h4>${r.ok ? T("✅ Correct!", "✅ ঠিক!") : T("❌ Not yet", "❌ এখনো হয়নি")}</h4>`;
    if (!r.ok && r.diff && r.diff.length) {
      h += `<p class="mt-1 text-xs font-bold uppercase text-stone-500">${T("Your answer compared with the right one", "আপনার উত্তর বনাম সঠিক উত্তর")}</p>` + diffHtml(r.diff);
      h += `<p class="text-xs text-stone-500"><span class="dw dw-wrong">${T("wrong/extra", "ভুল/বাড়তি")}</span> <span class="dw dw-missing">${T("missing", "বাদ পড়েছে")}</span></p>`;
    }
    if (!r.ok && r.expected && r.kind !== "say") h += `<p class="mt-1">${T("Right answer", "সঠিক উত্তর")}: <strong>${esc(r.expected)}</strong></p>`;
    if (r.kind === "say" && r.missed && r.missed.length) h += `<p class="mt-1">${T("Say these words more clearly", "এই শব্দগুলো আরও স্পষ্ট বলুন")}: <strong>${r.missed.map(esc).join(", ")}</strong></p>`;
    if (r.corrected) h += `<p class="mt-2 text-xs font-bold uppercase text-stone-500">${T("Better version", "সংশোধিত রূপ")}</p><p class="rounded-lg bg-white/70 p-2">${esc(r.corrected)}</p>`;
    if (r.notes && r.notes.length) h += "<ul>" + r.notes.map(n => `<li class="prose-bn">${esc(n)}</li>`).join("") + "</ul>";
    if (r.why) h += `<p class="prose-bn mt-1">📝 ${esc(r.why)}</p>`;
    if (!r.ok) h += `<p class="mt-2 text-sm font-bold">${T("Try again — practice answers can be changed.", "আবার চেষ্টা করুন — অনুশীলনে বারবার চেষ্টা করা যায়।")}</p>`;
    fb.innerHTML = h + "</div>";
    if (r.kind === "choose") card.querySelectorAll("[data-opt]").forEach(b => {
      b.classList.remove("is-right", "is-wrong");
      if (b.dataset.opt === given) b.classList.add(r.ok ? "is-right" : "is-wrong");
    });
  }

  function submit(card, given) {
    if (!given || !given.trim()) return;
    card.querySelector("[data-state]").textContent = "…";
    fetch(url, {
      method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify({ slug: card.dataset.slug, i: +card.dataset.i, answer: given, source }),
    }).then(r => r.json()).then(r => {
      if (r.error) throw new Error(r.error);
      render(card, r, given);
      tried.add(card); progress();
    }).catch(() => { card.querySelector("[data-state]").textContent = T("⚠ try again", "⚠ আবার চেষ্টা"); });
  }

  cards.forEach(card => {
    card.querySelectorAll("[data-opt]").forEach(b => b.addEventListener("click", () => submit(card, b.dataset.opt)));
    const form = card.querySelector("[data-form]");
    if (form) form.addEventListener("submit", e => { e.preventDefault(); submit(card, form.querySelector("[data-answer]").value); });
  });

  const bar = document.getElementById("practice-bar"), count = document.getElementById("practice-count"),
        finish = document.getElementById("practice-finish");
  function progress() {
    if (count) count.textContent = `${tried.size}/${cards.length}`;
    if (bar) bar.style.width = (tried.size * 100 / cards.length) + "%";
    if (finish && tried.size === cards.length) { finish.disabled = false; finish.classList.remove("opacity-50"); }
  }
  progress();
})();
