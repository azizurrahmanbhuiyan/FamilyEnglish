/* "Talk at home": play each two-line talk with two voices and check the child's line with the microphone. */
(function () {
  const synth = window.speechSynthesis;
  const bn = document.documentElement.dataset.lang === "bn";
  const T = (en, b) => (bn ? b : en);
  // A slightly different voice for each person (pitch, speed), so a talk sounds like two people.
  const VOICES = { child: [1.35, 0.85], sister: [1.25, 0.9], brother: [1.0, 0.9], mamma: [1.15, 0.85],
                   daddy: [0.8, 0.85], grandma: [1.05, 0.75], grandpa: [0.7, 0.75] };

  function utter(text, who) {
    const u = new SpeechSynthesisUtterance(text);
    const v = window.feVoice && window.feVoice();
    if (v) u.voice = v;
    u.lang = v ? v.lang : "en-GB";
    const [pitch, rate] = VOICES[who] || [1, 0.85];
    u.pitch = pitch; u.rate = rate;
    return u;
  }
  function play(lines) {
    if (!synth) { alert(T("Your browser cannot speak. Please read the lines aloud.", "আপনার ব্রাউজার পড়তে পারে না। লাইনগুলো জোরে পড়ুন।")); return; }
    synth.cancel();
    lines.forEach(([text, who]) => synth.speak(utter(text, who)));
  }

  document.querySelectorAll("[data-talk]").forEach(card => {
    const plays = Array.from(card.querySelectorAll(".talk-play"));
    plays.forEach(b => b.addEventListener("click", () => play([[b.dataset.line, b.dataset.voice]])));
    const both = card.querySelector("[data-play-both]");
    if (both) both.addEventListener("click", () => play(plays.map(b => [b.dataset.line, b.dataset.voice])));

    const sayBtn = card.querySelector("[data-say-mine]");
    const out = card.querySelector("[data-result]");
    const target = card.querySelector("[data-me]").textContent.trim();
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!sayBtn) return;
    sayBtn.addEventListener("click", () => {
      if (!SR) { out.hidden = false; out.classList.remove("hidden"); out.textContent = T("Your browser can't listen. Use Chrome, or just say it to your family!", "আপনার ব্রাউজার শুনতে পারে না। Chrome ব্যবহার করুন, অথবা পরিবারকে বলুন!"); return; }
      const rec = new SR(); rec.lang = "en-GB"; rec.interimResults = false;
      sayBtn.classList.add("mic-on");
      rec.onresult = e => {
        const heard = e.results[0][0].transcript;
        const norm = s => s.toLowerCase().replace(/[^a-z0-9' ]/g, " ").split(/\s+/).filter(Boolean);
        const want = norm(target), got = new Set(norm(heard));
        const missed = want.filter(w => !got.has(w));
        const score = Math.round((want.length - missed.length) * 100 / want.length);
        out.classList.remove("hidden");
        out.innerHTML = (score >= 70 ? "🌟 " + T("Great! ", "দারুণ! ") : "🔁 " + T("Try again. ", "আবার চেষ্টা করো। ")) +
          T("I heard: ", "শুনেছি: ") + "“" + heard.replace(/</g, "&lt;") + "” · " + score + "%" +
          (missed.length ? "<br>" + T("Say clearly: ", "স্পষ্ট করে বলো: ") + "<strong>" + missed.join(", ") + "</strong>" : "");
      };
      rec.onend = () => sayBtn.classList.remove("mic-on");
      rec.onerror = () => sayBtn.classList.remove("mic-on");
      rec.start();
    });
  });

  document.querySelectorAll("[data-toggle-bn]").forEach(b => b.addEventListener("click", () => {
    document.body.classList.toggle("hide-bn");
    try { localStorage.setItem("fe-hide-bn", document.body.classList.contains("hide-bn") ? "1" : ""); } catch (e) {}
  }));
  try { if (localStorage.getItem("fe-hide-bn")) document.body.classList.add("hide-bn"); } catch (e) {}
})();
