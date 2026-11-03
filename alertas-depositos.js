/* Alerta de depósitos a prazo do Literacia Financeira.
   Formulário feito com o lf-kit do Diogo: a pessoa escolhe prazo, taxa mínima e montante e deixa o email.
   A inscrição vai para a audiência do Mailchimp (formulário público com duplo opt-in, sem chave de API no browser).
   Os emails são enviados por scripts/enviar_alertas.py depois de cada verificação dos dados.
   Requer lf-kit.css e lf-kit.js. Raiz: <div id="lf-alerta-dp"></div>. */
(function () {
  /* Dados do formulário público do Mailchimp (Audience > Signup forms > Embedded forms). Enquanto estiverem vazios,
     o formulário mostra que está em configuração e não envia nada. */
  var MC = {
    /* Público "Alertas Literacia Financeira". O f_id é obrigatório: sem ele o Mailchimp pede captcha. */
    action: "https://literaciafinanceira.us22.list-manage.com/subscribe/post?u=c9fc2d228ed8174ccf3fcd54f&id=72ded487c6&f_id=00abc3e1f0",
    grupo: "",           /* público só de alertas: não há grupos */
    honeypot: "b_c9fc2d228ed8174ccf3fcd54f_72ded487c6"
  };
  var DATA = "https://franklinsilvapt-arch.github.io/depositos-comparator/data/depositos.json";
  var PRIV = "https://www.literaciafinanceira.pt/politicas/politica-de-privacidade";

  function pct(v) { return LFK.fmt(v, { currency: false }) + "%"; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function html() {
    return '<div class="lfk"><div class="lfk-card"><div class="lfk-stack">' +
      '<div class="lfk-stack is-sm"><h2 class="lfk-h-sm">Recebe um alerta quando houver um depósito melhor</h2>' +
      '<p class="lfk-small lfk-muted">Escolhe o prazo e a taxa que procuras. Verificamos os depósitos nos dias 1 e 16 de cada mês e enviamos um email só quando houver um depósito novo que cumpra o teu critério.</p></div>' +
      '<form class="lfk-stack" id="al-form" onsubmit="return false" novalidate>' +
      '<div class="lfk-grid is-3">' +
      '<div class="lfk-field"><label class="lfk-label" for="al-prazo">Prazo</label><select class="lfk-input" id="al-prazo" name="DP_PRAZO"><option value="3">3 meses</option><option value="6">6 meses</option><option value="12" selected>12 meses</option><option value="24">24 meses</option></select></div>' +
      '<div class="lfk-field"><label class="lfk-label" for="al-taxa">TANB mínima</label><div class="lfk-input-wrap"><input class="lfk-input lfk-num" id="al-taxa" name="DP_TAXA" inputmode="decimal" value="3,00" data-max="10"><span class="lfk-unit">%</span></div></div>' +
      '<div class="lfk-field"><label class="lfk-label" for="al-mont">Montante</label><div class="lfk-input-wrap"><input class="lfk-input lfk-num" id="al-mont" name="DP_MONT" inputmode="numeric" value="10.000" data-max="10000000"><span class="lfk-unit">€</span></div></div>' +
      "</div>" +
      '<div class="lfk-field" id="al-f-email"><label class="lfk-label" for="al-email">Email</label><input class="lfk-input" id="al-email" name="EMAIL" type="email" autocomplete="email" placeholder="o.teu@email.pt"><span class="lfk-error" id="al-e-email" hidden>Escreve um email válido.</span></div>' +
      '<div class="lfk-field" id="al-f-ok"><label class="lfk-check"><input type="checkbox" id="al-ok"> <span>Quero receber por email os alertas que pedi. <small>Podes cancelar em qualquer email. Ver a <a class="lfk-link" href="' + PRIV + '" target="_blank" rel="noopener">política de privacidade</a>.</small></span></label><span class="lfk-error" id="al-e-ok" hidden>Para criar o alerta tens de aceitar receber os emails.</span></div>' +
      '<div><button type="button" class="lfk-btn" id="al-btn">Criar alerta</button></div>' +
      '<div id="al-msg"></div>' +
      "</form></div></div></div>";
  }

  function hojeCumprem(d, prazo, taxa, mont) {
    return d.depositos.filter(function (x) {
      if (x.a_confirmar || x.idade_max) return false;
      var p = x.prazos[prazo]; if (!p) return false;
      var mn = p.min != null ? p.min : (x.min || 0), mx = p.max != null ? p.max : x.max;
      return p.tanb >= taxa && mont >= mn && (mx == null || mont <= mx);
    }).sort(function (a, b) { return b.prazos[prazo].tanb - a.prazos[prazo].tanb; });
  }

  function enviar(campos) {
    /* Formulário público do Mailchimp: o endpoint post-json responde em JSONP. */
    return new Promise(function (ok, falha) {
      var cb = "lfAlerta" + Date.now();
      var url = MC.action.replace("/post?", "/post-json?") + "&c=" + cb;
      Object.keys(campos).forEach(function (k) { url += "&" + encodeURIComponent(k) + "=" + encodeURIComponent(campos[k]); });
      var s = document.createElement("script");
      var t = setTimeout(function () { limpar(); falha(new Error("tempo")); }, 15000);
      function limpar() { clearTimeout(t); delete window[cb]; if (s.parentNode) s.parentNode.removeChild(s); }
      window[cb] = function (r) { limpar(); ok(r); };
      s.src = url; s.onerror = function () { limpar(); falha(new Error("rede")); };
      document.body.appendChild(s);
    });
  }

  function iniciar() {
    var root = document.getElementById("lf-alerta-dp");
    if (!root || !window.LFK || root.getAttribute("data-pronto")) return;
    root.setAttribute("data-pronto", "1");
    root.innerHTML = html();
    LFK.selects(root);
    var dados = null;
    fetch(DATA + "?v=" + Math.floor(Date.now() / 600000)).then(function (r) { return r.json(); }).then(function (d) { dados = d; }).catch(function () {});

    var msg = document.getElementById("al-msg");
    function aviso(cls, txt) { msg.innerHTML = '<div class="lfk-alert ' + cls + '">' + txt + "</div>"; }

    document.getElementById("al-btn").addEventListener("click", function () {
      var email = document.getElementById("al-email").value.trim();
      var aceitou = document.getElementById("al-ok").checked;
      var prazo = document.getElementById("al-prazo").value;
      var taxa = LFK.num(document.getElementById("al-taxa").value);
      var mont = LFK.num(document.getElementById("al-mont").value);
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      document.getElementById("al-f-email").classList.toggle("is-error", !emailOk);
      document.getElementById("al-e-email").hidden = emailOk;
      document.getElementById("al-f-ok").classList.toggle("is-error", !aceitou);
      document.getElementById("al-e-ok").hidden = aceitou;
      if (!emailOk || !aceitou || !taxa || !mont) return;

      var hoje = "";
      if (dados) {
        var l = hojeCumprem(dados, prazo, taxa, mont);
        hoje = l.length
          ? " Hoje já há " + l.length + (l.length === 1 ? " depósito" : " depósitos") + " com este critério, o melhor é " + esc(l[0].banco) + ", " + esc(l[0].produto) + " a " + pct(l[0].prazos[prazo].tanb) + ". Vês todos no comparador."
          : " Hoje nenhum depósito cumpre este critério. Avisamos-te quando aparecer um.";
      }
      if (!MC.action) { aviso("is-warn", "<b>Em configuração:</b> o envio para o Mailchimp ainda não está ligado." + hoje); return; }

      var campos = { EMAIL: email, DP_PRAZO: prazo, DP_TAXA: String(taxa), DP_MONT: String(Math.round(mont)) };
      if (MC.grupo) campos[MC.grupo] = "1";
      if (MC.honeypot) campos[MC.honeypot] = "";
      var b = this; b.disabled = true;
      enviar(campos).then(function (r) {
        b.disabled = false;
        if (r && r.result === "success") aviso("is-ok", "<b>Falta um passo:</b> enviámos-te um email para confirmares o alerta." + hoje);
        else if (r && r.result === "redirect") {
          /* O Mailchimp pediu captcha: a inscrição acaba na página do Mailchimp, aberta pelo clique da pessoa. */
          aviso("is-warn", "<b>Falta um passo:</b> confirma que não és um robô na página do Mailchimp. " +
            '<button type="button" class="lfk-btn is-sm" id="al-mc">Concluir inscrição</button>');
          document.getElementById("al-mc").addEventListener("click", function () {
            var f = document.createElement("form");
            f.method = "post"; f.action = MC.action; f.target = "_blank"; f.style.display = "none";
            Object.keys(campos).forEach(function (k) { var i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = campos[k]; f.appendChild(i); });
            document.body.appendChild(f); f.submit(); f.parentNode.removeChild(f);
            aviso("is-ok", "<b>Quase feito:</b> depois do captcha, enviamos-te um email para confirmares o alerta." + hoje);
          });
        }
        else if (r && /already subscribed|já está/i.test(r.msg || "")) aviso("is-warn", "<b>Este email já tem um alerta.</b> Para mudares o critério, usa o link Atualizar preferências no fim de qualquer alerta que recebeste.");
        else aviso("is-err", "Não foi possível criar o alerta. Confirma o email e tenta outra vez.");
      }, function () { b.disabled = false; aviso("is-err", "Não foi possível ligar ao serviço de email. Tenta outra vez dentro de alguns minutos."); });
    });
  }
  /* O índice desenha o seu div depois de carregar os dados: nesse caso chama window.LFAlertaDP(). */
  window.LFAlertaDP = iniciar;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
