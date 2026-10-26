/* Alertas por email do Literacia Financeira (depósitos, eletricidade, Euribor e corretoras).
   Formulário feito com o lf-kit do Diogo. A inscrição vai para o público "Alertas Literacia Financeira" no Mailchimp
   pelo formulário público (duplo opt-in, sem chave de API no browser). Os emails são enviados por scripts/enviar_alertas.py.

   Onde aparece:
   - se a página tiver <div id="lf-alerta-dp"> ou <div id="lf-alerta-el"> (páginas dos índices), desenha lá;
   - senão, nos comparadores, junta um bloco no fim da secção da ferramenta.
   O tipo de alerta sai do caminho da página (TIPO_POR_PAGINA) ou de data-tipo no div.
   Requer lf-kit.css e lf-kit.js (se não estiverem na página, carrega-os). */
(function () {
  var MC = {
    /* O f_id é obrigatório: sem ele o Mailchimp pede captcha logo no primeiro pedido. */
    action: "https://literaciafinanceira.us22.list-manage.com/subscribe/post?u=c9fc2d228ed8174ccf3fcd54f&id=72ded487c6&f_id=00abc3e1f0",
    honeypot: "b_c9fc2d228ed8174ccf3fcd54f_72ded487c6"
  };
  var KIT = "https://cdn.jsdelivr.net/gh/pedrofintech/lf-site-assets@63c25df227931cfeb49da2121df5719c1107cc46/kit/";
  var PRIV = "https://www.literaciafinanceira.pt/politicas/politica-de-privacidade";
  var TIPO_POR_PAGINA = {
    "comparador-depositos-a-prazo": "dp", "indice-depositos-a-prazo": "dp",
    "comparador-eletricidade": "el", "indice-eletricidade": "el",
    "simulador-euribor-prestacao": "eu", "euribor-hoje": "eu",
    "comparador-de-corretoras": "co"
  };
  /* Raiz da ferramenta em cada comparador: o bloco entra no fim da secção que a contém. */
  var RAIZES = ["#lf-dp", "#lf-cc", "#calc-ep", "#lf-euribor"];

  function pct(v) { return LFK.fmt(v, { currency: false }) + "%"; }
  function eur(v) { return LFK.fmt(v, { decimals: 0 }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function campo(id, label, html) { return '<div class="lfk-field"><label class="lfk-label" for="' + id + '">' + label + "</label>" + html + "</div>"; }
  function sel(id, opcoes, escolhida) {
    return '<select class="lfk-input" id="' + id + '">' + opcoes.map(function (o) {
      return '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(escolhida) ? " selected" : "") + ">" + esc(o[1]) + "</option>";
    }).join("") + "</select>";
  }
  function num(id, valor, unidade, max, modo) {
    return '<div class="lfk-input-wrap"><input class="lfk-input lfk-num" id="' + id + '" inputmode="' + (modo || "decimal") + '" value="' + valor + '" data-max="' + max + '"><span class="lfk-unit">' + unidade + "</span></div>";
  }

  /* Cada tipo: título, texto, dados, campos do formulário, leitura dos campos e frase "hoje". */
  var TIPOS = {
    dp: {
      titulo: "Recebe um alerta quando houver um depósito melhor",
      texto: "Escolhe o prazo e a taxa que procuras. Verificamos os depósitos nos dias 1 e 16 de cada mês e enviamos um email só quando houver um depósito novo que cumpra o teu critério.",
      dados: "https://franklinsilvapt-arch.github.io/depositos-comparator/data/depositos.json",
      campos: function () {
        return '<div class="lfk-grid is-3">' +
          campo("al-prazo", "Prazo", sel("al-prazo", [[3, "3 meses"], [6, "6 meses"], [12, "12 meses"], [24, "24 meses"]], 12)) +
          campo("al-taxa", "TANB mínima", num("al-taxa", "3,00", "%", 10)) +
          campo("al-mont", "Montante", num("al-mont", "10.000", "€", 10000000, "numeric")) + "</div>";
      },
      ler: function () {
        var prazo = val("al-prazo"), taxa = LFK.num(val("al-taxa")), mont = LFK.num(val("al-mont"));
        if (!taxa || !mont) return null;
        return { DP_PRAZO: prazo, DP_TAXA: String(taxa).replace(".", ","), DP_MONT: String(Math.round(mont)) };
      },
      hoje: function (d, c) {
        var prazo = c.DP_PRAZO, taxa = LFK.num(c.DP_TAXA), mont = +c.DP_MONT;
        var l = d.depositos.filter(function (x) {
          if (x.a_confirmar || x.idade_max) return false;
          var p = x.prazos[prazo]; if (!p) return false;
          var mn = p.min != null ? p.min : (x.min || 0), mx = p.max != null ? p.max : x.max;
          return p.tanb >= taxa && mont >= mn && (mx == null || mont <= mx);
        }).sort(function (a, b) { return b.prazos[prazo].tanb - a.prazos[prazo].tanb; });
        return l.length
          ? "Hoje já há " + l.length + (l.length === 1 ? " depósito" : " depósitos") + " com este critério. O melhor é " + esc(l[0].banco) + ", " + esc(l[0].produto) + ", a " + pct(l[0].prazos[prazo].tanb) + "."
          : "Hoje nenhum depósito cumpre este critério. Avisamos-te quando aparecer um.";
      }
    },
    el: {
      titulo: "Recebe um alerta quando a eletricidade ficar mais barata",
      texto: "Escolhe o tipo de casa e o custo anual que queres pagar. Atualizamos as ofertas da ERSE todos os dias e enviamos um email quando a oferta mais barata ficar abaixo desse valor.",
      dados: "https://franklinsilvapt-arch.github.io/comparador-eletricidade/comparador-eletricidade/data/indice.json",
      campos: function () {
        return '<div class="lfk-grid is-2">' +
          campo("al-perfil", "Tipo de casa", sel("al-perfil", [["p1", "Casal sem filhos (3,45 kVA, 1.900 kWh)"], ["p2", "Casal com 2 filhos (6,9 kVA, 5.000 kWh)"]], "p2")) +
          campo("al-max", "Custo anual abaixo de", num("al-max", "1.000", "€", 100000, "numeric")) + "</div>";
      },
      ler: function () {
        var max = LFK.num(val("al-max"));
        if (!max) return null;
        return { EL_PERFIL: val("al-perfil"), EL_MAX: String(Math.round(max)) };
      },
      hoje: function (d, c) {
        var p = (d.perfis || []).filter(function (x) { return x.id === c.EL_PERFIL; })[0];
        if (!p) return "";
        return p.melhor.total < +c.EL_MAX
          ? "Hoje já há uma oferta abaixo desse valor: " + esc(p.melhor.comercializador) + ", " + esc(p.melhor.oferta) + ", por " + eur(p.melhor.total) + " por ano."
          : "Hoje a oferta mais barata custa " + eur(p.melhor.total) + " por ano (" + esc(p.melhor.comercializador) + "). Avisamos-te quando descer abaixo de " + eur(+c.EL_MAX) + ".";
      },
      preencher: function (d) {
        /* Sugere um valor um pouco abaixo da oferta mais barata de hoje. */
        var p = (d.perfis || []).filter(function (x) { return x.id === val("al-perfil"); })[0];
        if (p) document.getElementById("al-max").value = LFK.fmt(Math.floor(p.melhor.total * 0.95 / 10) * 10, { decimals: 0, currency: false });
      }
    },
    eu: {
      titulo: "Recebe um alerta quando a Euribor mudar",
      texto: "Escolhe o prazo da Euribor do teu crédito e o valor que te interessa. Acompanhamos a Euribor todos os dias úteis e enviamos um email quando passar esse valor.",
      dados: "https://cdn.jsdelivr.net/gh/franklinsilvapt-arch/euribor-hoje@main/euribor-data.json",
      campos: function () {
        return '<div class="lfk-grid is-3">' +
          campo("al-eprazo", "Euribor", sel("al-eprazo", [[3, "3 meses"], [6, "6 meses"], [12, "12 meses"]], 12)) +
          campo("al-dir", "Avisa-me quando", sel("al-dir", [["abaixo", "descer abaixo de"], ["acima", "subir acima de"]], "abaixo")) +
          campo("al-etaxa", "Valor", num("al-etaxa", "2,50", "%", 10)) + "</div>";
      },
      ler: function () {
        var t = LFK.num(val("al-etaxa"));
        if (!t) return null;
        return { EU_PRAZO: val("al-eprazo"), EU_DIR: val("al-dir"), EU_TAXA: String(t).replace(".", ",") };
      },
      hoje: function (d, c) {
        var u = d.serie[d.serie.length - 1], v = u["m" + c.EU_PRAZO], t = LFK.num(c.EU_TAXA);
        var ja = c.EU_DIR === "abaixo" ? v < t : v > t;
        return "A Euribor a " + c.EU_PRAZO + " meses estava em " + pct(v) + " a " + u.d + "." +
          (ja ? " Já está " + (c.EU_DIR === "abaixo" ? "abaixo" : "acima") + " desse valor: o primeiro email chega na próxima atualização." : " Avisamos-te quando passar " + pct(t) + ".");
      },
      preencher: function (d) {
        var u = d.serie[d.serie.length - 1], v = u["m" + val("al-eprazo")];
        document.getElementById("al-etaxa").value = LFK.fmt(Math.round((v - 0.25) * 20) / 20, { currency: false });
      }
    },
    co: {
      titulo: "Recebe um alerta quando uma corretora mudar os custos",
      texto: "Escolhe a corretora que usas ou que estás a pensar usar. Revemos os preçários todos os meses e enviamos um email quando mudarem as comissões ou as condições.",
      dados: "https://franklinsilvapt-arch.github.io/corretoras-comparator/data/corretoras.json",
      campos: function (d) {
        var l = d ? d.corretoras.map(function (c) { return [c.id, c.name]; }) : [["", "A carregar..."]];
        return '<div class="lfk-grid is-2">' + campo("al-cor", "Corretora", sel("al-cor", l, "xtb")) + "</div>";
      },
      ler: function () { var v = val("al-cor"); return v ? { CO_ID: v } : null; },
      hoje: function (d, c) {
        var x = d.corretoras.filter(function (y) { return y.id === c.CO_ID; })[0];
        return x ? "Avisamos-te quando mudarem as comissões ou as condições da " + esc(x.name) + "." : "";
      },
      precisaDados: true
    }
  };

  function val(id) { var e = document.getElementById(id); return e ? e.value : ""; }

  function carregarKit(feito) {
    if (window.LFK) return feito();
    if (!document.querySelector('link[href*="lf-kit.css"]')) {
      var l = document.createElement("link"); l.rel = "stylesheet"; l.href = KIT + "lf-kit.css"; document.head.appendChild(l);
    }
    var s = document.querySelector('script[src*="lf-kit.js"]');
    if (!s) { s = document.createElement("script"); s.src = KIT + "lf-kit.js"; document.body.appendChild(s); }
    s.addEventListener("load", feito);
    var n = 0, t = setInterval(function () { if (window.LFK || ++n > 100) { clearInterval(t); if (window.LFK) feito(); } }, 100);
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

  function postarNoMailchimp(campos) {
    /* Usado quando o Mailchimp pede captcha: abre a página dele com os dados já preenchidos. */
    var f = document.createElement("form");
    f.method = "post"; f.action = MC.action; f.target = "_blank"; f.style.display = "none";
    Object.keys(campos).forEach(function (k) { var i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = campos[k]; f.appendChild(i); });
    document.body.appendChild(f); f.submit(); f.parentNode.removeChild(f);
  }

  function raiz() {
    var r = document.getElementById("lf-alerta-dp") || document.getElementById("lf-alerta-el") || document.getElementById("lf-alerta");
    if (r) return r;
    /* Nos índices o div é criado pelo próprio índice depois de carregar os dados (que chama window.LFAlerta). */
    if (/^\/indice-/.test(location.pathname)) return null;
    /* Comparadores: junta um bloco no fim da secção da ferramenta, com as classes de layout do site. */
    for (var i = 0; i < RAIZES.length; i++) {
      var ferr = document.querySelector(RAIZES[i]);
      if (!ferr) continue;
      var sec = ferr.closest("section") || ferr.parentNode;
      /* Mesma largura e centro da ferramenta (os comparadores usam min(1120px, 100vw - 48px)). */
      var grelha = ferr.closest(".is-calculadora") || ferr;
      var larg = Math.round(grelha.getBoundingClientRect().width) || 1120;
      var w = document.createElement("div");
      w.style.cssText = "width:min(" + Math.max(larg, 320) + "px,calc(100vw - 48px));margin:0 auto;padding:2.5rem 0 3rem";
      w.innerHTML = '<div id="lf-alerta" data-modo="comparador"></div>';
      sec.appendChild(w);
      return document.getElementById("lf-alerta");
    }
    return null;
  }

  function iniciar() {
    var r = raiz();
    if (!r || r.getAttribute("data-pronto")) return;
    var nome = location.pathname.replace(/^\/|\/$/g, "").split("/").pop();
    var tipo = TIPOS[r.getAttribute("data-tipo") || (r.id === "lf-alerta-el" ? "el" : r.id === "lf-alerta-dp" ? "dp" : TIPO_POR_PAGINA[nome])];
    if (!tipo) return;
    r.setAttribute("data-pronto", "1");
    carregarKit(function () { desenhar(r, tipo); });
  }

  function desenhar(r, tipo) {
    var dados = null;
    /* Nos comparadores o cartão segue o desenho da página: largura da ferramenta, moldura fina como os cartões
       dos resultados e campos numa só linha em desktop. Nos índices fica o cartão normal do kit. */
    var comp = r.getAttribute("data-modo") === "comparador";
    function html() {
      var email = '<div class="lfk-field" id="al-f-email"><label class="lfk-label" for="al-email">Email</label><input class="lfk-input" id="al-email" type="email" autocomplete="email" placeholder="o.teu@email.pt"><span class="lfk-error" id="al-e-email" hidden>Escreve um email válido.</span></div>';
      var ok = '<div class="lfk-field" id="al-f-ok"><label class="lfk-check"><input type="checkbox" id="al-ok"> <span>Quero receber por email os alertas que pedi. <small>Podes cancelar em qualquer email. Ver a <a class="lfk-link" href="' + PRIV + '" target="_blank" rel="noopener">política de privacidade</a>.</small></span></label><span class="lfk-error" id="al-e-ok" hidden>Para criar o alerta tens de aceitar receber os emails.</span></div>';
      var btn = '<button type="button" class="lfk-btn" id="al-btn">Criar alerta</button>';
      var campos = tipo.campos(dados);
      var cab = '<div class="lfk-stack is-sm"><h2 class="lfk-h-sm">' + tipo.titulo + "</h2>" + '<p class="lfk-small lfk-muted">' + tipo.texto + "</p></div>";
      if (comp) {
        campos = campos.replace(/^<div class="lfk-grid is-\d">/, '<div class="lfk-grid">').replace(/<\/div>$/, email + "</div>");
        return '<div class="lfk"><div class="lfk-card is-sm" style="border-width:1px;border-color:#e9ecf1;border-radius:16px"><div class="lfk-stack">' + cab +
          '<form class="lfk-stack" id="al-form" onsubmit="return false" novalidate>' + campos +
          '<div class="lfk-row is-between" style="align-items:flex-start">' + ok + btn + "</div>" +
          '<div id="al-msg"></div></form></div></div></div>';
      }
      return '<div class="lfk"><div class="lfk-calc"><div class="lfk-card"><div class="lfk-stack">' + cab +
        '<form class="lfk-stack" id="al-form" onsubmit="return false" novalidate>' + campos + email + ok +
        "<div>" + btn + "</div>" + '<div id="al-msg"></div></form></div></div></div></div>';
    }
    function montar() {
      r.innerHTML = html();
      LFK.selects(r);
      if (dados && tipo.preencher) {
        tipo.preencher(dados);
        var s = r.querySelector("select");
        if (s) s.addEventListener("change", function () { tipo.preencher(dados); });
      }
      ligar();
    }
    function ligar() {
      var msg = document.getElementById("al-msg");
      function aviso(cls, txt) { msg.innerHTML = '<div class="lfk-alert ' + cls + '">' + txt + "</div>"; }
      document.getElementById("al-btn").addEventListener("click", function () {
        var email = val("al-email").trim(), aceitou = document.getElementById("al-ok").checked;
        var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        document.getElementById("al-f-email").classList.toggle("is-error", !emailOk);
        document.getElementById("al-e-email").hidden = emailOk;
        document.getElementById("al-f-ok").classList.toggle("is-error", !aceitou);
        document.getElementById("al-e-ok").hidden = aceitou;
        var crit = tipo.ler();
        if (!emailOk || !aceitou || !crit) return;
        var hoje = dados ? " " + tipo.hoje(dados, crit) : "";
        var campos = { EMAIL: email };
        Object.keys(crit).forEach(function (k) { campos[k] = crit[k]; });
        campos[MC.honeypot] = "";
        var b = this; b.disabled = true;
        enviar(campos).then(function (res) {
          b.disabled = false;
          if (res && res.result === "success") aviso("is-ok", "<b>Falta um passo:</b> enviámos-te um email para confirmares o alerta." + hoje);
          else if (res && res.result === "redirect") {
            aviso("is-warn", "<b>Falta um passo:</b> confirma que não és um robô na página do Mailchimp. " +
              '<button type="button" class="lfk-btn is-sm" id="al-mc">Concluir inscrição</button>');
            document.getElementById("al-mc").addEventListener("click", function () {
              postarNoMailchimp(campos);
              aviso("is-ok", "<b>Quase feito:</b> depois do captcha, enviamos-te um email para confirmares o alerta." + hoje);
            });
          }
          else if (res && /already subscribed|já está|is already a list member/i.test(res.msg || "")) aviso("is-warn", "<b>Este email já tem um alerta.</b> Para mudares o critério ou juntares outro, usa o link Atualizar preferências no fim de qualquer alerta que recebeste.");
          else aviso("is-err", "Não foi possível criar o alerta. Confirma o email e tenta outra vez.");
        }, function () { b.disabled = false; aviso("is-err", "Não foi possível ligar ao serviço de email. Tenta outra vez dentro de alguns minutos."); });
      });
    }
    montar();
    fetch(tipo.dados + (tipo.dados.indexOf("jsdelivr") > -1 ? "" : "?v=" + Math.floor(Date.now() / 600000)))
      .then(function (x) { return x.json(); })
      .then(function (d) {
        dados = d;
        if (tipo.precisaDados || tipo.preencher) {
          /* Guarda o que a pessoa já escreveu antes de redesenhar com os dados. */
          var email = val("al-email"), ok = document.getElementById("al-ok").checked;
          montar();
          document.getElementById("al-email").value = email; document.getElementById("al-ok").checked = ok;
        }
      }).catch(function () {});
  }

  /* Os índices desenham o seu div depois de carregar os dados: chamam window.LFAlertaDP() ou window.LFAlerta(). */
  window.LFAlerta = window.LFAlertaDP = iniciar;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
