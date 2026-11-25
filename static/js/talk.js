/* Talk: the AI conversation page and the lesson-report practice cards.
   Uses the browser's own speech (Web Speech API): speechSynthesis to speak, SpeechRecognition to listen. */
(function () {
  var C = JSON.parse(document.getElementById('t-config').textContent);
  var csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || '';
  var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;

  function post(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }, body: JSON.stringify(body || {}) })
      .then(function (r) { return r.json(); });
  }
  function say(text, slow, done) {
    if (!window.speechSynthesis) { if (done) done(); return; }
    var u = new SpeechSynthesisUtterance(text.replace(/\(Tip:.*?\)/, ''));
    u.lang = 'en-GB'; u.rate = (C.rate || 1) * (slow ? 0.65 : 0.95); u.pitch = C.pitch || 1;
    var v = speechSynthesis.getVoices().filter(function (x) { return x.lang === 'en-GB'; })[0];
    if (v) u.voice = v;
    u.onend = function () { if (done) done(); };
    speechSynthesis.cancel(); speechSynthesis.speak(u);
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  /** Listen once. cb({text, confidence, seconds}) or cb(null). */
  function listen(onStart, cb) {
    if (!Rec) { alert('Speech recognition needs Chrome or Edge. You can type instead.'); cb(null); return null; }
    var r = new Rec(), t0 = Date.now(), got = false;
    r.lang = 'en-GB'; r.interimResults = false; r.maxAlternatives = 1;
    r.onresult = function (e) { got = true; var a = e.results[0][0]; cb({ text: a.transcript, confidence: a.confidence, seconds: Math.round((Date.now() - t0) / 1000) }); };
    r.onerror = function () { if (!got) { got = true; cb(null); } };
    r.onend = function () { if (!got) cb(null); };
    speechSynthesis && speechSynthesis.cancel();
    r.start(); onStart && onStart();
    return r;
  }

  // ------------------------------------------------------------------ conversation page
  var log = document.getElementById('t-log');
  if (log) {
    var mic = document.getElementById('t-mic'), status = document.getElementById('t-status'), turnsEl = document.getElementById('t-turns');
    var busy = false, rec = null, turns = C.messages.filter(function (m) { return m.role === 'user'; }).length;

    function showTurns() { turnsEl.textContent = turns + ' / ' + C.maxTurns + ' answers'; }
    function bubble(m, speak) {
      var row = el('div', 't-msg ' + (m.role === 'user' ? 'is-me' : 'is-bot'));
      if (m.role !== 'user') row.appendChild(el('span', 't-ava', '🐦'));
      var b = el('div', 't-bubble'); b.appendChild(el('p', '', m.content));
      if (m.tip) b.appendChild(el('p', 't-tip', '💡 ' + m.tip));
      if (m.role !== 'user') {
        var tools = el('div', 't-tools'), tr = el('p', 't-tr');
        [['🔈', function () { say(m.content); }], ['🐢', function () { say(m.content, true); }],
         ['文A', function () {
           if (tr.textContent) { tr.textContent = ''; return; }
           if (!C.aiOn) { tr.textContent = 'Translation needs AI.'; return; }
           tr.textContent = '…';
           post(C.urls.translate, { text: m.content }).then(function (d) { tr.textContent = d.text || 'Translation is not available now.'; });
         }]].forEach(function (x) { var btn = el('button', 't-tool', x[0]); btn.type = 'button'; btn.onclick = x[1]; tools.appendChild(btn); });
        b.appendChild(tools); b.appendChild(tr);
      }
      row.appendChild(b); log.appendChild(row);
      row.scrollIntoView({ behavior: 'smooth', block: 'end' });
      if (speak) say(m.content);
    }
    C.messages.forEach(function (m, i) { bubble(m, i === C.messages.length - 1 && m.role !== 'user'); });
    showTurns();

    function send(text, confidence, seconds) {
      text = (text || '').trim();
      if (!text || busy) return;
      busy = true; turns++; showTurns();
      bubble({ role: 'user', content: text });
      status.textContent = 'Your tutor is thinking…';
      post(C.urls.reply, { text: text, confidence: confidence, seconds: seconds }).then(function (d) {
        busy = false;
        if (d.reply) bubble({ role: 'assistant', content: d.reply, tip: d.tip }, true);
        status.textContent = d.done ? 'Great talk! Tap Finish to see your report.' : 'Tap the microphone and answer';
        if (d.done) document.getElementById('t-finish').classList.add('s-btn');
      }).catch(function () { busy = false; status.textContent = 'Network problem — please try again.'; });
    }

    mic.onclick = function () {
      if (rec) { rec.stop(); return; }
      rec = listen(function () { mic.classList.add('is-on'); status.textContent = 'Listening… speak now'; }, function (h) {
        rec = null; mic.classList.remove('is-on');
        if (!h || !h.text) { status.textContent = "I didn't hear you. Tap the mic and speak clearly."; return; }
        send(h.text, h.confidence, h.seconds);
      });
    };
    document.getElementById('t-kb').onclick = function () {
      var f = document.getElementById('t-typed'); f.classList.toggle('hidden'); document.getElementById('t-text').focus();
    };
    document.getElementById('t-typed').onsubmit = function (e) {
      e.preventDefault(); var i = document.getElementById('t-text'); send(i.value, null, 0); i.value = '';
    };
    document.getElementById('t-hint').onclick = function () {
      status.textContent = 'Getting a hint…';
      post(C.urls.hint).then(function (d) { status.textContent = '💡 You could say: “' + d.hint + '”'; });
    };
    document.getElementById('t-finish').onclick = function () {
      this.disabled = true; status.textContent = 'Writing your report…';
      post(C.urls.finish).then(function (d) { location.href = d.url || C.report; });
    };
  }

  // ------------------------------------------------------------------ report page: listen, save, say it
  var saved = new Set(C.saved || []);
  document.querySelectorAll('.t-say').forEach(function (card) {
    var text = card.dataset.text, score = card.querySelector('.t-say-score'), saveBtn = card.querySelector('[data-act=save]');
    if (saved.has(text.slice(0, 120))) saveBtn.classList.add('is-on');
    card.querySelector('[data-act=play]').onclick = function () { say(text); };
    saveBtn.onclick = function () {
      post(C.bookmark, { text: text }).then(function (d) { saveBtn.classList.toggle('is-on', !!d.saved); });
    };
    card.querySelector('[data-act=say]').onclick = function () {
      var b = this;
      listen(function () { b.classList.add('is-on'); score.textContent = 'Listening…'; }, function (h) {
        b.classList.remove('is-on');
        if (!h) { score.textContent = "Didn't hear you"; return; }
        post(C.practice, { target: text, said: h.text, confidence: h.confidence }).then(function (d) {
          score.textContent = d.score + '%';
          score.className = 't-say-score ' + (d.score >= 70 ? 'is-ok' : 'is-bad');
          var p = card.querySelector('.t-say-text'); p.textContent = '';
          (d.marks || []).forEach(function (m) { p.appendChild(el('span', m.ok ? 'is-ok' : 'is-bad', m.w + ' ')); });
        });
      });
    };
  });
})();
