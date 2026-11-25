/* FamilyEnglish speaking studio player.
   Modes: repeat (say the word/phrase), convo (scripted or free conversation), grammar (chat tutor),
   speak (speech analyzer). Speech recognition uses the browser (British English); it falls back to
   typing or self-checking where the browser cannot listen. */
(function () {
  "use strict";
  var C = JSON.parse(document.getElementById("p-config").textContent);
  var LANG = C.lang || "en", I18N = C.i18n || {};
  var body = document.getElementById("p-body");
  var bar = document.getElementById("p-bar");
  var skipBtn = document.getElementById("p-skip");
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var csrf = (document.querySelector("[name=csrfmiddlewaretoken]") || {}).value || "";
  var started = Date.now();

  // ------------------------------------------------------------------ helpers
  // UI words: English and Bangla are written in the code; other languages come from the server (C.i18n).
  function t(en, bn) { return LANG === "bn" ? (bn || en) : LANG === "en" ? en : (I18N[en] || en); }
  // Lesson help text: the server already put it in the learner's language as `native`.
  function n(en, native) { return LANG === "en" ? en : (native || I18N[en] || en); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  var ICONS = document.getElementById("tpl-icons").content;
  function icon(name) { var n = ICONS.querySelector('[data-i="' + name + '"]'); return n ? n.innerHTML : ""; }
  function h(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
  function post(url, data) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrf }, body: JSON.stringify(data), credentials: "same-origin" })
      .then(function (r) { return r.json(); }).catch(function () { return {}; });
  }
  function say(text, rate) {
    if (window.feSay) return window.feSay(text, rate || 0.9);
    try { var u = new SpeechSynthesisUtterance(text); u.lang = "en-GB"; u.rate = rate || 0.9; speechSynthesis.cancel(); speechSynthesis.speak(u); return true; } catch (e) { return false; }
  }
  function sayAndWait(text, rate) {
    return new Promise(function (res) {
      if (!window.speechSynthesis) return res();
      say(text, rate);
      var waited = 0, iv = setInterval(function () { waited += 200; if ((!speechSynthesis.speaking && waited > 400) || waited > 12000) { clearInterval(iv); res(); } }, 200);
    });
  }
  function progress(i, n) { bar.style.width = Math.round(100 * i / Math.max(1, n)) + "%"; }
  function mascot(state) {
    var tpl = document.getElementById("tpl-mascot").content.cloneNode(true);
    var svg = tpl.querySelector("svg"); if (state) svg.classList.add(state);
    return svg;
  }
  function stage(state) { var s = h('<div class="p-stage"></div>'); s.appendChild(mascot(state)); return s; }
  function setMascot(state) {
    var m = body.querySelector(".p-stage .doel"); if (!m) return;
    m.classList.remove("is-talking", "is-happy", "is-sad"); if (state) m.classList.add(state);
  }
  function scoreClass(s) { return s >= 80 ? "ok" : s >= 60 ? "mid" : "bad"; }
  function wordsOf(s) { return (s || "").toLowerCase().replace(/[^a-z0-9' ]+/g, " ").trim().split(/\s+/).filter(Boolean); }

  // one-shot listening: resolves {text, confidence} or rejects with a reason
  function listenOnce() {
    return new Promise(function (resolve, reject) {
      if (!SR) return reject("unsupported");
      var r = new SR(); r.lang = "en-GB"; r.interimResults = false; r.maxAlternatives = 3;
      var got = false;
      r.onresult = function (e) {
        got = true; var best = e.results[0][0];
        var alts = []; for (var i = 0; i < e.results[0].length; i++) alts.push(e.results[0][i]);
        resolve({ text: best.transcript, confidence: best.confidence, alts: alts });
      };
      r.onerror = function (e) { if (!got) reject(e.error || "error"); };
      r.onend = function () { if (!got) reject("no-speech"); };
      try { r.start(); } catch (e) { reject("busy"); }
      listenOnce.current = r;
    });
  }
  function stopListening() { try { listenOnce.current && listenOnce.current.stop(); } catch (e) { /* ignore */ } }
  function bestAlt(res, target) {
    if (!res.alts || !target) return res;
    var tw = wordsOf(target), best = res, bestHit = -1;
    res.alts.forEach(function (a) {
      var aw = wordsOf(a.transcript), hit = 0; tw.forEach(function (w) { if (aw.indexOf(w) >= 0) hit++; });
      if (hit > bestHit) { bestHit = hit; best = { text: a.transcript, confidence: a.confidence || res.confidence }; }
    });
    return best;
  }
  function micError(reason) {
    if (reason === "not-allowed" || reason === "service-not-allowed") return t("Please allow the microphone in your browser settings.", "ব্রাউজারের সেটিংসে মাইক্রোফোন চালু করুন।");
    if (reason === "no-speech") return t("I didn't hear anything. Tap the mic and speak clearly.", "কিছু শুনতে পাইনি। মাইকে চাপ দিয়ে পরিষ্কার বলুন।");
    if (reason === "network") return t("Speech needs the internet. Check your connection.", "উচ্চারণ যাচাইয়ে ইন্টারনেট লাগে।");
    return t("Listening didn't work. Try again.", "শোনা যায়নি। আবার চেষ্টা করুন।");
  }

  // record yourself for a few seconds and play it back
  function recordSelf(btn, seconds) {
    if (!navigator.mediaDevices || !window.MediaRecorder) { alert(t("Recording is not supported in this browser.", "এই ব্রাউজারে রেকর্ড করা যায় না।")); return; }
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      var rec = new MediaRecorder(stream), chunks = [];
      rec.ondataavailable = function (e) { chunks.push(e.data); };
      rec.onstop = function () {
        stream.getTracks().forEach(function (tr) { tr.stop(); });
        btn.classList.remove("is-rec");
        var audio = new Audio(URL.createObjectURL(new Blob(chunks, { type: rec.mimeType || "audio/webm" })));
        audio.play();
      };
      btn.classList.add("is-rec"); rec.start();
      setTimeout(function () { if (rec.state !== "inactive") rec.stop(); }, (seconds || 3.5) * 1000);
    }).catch(function () { alert(micError("not-allowed")); });
  }

  // ------------------------------------------------------------------ finish screen
  function finish(score, extra) {
    progress(1, 1);
    skipBtn.hidden = true;
    score = Math.max(0, Math.min(100, Math.round(score)));
    var data = { key: C.key, title: C.title, score: score };
    if (C.unitKey) data.alsoKey = C.unitKey;
    body.innerHTML = "";
    var wrap = h('<div class="p-done"></div>');
    wrap.appendChild(mascot(score >= 70 ? "is-happy" : ""));
    wrap.appendChild(h('<p class="p-big">' + score + '%</p>'));
    wrap.appendChild(h('<p class="text-xl font-extrabold">' + (score >= 90 ? t("Excellent!", "অসাধারণ!") : score >= 70 ? t("Well done!", "খুব ভালো!") : t("Good effort — practise once more!", "ভালো চেষ্টা — আরেকবার অনুশীলন করুন!")) + '</p>'));
    var rewards = h('<div class="p-rewards"><span>…</span></div>');
    wrap.appendChild(rewards);
    if (extra) wrap.appendChild(extra);
    wrap.appendChild(h('<div class="grid w-full max-w-sm gap-3 mt-2">' +
      (C.next ? '<a class="s-btn is-block" href="' + esc(C.next) + '">' + t("Next: practise the words", "এবার শব্দগুলো অনুশীলন") + ' →</a>' : "") +
      '<a class="' + (C.next ? "s-btn-ghost" : "s-btn is-block") + '" href="' + esc(C.back) + '">' + t("Continue", "চালিয়ে যান") + '</a>' +
      '<button type="button" class="s-btn-ghost" onclick="location.reload()">' + icon("retry") + " " + t("Practise again", "আবার অনুশীলন") + '</button></div>'));
    body.appendChild(wrap);
    post(C.finishUrl, data).then(function (r) {
      rewards.innerHTML = r && r.first ? '<span>⚡ +' + r.xp + ' XP</span><span>' + icon("gem") + ' +' + r.gemsEarned + '</span>'
        : '<span>' + t("Best", "সেরা") + ': ' + (r && r.score != null ? r.score : score) + '%</span>';
    });
  }

  // ------------------------------------------------------------------ REPEAT mode
  function runRepeat() {
    var items = C.items || [], i = 0, scores = [], skips = 3, advanced = !!C.advancedDefault, tries = 0, best = 0;
    var saved = {};
    skipBtn.hidden = false;
    function updSkip() { skipBtn.textContent = "SKIP " + skips; skipBtn.disabled = skips <= 0; }
    updSkip();
    skipBtn.onclick = function () { if (skips <= 0) return; skips--; updSkip(); scores.push(null); next(); };
    function threshold() { return advanced ? 85 : 70; }
    function wordHtml(it, marks) {
      if (marks && marks.length) {
        return marks.map(function (m) { return '<span class="' + (m.ok ? "ok" : "bad") + '">' + esc(m.w) + "</span>"; }).join(" ");
      }
      if (it.target) return esc(it.before) + "<u>" + esc(it.target) + "</u>" + esc(it.after);
      return esc(it.text);
    }
    function render(result) {
      var it = items[i];
      progress(i, items.length);
      body.innerHTML = "";
      body.appendChild(stage(result ? (result.ok ? "is-happy" : "is-sad") : ""));
      var mode = h('<div class="p-mode"><button type="button" data-m="0" class="' + (advanced ? "" : "is-on") + '">' + t("Regular", "সাধারণ") +
        '</button><button type="button" data-m="1" class="' + (advanced ? "is-on" : "") + '">' + t("Advanced", "উন্নত") + "</button></div>");
      mode.onclick = function (e) { var b = e.target.closest("button"); if (!b) return; advanced = b.dataset.m === "1"; render(result); };
      body.appendChild(mode);
      var long = it.text.split(" ").length > 3;
      var card = h('<div class="p-card"></div>');
      if (result) {
        card.appendChild(h('<div class="p-result ' + (result.ok ? "is-ok" : "is-bad") + '">' + icon(result.ok ? "ok" : "x") + " " +
          (result.ok ? t("Correct", "সঠিক") : t("Try again", "আবার চেষ্টা করুন")) + '<span class="p-score">' + result.score + "%</span></div>"));
        if (!result.ok) card.appendChild(h('<p class="p-tip">' + esc(n(it.tip_en, it.tip_bn)) + "</p>"));
        if (result.heard) card.appendChild(h('<p class="p-tip"><b>' + t("I heard", "শুনেছি") + ':</b> “' + esc(result.heard) + '”</p>'));
      } else {
        card.appendChild(h('<span class="p-label">' + (it.target ? t("Single sound feedback", "একক ধ্বনি ফিডব্যাক") : t("Sentence feedback", "বাক্য ফিডব্যাক")) + "</span>"));
        card.appendChild(h('<p class="p-help">' + (it.target ? t("Speak and get feedback on the underlined sound.", "বলুন, দাগ দেওয়া ধ্বনির ওপর ফিডব্যাক পাবেন।")
          : t("Listen, then say the whole sentence clearly.", "শুনুন, তারপর পুরো বাক্যটি পরিষ্কার বলুন।")) +
          (!it.target && it.sound && it.sound !== "stress" ? " " + t("Focus sound", "লক্ষ্য ধ্বনি") + ": <b>/" + esc(it.sound) + "/</b>" : "") + "</p>"));
      }
      card.appendChild(h('<div class="p-word' + (long ? " is-long" : "") + '">' + wordHtml(it, result && result.marks) + "</div>"));
      if (it.ipa) card.appendChild(h('<div class="p-ipa">' + esc(it.ipa) + "</div>"));
      if (it.bn) card.appendChild(h('<div class="p-bn">' + esc(it.bn) + "</div>"));
      var tools = h('<div class="p-tools"></div>');
      var bNormal = h('<button type="button" title="' + t("Listen", "শুনুন") + '">' + icon("volume") + "</button>");
      var bSlow = h('<button type="button" title="' + t("Listen slowly", "ধীরে শুনুন") + '">' + icon("snail") + "</button>");
      var bMark = h('<button type="button" title="' + t("Save to My Words", "আমার শব্দে রাখুন") + '" class="' + (saved[it.text] ? "is-on" : "") + '">' + icon("bookmark") + "</button>");
      var bSelf = h('<button type="button" title="' + t("Record and hear yourself", "রেকর্ড করে নিজেকে শুনুন") + '">' + icon("self") + "</button>");
      var bInfo = h('<button type="button" class="p-info" title="' + t("How to say it", "কীভাবে বলবেন") + '">' + icon("info") + "</button>");
      bNormal.onclick = function () { say(it.text, 0.9); };
      bSlow.onclick = function () { say(it.text, 0.55); };
      bMark.onclick = function () { post(C.bookmarkUrl, { text: it.text, ipa: it.ipa, bn: it.bn }).then(function (r) { saved[it.text] = r.saved; bMark.classList.toggle("is-on", !!r.saved); }); };
      bSelf.onclick = function () { recordSelf(bSelf, Math.min(6, 1.5 + it.text.split(" ").length * 0.6)); };
      bInfo.onclick = function () { alert(n(it.tip_en, it.tip_bn)); };
      [bNormal, bSlow, bMark, bSelf, bInfo].forEach(function (b) { tools.appendChild(b); });
      card.appendChild(tools);
      body.appendChild(card);
      var foot = h('<div class="p-foot"></div>');
      if (result) {
        if (result.ok) {
          foot.appendChild(h('<button type="button" class="s-btn is-block">' + t("Continue", "চালিয়ে যান") + " " + icon("arrow") + "</button>"));
          foot.lastChild.onclick = function () { scores.push(best); next(); };
        } else {
          var row = h('<div class="p-row"><button type="button" class="s-btn">' + t("Retry", "আবার") + " " + icon("retry") + '</button><button type="button" class="s-btn-ghost">' + t("Skip", "বাদ দিন") + " " + icon("skip") + "</button></div>");
          row.children[0].onclick = function () { render(null); };
          row.children[1].onclick = function () { scores.push(best); next(); };
          foot.appendChild(row);
        }
      } else if (SR) {
        foot.appendChild(h('<p class="p-hint">' + t("Tap to speak", "বলতে চাপ দিন") + "</p>"));
        var mic = h('<button type="button" class="p-mic" aria-label="Speak">' + icon("mic") + "</button>");
        mic.onclick = function () { doListen(mic); };
        foot.appendChild(mic);
      } else {
        foot.appendChild(h('<p class="p-hint text-center">' + t("Say it aloud, then check yourself:", "জোরে বলুন, তারপর নিজেই যাচাই করুন:") + "</p>"));
        var row2 = h('<div class="p-row"><button type="button" class="s-btn">' + t("I said it well", "ঠিকভাবে বলেছি") + '</button><button type="button" class="s-btn-ghost">' + t("Next", "পরের") + "</button></div>");
        row2.children[0].onclick = function () { send(it, "", null, 75); };
        row2.children[1].onclick = function () { scores.push(best || 50); next(); };
        foot.appendChild(row2);
        foot.appendChild(h('<p class="text-xs s-muted text-center">' + t("Tip: use Google Chrome on Android or a computer for automatic speech checking.", "স্বয়ংক্রিয় যাচাইয়ের জন্য Android বা কম্পিউটারে Google Chrome ব্যবহার করুন।") + "</p>"));
      }
      body.appendChild(foot);
      if (!result && tries === 0) setTimeout(function () { say(it.text, 0.9); }, 250);
    }
    function doListen(mic) {
      var it = items[i];
      mic.classList.add("is-listening"); mic.innerHTML = icon("stop");
      mic.onclick = function () { stopListening(); };
      var t0 = Date.now();
      listenOnce().then(function (res) {
        res = bestAlt(res, it.text);
        send(it, res.text, res.confidence, null, (Date.now() - t0) / 1000);
      }).catch(function (reason) {
        mic.classList.remove("is-listening"); mic.innerHTML = icon("mic"); mic.onclick = function () { doListen(mic); };
        var p = body.querySelector(".p-hint"); if (p) p.textContent = micError(reason);
      });
    }
    function send(it, said, conf, selfScore, secs) {
      tries++;
      post(C.attemptUrl, { kind: "repeat", key: C.key, target: it.text, said: said, confidence: conf, score: selfScore, seconds: Math.round(secs || 4) }).then(function (r) {
        var score = r.score != null ? r.score : (selfScore || 0);
        best = Math.max(best, score);
        render({ ok: score >= threshold(), score: score, marks: r.marks, heard: said });
      });
    }
    function next() {
      i++; tries = 0; best = 0;
      if (i >= items.length) {
        var done = scores.map(function (s) { return s == null ? 50 : s; });
        return finish(done.reduce(function (a, b) { return a + b; }, 0) / Math.max(1, done.length));
      }
      render(null);
    }
    if (!items.length) { body.innerHTML = '<p class="mt-8 text-center">' + t("Nothing to practise here yet.", "এখানে এখনো কিছু নেই।") + "</p>"; return; }
    render(null);
  }

  // ------------------------------------------------------------------ CONVO mode
  function runConvo() {
    var lines = C.lines || [], i = 0, scores = [], advanced = false, freeMode = !!C.aiOn, history = [], turns = 0;
    body.innerHTML = "";
    body.appendChild(stage(""));
    var mode = h('<div class="p-mode"><button type="button" data-m="0" class="is-on">' + t("Regular", "সাধারণ") + '</button><button type="button" data-m="1">' + t("Advanced", "উন্নত") + "</button></div>");
    mode.onclick = function (e) {
      var b = e.target.closest("button"); if (!b) return;
      advanced = b.dataset.m === "1"; mode.querySelectorAll("button").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      var cue = chat.querySelector(".p-cue:last-child"); if (cue && lines[i]) cue.outerHTML = cueHtml(lines[i]);
    };
    if (!freeMode) body.appendChild(mode);
    var chat = h('<div class="p-chat"></div>');
    body.appendChild(chat);
    var foot = h('<div class="p-foot"></div>');
    body.appendChild(foot);
    if (C.setting) chat.appendChild(h('<p class="text-center text-sm s-muted">' + esc(C.setting) + (C.persona ? " · " + t("Coach", "কোচ") + ": " + esc(C.persona) : "") + "</p>"));

    function scroll() { window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }); }
    function bot(text) {
      var b = h('<div class="p-bub is-bot">' + esc(text) + ' <button type="button" class="say" aria-label="Listen">' + icon("volume") + "</button></div>");
      b.querySelector(".say").onclick = function () { say(text); };
      chat.appendChild(b); scroll(); setMascot("is-talking");
      return sayAndWait(text).then(function () { setMascot(""); });
    }
    function cueHtml(line) {
      if (advanced) return '<div class="p-bub is-me p-cue" style="opacity:.75"><i>' + t("Answer in your own words", "নিজের ভাষায় উত্তর দিন") + "</i>" +
        (line.hint ? '<span class="hint">💡 ' + esc(line.hint) + "</span>" : "") + '<span class="hint">' + t("Example", "উদাহরণ") + ": " + esc(line.reply) + "</span></div>";
      return '<div class="p-bub is-me p-cue" style="opacity:.8">' + esc(line.reply) + "</div>";
    }
    function askUser(line) {
      if (line) chat.appendChild(h(cueHtml(line)));
      scroll();
      foot.innerHTML = "";
      if (SR) {
        foot.appendChild(h('<p class="p-hint">' + t("Tap to speak", "বলতে চাপ দিন") + "</p>"));
        var row = h('<div class="flex items-center gap-4"></div>');
        var mic = h('<button type="button" class="p-mic">' + icon("mic") + "</button>");
        var kb = h('<button type="button" class="p-kbd" title="' + t("Type instead", "টাইপ করুন") + '">' + icon("kbd") + "</button>");
        mic.onclick = function () {
          mic.classList.add("is-listening"); mic.innerHTML = icon("stop"); mic.onclick = stopListening;
          listenOnce().then(function (res) { answered(line, line ? bestAlt(res, line.reply).text : res.text, res.confidence); })
            .catch(function (reason) { foot.querySelector(".p-hint").textContent = micError(reason); mic.classList.remove("is-listening"); mic.innerHTML = icon("mic"); mic.onclick = function () { askUser(null); }; });
        };
        kb.onclick = function () { typeBox(line); };
        row.appendChild(mic); row.appendChild(kb); foot.appendChild(row);
        if (freeMode) { var end = h('<button type="button" class="s-btn-ghost mt-2">' + t("Finish conversation", "কথোপকথন শেষ") + "</button>"); end.onclick = endConvo; foot.appendChild(end); }
      } else typeBox(line);
    }
    function typeBox(line) {
      foot.innerHTML = "";
      var f = h('<form class="p-type"><input type="text" autocomplete="off" placeholder="' + t("Type your answer…", "উত্তর লিখুন…") + '"><button class="s-btn">' + icon("arrow") + "</button></form>");
      f.onsubmit = function (e) { e.preventDefault(); var v = f.querySelector("input").value.trim(); if (v) answered(line, v, null); };
      foot.appendChild(f); f.querySelector("input").focus();
      if (freeMode) { var end = h('<button type="button" class="s-btn-ghost mt-2">' + t("Finish conversation", "কথোপকথন শেষ") + "</button>"); end.onclick = endConvo; foot.appendChild(end); }
    }
    function answered(line, said, conf) {
      var cue = chat.querySelector(".p-cue"); if (cue) cue.remove();
      var me = h('<div class="p-bub is-me">' + esc(said) + '<div class="pct">…</div></div>');
      chat.appendChild(me); scroll(); foot.innerHTML = "";
      if (freeMode) {
        var n = wordsOf(said).length, sc = Math.min(95, 50 + n * 5);
        me.querySelector(".pct").innerHTML = '<span></span><b class="' + scoreClass(sc) + '">' + sc + "%</b>";
        scores.push(sc); turns++; history.push({ role: "user", content: said });
        var typing = h('<div class="p-bub is-bot p-typing"><i></i><i></i><i></i></div>'); chat.appendChild(typing); scroll();
        post(C.replyUrl, { coach: C.coach, scenario: C.scenario, history: history }).then(function (r) {
          typing.remove();
          if (!r.reply) { freeMode = false; return bot(t("Let's continue with the practice script.", "চলুন অনুশীলনের স্ক্রিপ্টে ফিরি।")).then(nextLine); }
          history.push({ role: "assistant", content: r.reply });
          bot(r.reply).then(function () { if (turns >= 8) endConvo(); else askUser(null); });
        });
        return;
      }
      post(C.attemptUrl, { kind: "convo", key: C.key, target: line.reply, said: said, confidence: conf, free: advanced, seconds: 6 }).then(function (r) {
        me.querySelector(".pct").innerHTML = '<button type="button" class="say">' + icon("volume") + '</button><b class="' + scoreClass(r.score) + '">' + r.score + "%</b>";
        me.querySelector(".say").onclick = function () { say(line.reply); };
        scores.push(r.score);
        if (r.score < 60 && !advanced) {
          foot.innerHTML = "";
          var row = h('<div class="p-row"><button type="button" class="s-btn">' + t("Retry", "আবার") + " " + icon("retry") + '</button><button type="button" class="s-btn-ghost">' + t("Next", "পরের") + " " + icon("skip") + "</button></div>");
          row.children[0].onclick = function () { scores.pop(); me.remove(); askUser(line); };
          row.children[1].onclick = function () { i++; nextLine(); };
          foot.appendChild(row);
        } else { i++; setTimeout(nextLine, 500); }
      });
    }
    function nextLine() {
      progress(i, lines.length);
      if (i >= lines.length) return endConvo();
      bot(lines[i].bot).then(function () { askUser(lines[i]); });
    }
    function endConvo() {
      var avg = scores.length ? scores.reduce(function (a, b) { return a + b; }, 0) / scores.length : 0;
      finish(avg);
    }
    if (freeMode) {
      var first = lines[0] ? lines[0].bot : t("Hello! Let's talk.", "হ্যালো! চলুন কথা বলি।");
      history.push({ role: "assistant", content: first });
      bot(first).then(function () { askUser(null); });
    } else nextLine();
  }

  // ------------------------------------------------------------------ GRAMMAR mode (chat tutor)
  function runGrammar() {
    var L = C.lesson, scores = [], step = 0, pi = 0;
    body.innerHTML = "";
    body.appendChild(stage(""));
    var chat = h('<div class="p-chat"></div>'); body.appendChild(chat);
    var foot = h('<div class="p-foot"></div>'); body.appendChild(foot);
    var total = 3 + L.practice.length;
    function scroll() { window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }); }
    function bot(html, speakText) {
      var typing = h('<div class="p-bub is-bot p-typing"><i></i><i></i><i></i></div>'); chat.appendChild(typing); scroll();
      return new Promise(function (res) {
        setTimeout(function () {
          typing.remove();
          var b = h('<div class="p-bub is-bot">' + html + "</div>"); chat.appendChild(b); scroll();
          if (speakText) { setMascot("is-talking"); sayAndWait(speakText).then(function () { setMascot(""); }); }
          res(b);
        }, 650);
      });
    }
    function cont(label, fn) {
      foot.innerHTML = "";
      var b = h('<button type="button" class="s-btn is-block">' + label + " " + icon("arrow") + "</button>");
      b.onclick = function () { foot.innerHTML = ""; fn(); };
      foot.appendChild(b);
    }
    function formula() {
      return '<div class="p-formula on-light">' + L.formula.map(function (f) { return '<span class="' + f.cls + '">' + esc(f.text) + "</span>"; }).join('<span style="border:0">+</span>') + "</div>";
    }
    function intro() {
      progress(0, total);
      bot(esc(L.hello[0]) + '<span class="bn">' + esc(L.hello[1]) + "</span>", L.hello[0]).then(function () { cont(t("Ready!", "প্রস্তুত!"), rule); });
    }
    function rule() {
      progress(1, total);
      bot("<b>" + t("Here's the pattern:", "গঠনটা এরকম:") + "</b>" + formula() + esc(L.rule[0]) + '<span class="bn">' + esc(L.rule[1]) + "</span>").then(function () { cont(t("Show me examples", "উদাহরণ দেখাও"), examples); });
    }
    function examples() {
      progress(2, total);
      var html = "<b>" + t("Examples — tap to listen:", "উদাহরণ — শুনতে চাপ দিন:") + "</b>" + L.examples.map(function (e) {
        return '<span class="p-ex"><button type="button" class="say" data-say="' + esc(e[0]) + '">' + icon("volume") + "</button> " + esc(e[0]) + '<span class="bn">' + esc(e[1]) + "</span></span>";
      }).join("");
      bot(html).then(function () { cont(t("Let's practise", "অনুশীলন করি"), practice); });
    }
    function practice() {
      progress(3 + pi, total);
      if (pi >= L.practice.length) {
        var avg = scores.reduce(function (a, b) { return a + b; }, 0) / Math.max(1, scores.length);
        return bot(t("Great work! You finished the lesson.", "দারুণ! পাঠটি শেষ করেছেন।"), "Great work!").then(function () { setTimeout(function () { finish(avg); }, 700); });
      }
      var p = L.practice[pi];
      var label = { fill: t("Fill the gap:", "শূন্যস্থান পূরণ করুন:"), fix: t("Correct the mistake:", "ভুলটি ঠিক করুন:"), say: t("Say this sentence:", "এই বাক্যটি বলুন:"), make: t("Your turn:", "আপনার পালা:") }[p.type];
      var extra = p.type === "say" ? ' <button type="button" class="say" data-say="' + esc(p.prompt) + '">' + icon("volume") + "</button>" : "";
      bot("<b>" + (pi + 1) + "/" + L.practice.length + " · " + label + "</b><br>" + esc(p.prompt) + extra, p.type === "say" ? p.prompt : null).then(function () { answerBox(p); });
    }
    function answerBox(p) {
      foot.innerHTML = "";
      var f = h('<form class="p-type"><input type="text" autocomplete="off" autocapitalize="off" placeholder="' + (p.type === "fill" ? t("Type the missing word(s)…", "বাদ পড়া শব্দ লিখুন…") : t("Type or tap the mic…", "লিখুন বা মাইকে চাপ দিন…")) + '"><button class="s-btn">' + icon("arrow") + "</button></form>");
      f.onsubmit = function (e) { e.preventDefault(); var v = f.querySelector("input").value.trim(); if (v) check(p, v, null); };
      if (p.type === "say" && SR) {
        foot.appendChild(h('<p class="p-hint">' + t("Tap to speak", "বলতে চাপ দিন") + "</p>"));
        var mic = h('<button type="button" class="p-mic">' + icon("mic") + "</button>");
        mic.onclick = function () {
          mic.classList.add("is-listening"); mic.innerHTML = icon("stop"); mic.onclick = stopListening;
          listenOnce().then(function (r) { r = bestAlt(r, p.prompt); check(p, r.text, r.confidence); })
            .catch(function (reason) { foot.querySelector(".p-hint").textContent = micError(reason); answerBox(p); });
        };
        foot.appendChild(mic);
        var kb = h('<button type="button" class="p-kbd">' + icon("kbd") + "</button>"); kb.onclick = function () { foot.innerHTML = ""; foot.appendChild(f); f.querySelector("input").focus(); };
        foot.appendChild(kb);
        return;
      }
      if (p.type === "make" && SR) {
        var m2 = h('<button type="button" class="p-kbd" title="Speak">' + icon("mic") + "</button>");
        m2.onclick = function () { m2.classList.add("is-rec"); listenOnce().then(function (r) { f.querySelector("input").value = r.text; m2.classList.remove("is-rec"); }).catch(function () { m2.classList.remove("is-rec"); }); };
        f.insertBefore(m2, f.firstChild);
      }
      foot.appendChild(f); f.querySelector("input").focus();
    }
    function check(p, answer, conf) {
      foot.innerHTML = "";
      chat.appendChild(h('<div class="p-bub is-me">' + esc(answer) + "</div>")); scroll();
      post(C.checkUrl, { lesson: L.slug, index: pi, answer: answer, confidence: conf, seconds: 10 }).then(function (r) {
        scores.push(r.score || 0);
        var msg = r.ok ? "✅ <b>" + t(["Spot on!", "Correct!", "Nice one!", "That's right!"][pi % 4], "সঠিক!") + "</b>"
          : "❌ <b>" + t("Not quite.", "পুরোপুরি ঠিক হয়নি।") + "</b>" + (r.right ? "<br>" + t("Answer", "উত্তর") + ": <b>" + esc(r.right) + "</b>" : "");
        if (p.type === "say") msg = '<div class="pct"><span>' + (r.ok ? "✅" : "🔁") + '</span><b class="' + scoreClass(r.score) + '">' + r.score + "%</b></div>";
        if (p.type === "make") msg = r.ok ? "✅ <b>" + t("Good sentence — it uses the pattern.", "ভালো বাক্য — গঠনটি ব্যবহার করেছেন।") + "</b>" : "🔁 <b>" + t("Try to use the pattern from this lesson.", "এই পাঠের গঠনটি ব্যবহার করার চেষ্টা করুন।") + "</b>";
        if (r.ai) msg += '<span class="bn" style="color:#3b3f72">' + esc(r.ai) + "</span>";
        bot(msg).then(function () {
          if (!r.ok && (p.type === "make" || p.type === "say")) {
            foot.innerHTML = "";
            var row = h('<div class="p-row"><button type="button" class="s-btn">' + t("Try again", "আবার") + '</button><button type="button" class="s-btn-ghost">' + t("Next", "পরের") + "</button></div>");
            row.children[0].onclick = function () { scores.pop(); answerBox(p); };
            row.children[1].onclick = function () { pi++; practice(); };
            foot.appendChild(row);
          } else cont(t("Next", "পরের"), function () { pi++; practice(); });
        });
      });
    }
    intro();
  }

  // ------------------------------------------------------------------ SPEAK mode (speech analyzer)
  function runSpeak() {
    var transcript = "", t0 = 0, timer = null, rec = null, listening = false, limit = C.seconds || 60;
    body.innerHTML = "";
    var top = h('<div class="s-card is-pad mt-4"></div>');
    top.appendChild(h('<p class="s-eyebrow">' + (C.ielts ? "IELTS · Part " + C.part : t("Speak freely", "মুক্তভাবে বলুন")) + "</p>"));
    top.appendChild(h('<p class="mt-2 text-xl font-extrabold">' + esc(C.prompt) + ' <button type="button" class="text-sky-300" data-say="' + esc(C.prompt) + '">' + icon("volume") + "</button></p>"));
    if (C.promptBn) top.appendChild(h('<p class="mt-1 font-bn s-sub">' + esc(C.promptBn) + "</p>"));
    if (C.questions && C.questions.length > 1) top.appendChild(h('<ul class="mt-3 list-disc pl-5 s-sub">' + C.questions.slice(1).map(function (q) { return "<li>" + esc(q) + "</li>"; }).join("") + "</ul>"));
    if (C.prompts) {
      var sel = h('<select class="mt-3 w-full p-2">' + C.prompts.map(function (p, k) { return '<option value="' + k + '"' + (k === C.promptIndex ? " selected" : "") + ">" + esc(p) + "</option>"; }).join("") + "</select>");
      sel.onchange = function () { location.search = "?p=" + sel.value; };
      top.appendChild(sel);
    }
    top.appendChild(h('<p class="mt-3 text-sm s-muted">' + t("Aim for", "লক্ষ্য") + " " + (C.minWords || 40) + "+ " + t("words · up to", "শব্দ · সর্বোচ্চ") + " " + limit + " " + t("seconds", "সেকেন্ড") + "</p>"));
    body.appendChild(top);
    var live = h('<div class="p-live mt-4">' + t("Your words will appear here as you speak…", "বলার সাথে সাথে আপনার কথা এখানে দেখা যাবে…") + "</div>");
    var clock = h('<p class="p-timer text-center mt-4">0:00</p>');
    body.appendChild(clock); body.appendChild(live);
    var foot = h('<div class="p-foot"></div>'); body.appendChild(foot);
    var out = h('<div class="mt-4"></div>'); body.appendChild(out);
    if (C.history && C.history.length) {
      body.appendChild(h('<div class="s-card is-pad mt-4"><p class="s-eyebrow">' + t("Your last tries", "আগের চেষ্টা") + '</p><div class="mt-2 grid gap-1 text-sm">' +
        C.history.map(function (x) { return '<div class="flex justify-between"><span>' + esc(x.when) + "</span><span>" + x.wpm + " wpm · <b>" + x.score + "%</b></span></div>"; }).join("") + "</div></div>"));
    }
    function fmt(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
    function prep() {
      if (!C.prep) return ready();
      var left = C.prep;
      foot.innerHTML = '<p class="p-hint">' + t("Prepare your answer", "উত্তর প্রস্তুত করুন") + "</p>";
      var skip = h('<button type="button" class="s-btn-ghost">' + t("Start speaking now", "এখনই বলা শুরু") + "</button>");
      foot.appendChild(h('<textarea rows="3" class="w-full p-3" placeholder="' + t("Notes (only for you)", "নোট (শুধু আপনার জন্য)") + '"></textarea>'));
      foot.appendChild(skip);
      clock.textContent = fmt(left);
      var iv = setInterval(function () { left--; clock.textContent = fmt(left); if (left <= 0) { clearInterval(iv); ready(); } }, 1000);
      skip.onclick = function () { clearInterval(iv); ready(); };
    }
    function ready() {
      clock.textContent = "0:00";
      foot.innerHTML = "";
      if (SR) {
        foot.appendChild(h('<p class="p-hint">' + t("Tap to start", "শুরু করতে চাপ দিন") + "</p>"));
        var mic = h('<button type="button" class="p-mic">' + icon("mic") + "</button>");
        mic.onclick = function () { listening ? stop() : start(mic); };
        foot.appendChild(mic);
      } else {
        var ta = h('<textarea rows="6" class="w-full p-3" placeholder="' + t("Your browser cannot listen. Type your answer here instead.", "আপনার ব্রাউজার শুনতে পারে না। এখানে উত্তর লিখুন।") + '"></textarea>');
        var go = h('<button type="button" class="s-btn is-block">' + t("Check my answer", "উত্তর যাচাই করুন") + "</button>");
        var tStart = Date.now();
        go.onclick = function () { transcript = ta.value; analyse(Math.max(20, (Date.now() - tStart) / 1000)); };
        foot.appendChild(ta); foot.appendChild(go);
      }
    }
    function start(mic) {
      transcript = ""; listening = true; t0 = Date.now();
      mic.classList.add("is-listening"); mic.innerHTML = icon("stop");
      foot.querySelector(".p-hint").textContent = t("Listening… tap to stop", "শুনছি… থামাতে চাপ দিন");
      var finalText = "";
      rec = new SR(); rec.lang = "en-GB"; rec.continuous = true; rec.interimResults = true;
      rec.onresult = function (e) {
        var interim = "";
        for (var k = e.resultIndex; k < e.results.length; k++) {
          if (e.results[k].isFinal) finalText += e.results[k][0].transcript + " "; else interim += e.results[k][0].transcript;
        }
        transcript = finalText; live.textContent = (finalText + interim).trim();
      };
      rec.onend = function () { if (listening) { try { rec.start(); } catch (e) { stop(); } } };
      rec.onerror = function (e) { if (e.error === "not-allowed") { listening = false; live.textContent = micError("not-allowed"); } };
      try { rec.start(); } catch (e) { /* ignore */ }
      timer = setInterval(function () {
        var s = (Date.now() - t0) / 1000; clock.textContent = fmt(s);
        if (s >= limit) stop();
      }, 250);
    }
    function stop() {
      listening = false; clearInterval(timer);
      try { rec && rec.stop(); } catch (e) { /* ignore */ }
      var secs = (Date.now() - t0) / 1000;
      setTimeout(function () { analyse(secs); }, 700);
    }
    function analyse(secs) {
      foot.innerHTML = '<p class="p-hint">' + t("Analysing…", "বিশ্লেষণ করছি…") + "</p>";
      var said = (transcript || live.textContent || "").trim();
      post(C.analyseUrl, { key: C.key, transcript: said, seconds: Math.round(secs), targetWpm: C.targetWpm, minWords: C.minWords, ielts: !!C.ielts, prompt: C.prompt }).then(function (r) {
        foot.innerHTML = "";
        out.innerHTML = "";
        var card = h('<div class="s-card is-pad"></div>');
        card.appendChild(h('<div class="flex items-center gap-4"><p class="p-big !text-5xl">' + r.overall + '%</p><div><p class="font-extrabold text-lg">' +
          (C.ielts ? t("Estimated band", "আনুমানিক ব্যান্ড") + " " + r.band : t("Speaking score", "বলার স্কোর")) + '</p><p class="s-muted text-sm">' + r.words + " " + t("words", "শব্দ") + " · " + r.seconds + "s</p></div></div>"));
        card.appendChild(h('<div class="p-metrics mt-4">' +
          '<div class="p-metric"><b>' + r.wpm + "</b><span>" + t("words / min", "শব্দ/মিনিট") + "</span></div>" +
          '<div class="p-metric"><b>' + r.fillers + "</b><span>" + t("fillers (um, like)", "অপ্রয়োজনীয় শব্দ") + "</span></div>" +
          '<div class="p-metric"><b>' + r.unique + "%</b><span>" + t("different words", "ভিন্ন শব্দ") + "</span></div>" +
          '<div class="p-metric"><b>' + r.linkers.length + "</b><span>" + t("linking words", "সংযোজক শব্দ") + "</span></div></div>"));
        [["fluency", t("Fluency", "সাবলীলতা")], ["vocab", t("Vocabulary range", "শব্দভান্ডার")], ["grammar", t("Linking & grammar range", "সংযোগ ও ব্যাকরণ")], ["length", t("Length", "দৈর্ঘ্য")]].forEach(function (m) {
          card.appendChild(h('<div class="mt-3"><div class="flex justify-between text-sm font-bold"><span>' + m[1] + "</span><span>" + r[m[0]] + '%</span></div><div class="s-bar is-thin mt-1"><i style="width:' + r[m[0]] + '%"></i></div></div>'));
        });
        card.appendChild(h('<ul class="mt-4 grid gap-2">' + r.tips.map(function (tp) { return "<li>💡 " + esc(n(tp[0], tp[1])) + "</li>"; }).join("") + "</ul>"));
        if (r.linkers.length) card.appendChild(h('<p class="mt-3 text-sm s-muted">' + t("Linkers you used", "ব্যবহৃত সংযোজক") + ": " + r.linkers.map(esc).join(", ") + "</p>"));
        if (r.ai) card.appendChild(h('<div class="mt-4 rounded-2xl p-4" style="background:rgba(70,168,255,.12);white-space:pre-line"><b>' + t("Coach feedback", "কোচের মতামত") + "</b>\n" + esc(r.ai) + "</div>"));
        out.appendChild(card);
        var row = h('<div class="p-row mt-4"><button type="button" class="s-btn">' + t("Finish", "শেষ করুন") + '</button><button type="button" class="s-btn-ghost">' + t("Try again", "আবার") + "</button></div>");
        row.children[0].onclick = function () { finish(r.overall); };
        row.children[1].onclick = function () { out.innerHTML = ""; live.textContent = ""; ready(); };
        out.appendChild(row);
        out.scrollIntoView({ behavior: "smooth" });
      });
    }
    progress(0, 1);
    prep();
  }

  ({ repeat: runRepeat, convo: runConvo, grammar: runGrammar, speak: runSpeak }[C.mode] || runRepeat)();
})();
