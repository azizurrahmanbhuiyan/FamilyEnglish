/* FamilyEnglish: speak words with the browser's own voice (no audio files, no cost).
 * Any element with data-say="text" becomes a play button.
 * Prefers a British English voice when the device has one. */
(function () {
  const synth = window.speechSynthesis;
  let voice = null;

  // Best British voices first (Chrome, Edge, Android, iPhone/Mac), then any en-GB voice.
  const GOOD_GB = ["Google UK English Female", "Google UK English Male", "Microsoft Sonia", "Microsoft Libby",
                   "Microsoft Ryan", "Microsoft Hazel", "Microsoft George", "Serena", "Daniel", "Kate", "Arthur", "Martha"];
  function pickVoice() {
    if (!synth) return;
    const voices = synth.getVoices();
    const gb = voices.filter(v => (v.lang || "").replace("_", "-").toLowerCase() === "en-gb");
    voice = GOOD_GB.map(n => gb.find(v => v.name.indexOf(n) === 0)).find(Boolean) || gb[0] ||
            voices.find(v => v.lang && v.lang.startsWith("en")) || null;
    window.feHasBritishVoice = gb.length > 0;
    document.querySelectorAll("[data-voice-note]").forEach(el => { el.hidden = gb.length > 0 || !voices.length; });
  }
  if (synth) {
    pickVoice();
    synth.onvoiceschanged = pickVoice;
  }

  window.feVoice = function () { return voice; };

  window.feSay = function (text, rate) {
    if (!synth || !text) return false;
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    if (voice) u.voice = voice;
    u.lang = voice ? voice.lang : "en-GB";
    u.rate = rate || 0.85;
    synth.speak(u);
    return true;
  };

  document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-say]");
    if (!btn) return;
    e.preventDefault();
    if (!window.feSay(btn.dataset.say, parseFloat(btn.dataset.rate || "0.85"))) {
      alert("Your browser cannot speak. Please read the word aloud for your child.");
    }
  });
})();

/* Video clip lists: pick a clip to load it into the player (never autoplays). */
document.addEventListener("click", function (e) {
  const b = e.target.closest("[data-clip-src]");
  if (!b) return;
  const box = b.closest("[data-clips]");
  const player = box.querySelector("[data-clip-player]");
  player.src = b.dataset.clipSrc; player.title = b.dataset.clipTitle;
  box.querySelectorAll("[data-clip-src]").forEach(x => x.classList.toggle("is-on", x === b));
  player.scrollIntoView({ block: "nearest", behavior: "smooth" });
});
