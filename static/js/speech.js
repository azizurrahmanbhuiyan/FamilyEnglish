/* FamilyEnglish: speak words with the browser's own voice (no audio files, no cost).
 * Any element with data-say="text" becomes a play button.
 * Prefers a British English voice when the device has one. */
(function () {
  const synth = window.speechSynthesis;
  let voice = null;

  function pickVoice() {
    if (!synth) return;
    const voices = synth.getVoices();
    voice = voices.find(v => v.lang === "en-GB") ||
            voices.find(v => v.lang && v.lang.startsWith("en")) || null;
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
