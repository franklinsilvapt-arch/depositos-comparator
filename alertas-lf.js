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
    return null;
  }

  function iniciar() {
    var nomePag = location.pathname.replace(/^\/|\/$/g, "").split("/").pop();
    if (LINHAS[nomePag] && !/^indice-/.test(nomePag)) { carregarKit(function () { LINHAS[nomePag](); }); return; }
    var r = raiz();
    if (!r || r.getAttribute("data-pronto")) return;
    var nome = location.pathname.replace(/^\/|\/$/g, "").split("/").pop();
    var tipo = TIPOS[r.getAttribute("data-tipo") || (r.id === "lf-alerta-el" ? "el" : r.id === "lf-alerta-dp" ? "dp" : TIPO_POR_PAGINA[nome])];
    if (!tipo) return;
    r.setAttribute("data-pronto", "1");
    /* As páginas usam o Lenis (scroll suave), que bloqueia o scroll dentro das listas de opções. */
    r.setAttribute("data-lenis-prevent", "");
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


  /* ---------- Linha compacta nos comparadores ----------
     Uma linha logo acima dos resultados, já preenchida com o que a pessoa escolheu na ferramenta.
     Só pede o email. A moldura segue os cartões dos resultados (1px, cantos de 16px). */
  var SINO = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>';
  var dadosCache = {};
  function obterDados(url, feito) {
    if (dadosCache[url]) return feito(dadosCache[url]);
    fetch(url + (url.indexOf("jsdelivr") > -1 ? "" : "?v=" + Math.floor(Date.now() / 600000))).then(function (x) { return x.json(); })
      .then(function (d) { dadosCache[url] = d; feito(d); }).catch(function () {});
  }
  /* Quem fecha a linha não a volta a ver nesta página durante 30 dias (só neste browser). */
  var CHAVE = "lf-alerta-fechado:" + location.pathname;
  function fechado(marcar) {
    try {
      if (marcar) { localStorage.setItem(CHAVE, String(Date.now())); return true; }
      var t = +localStorage.getItem(CHAVE);
      return !!t && Date.now() - t < 30 * 864e5;
    } catch (e) { return !!marcar || !!window.__lfAlFechado; }
    finally { if (marcar) window.__lfAlFechado = true; }
  }
  function arredonda(v, passo) { return Math.round(v / passo) * passo; }

  /* html: frase com os controlos (já com ids al-*); devolve o elemento da linha. */
  function criarLinha(id, frase, resumo) {
    var el = document.createElement("div");
    el.id = id; el.className = "lfk"; el.setAttribute("data-lenis-prevent", "");
    /* No telemóvel começa fechada: uma linha com o resumo e o botão que abre o formulário. */
    var fechada = window.innerWidth < 600 && resumo;
    el.innerHTML = '<div class="lfk-card" style="position:relative;padding:14px 44px 14px 18px;border-width:1px;border-color:#e9ecf1;border-radius:16px;margin:0 0 12px">' +
      '<button type="button" class="lf-al-fechar" aria-label="Fechar o alerta" title="Fechar" style="position:absolute;top:8px;right:8px;width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;background:none;border:0;border-radius:8px;color:#697386;cursor:pointer;font-size:20px;line-height:1">&times;</button>' +
      (resumo ? '<div class="lf-al-resumo lfk-row" style="justify-content:space-between;gap:8px;flex-wrap:nowrap;' + (fechada ? "" : "display:none") + '"><span class="lfk-row" style="gap:8px;flex-wrap:nowrap"><span style="display:inline-flex;color:#ff5a1f">' + SINO + '</span><span style="font-size:15px">' + resumo + '</span></span><button type="button" class="lfk-btn is-secondary is-sm lf-al-abrir" style="flex:0 0 auto">Criar alerta</button></div>' : "") +
      '<div class="lf-al-corpo"' + (fechada ? ' style="display:none"' : "") + '>' +
      '<div class="lfk-row" style="justify-content:space-between;gap:10px 16px">' +
      '<div class="lfk-row" style="gap:6px 8px;flex:1 1 420px;align-items:center"><span style="display:inline-flex;color:#ff5a1f;flex:0 0 auto">' + SINO + "</span>" + frase + "</div>" +
      '<div class="lfk-row" style="gap:8px;flex:0 1 380px;flex-wrap:nowrap;margin-left:auto"><input class="lfk-input" id="al-email" type="email" autocomplete="email" placeholder="o.teu@email.pt" aria-label="Email" style="flex:1 1 auto;min-width:0;height:40px;font-size:15px">' +
      '<button type="button" class="lfk-btn" id="al-btn" style="flex:0 0 auto;height:40px">Avisar-me</button></div></div>' +
      '<p class="lfk-xs lfk-muted" style="margin:8px 0 0">Recebes um email para confirmar e podes cancelar quando quiseres. <a class="lfk-link" href="' + PRIV + '" target="_blank" rel="noopener">Política de privacidade</a>.</p>' +
      '<div id="al-msg" style="margin-top:8px"></div></div></div>';
    el.querySelector(".lf-al-fechar").addEventListener("click", function () {
      fechado(true);
      if (el.parentNode) el.parentNode.removeChild(el);
    });
    var abrir = el.querySelector(".lf-al-abrir");
    if (abrir) abrir.addEventListener("click", function () {
      el.querySelector(".lf-al-resumo").style.display = "none";
      el.querySelector(".lf-al-corpo").style.display = "";
      var e = el.querySelector("#al-email"); if (e) e.focus({ preventScroll: true });
    });
    return el;
  }
  /* Select nativo pequeno, para caber na frase (o dropdown do kit ocupa a largura toda). */
  var SETA = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%233A4454' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E\") no-repeat right 10px center";
  function selInline(id, opcoes, escolhida) {
    return '<select id="' + id + '" style="-webkit-appearance:none;appearance:none;font:inherit;font-size:15px;color:#202432;height:40px;padding:0 30px 0 12px;border:1px solid #ced5df;border-radius:12px;background:#fff ' + SETA + ';cursor:pointer">' + opcoes.map(function (o) {
      return '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(escolhida) ? " selected" : "") + ">" + esc(o[1]) + "</option>";
    }).join("") + "</select>";
  }
  function numInline(id, valor, unidade, larg) {
    return '<span class="lfk-input-wrap" style="display:inline-block;width:' + (larg || 104) + 'px"><input class="lfk-input lfk-num" id="' + id + '" inputmode="decimal" value="' + valor + '" style="height:40px;padding:0 28px 0 12px;font-size:15px"><span class="lfk-unit">' + unidade + "</span></span>";
  }
  function ligarLinha(el, ler, hoje) {
    var tocado = false;
    el.querySelectorAll("select, input:not(#al-email)").forEach(function (i) { i.addEventListener("change", function () { tocado = true; }); i.addEventListener("input", function () { tocado = true; }); });
    el.querySelector("#al-btn").addEventListener("click", function () {
      var msg = el.querySelector("#al-msg"), b = this;
      function aviso(cls, txt) { msg.innerHTML = '<div class="lfk-alert ' + cls + '">' + txt + "</div>"; }
      var email = el.querySelector("#al-email").value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { aviso("is-err", "Escreve um email válido para criarmos o alerta."); return; }
      var crit = ler();
      if (!crit) { aviso("is-err", "Confirma o valor do alerta."); return; }
      var campos = { EMAIL: email };
      Object.keys(crit).forEach(function (k) { campos[k] = crit[k]; });
      campos[MC.honeypot] = "";
      b.disabled = true;
      enviar(campos).then(function (res) {
        b.disabled = false;
        var h = hoje ? " " + hoje(crit) : "";
        if (res && res.result === "success") aviso("is-ok", "<b>Falta um passo:</b> enviámos-te um email para confirmares o alerta." + h);
        else if (res && /already subscribed|já está|is already a list member/i.test(res.msg || "")) aviso("is-warn", "<b>Este email já tem um alerta.</b> Para mudares o critério ou juntares outro, usa o link Mudar o critério no fim de qualquer alerta que recebeste.");
        else if (res && res.result === "redirect") { postarNoMailchimp(campos); aviso("is-ok", "<b>Quase feito:</b> abrimos a página do Mailchimp para concluíres a inscrição."); }
        else aviso("is-err", "Não foi possível criar o alerta. Confirma o email e tenta outra vez.");
      }, function () { b.disabled = false; aviso("is-err", "Não foi possível ligar ao serviço de email. Tenta outra vez dentro de alguns minutos."); });
    });
    return function () { return tocado; };
  }
  /* Insere (e volta a inserir se a ferramenta redesenhar) a linha antes de um elemento-âncora. */
  function manter(raizSel, ancora, montar) {
    var raizEl = document.querySelector(raizSel);
    if (!raizEl) return;
    function verificar() {
      if (document.getElementById("lf-al-linha") || fechado()) return;
      var a = ancora(raizEl);
      if (a) montar(a);
    }
    verificar();
    new MutationObserver(verificar).observe(raizEl, { childList: true, subtree: true, attributes: true, attributeFilter: ["class"] });
  }

  var LINHAS = {
    "comparador-depositos-a-prazo": function () {
      /* Resumo mensal (sugestão do Pedro): todos os meses as melhores taxas por prazo e o que mudou. Sem critério a escolher. */
      manter("#lf-dp", function (r) { return r.querySelector(".dp-cards"); }, function (a) {
        var el = criarLinha("lf-al-linha", "<span>Recebe todos os meses as melhores taxas de depósitos a prazo e o que mudou</span>", "Recebe as melhores taxas todos os meses");
        el.querySelector("#al-btn").textContent = "Subscrever";
        a.parentNode.insertBefore(el, a);
        ligarLinha(el, function () { return { DM: "1" }; }, function () { return "Depois de confirmares, o primeiro resumo chega no dia seguinte e os outros no início de cada mês."; });
      });
    },
    "comparador-eletricidade": function () {
      manter("#lf-dp", function (r) { return window.LFEletricidade && window.LFEletricidade.melhorMes ? r.querySelector(".dp-cards") : null; }, function (a) {
        var s = window.LFEletricidade, alvo = Math.max(5, Math.floor(s.melhorMes * 0.95));
        var el = criarLinha("lf-al-linha", '<span>Avisa-me quando houver uma oferta abaixo de</span>' + numInline("al-max", String(alvo), "€", 88) + "<span>por mês para o meu consumo</span>", "Avisa-me de ofertas mais baratas");
        a.parentNode.insertBefore(el, a);
        ligarLinha(el, function () {
          var m = LFK.num(val("al-max")), x = window.LFEletricidade; if (!m || !x || !x.kwhAno) return null;
          return { EL_POT: String(x.pot), EL_KWH: String(x.kwhAno), EL_MES: String(m).replace(".", ",") };
        }, function (c) {
          var x = window.LFEletricidade;
          return "Hoje a mais barata para ti custa " + LFK.fmt(x.melhorMes) + " por mês (" + esc(x.nome) + "). Avisamos-te quando houver uma oferta de preço fixo abaixo de " + eur(LFK.num(c.EL_MES)) + ".";
        });
      });
    },
    "simulador-euribor-prestacao": function () {
      obterDados(TIPOS.eu.dados, function (d) {
        manter("#lfc-ep", function (r) { return r.classList.contains("lfc-ep-hidden") ? null : document.getElementById("ep-fonte"); }, function (a) {
          var pill = document.querySelector("#calc-ep .lfc-ep-pill.is-active"), m = pill && /(\d+)/.exec(pill.textContent);
          var prazo = m && [3, 6, 12].indexOf(+m[1]) > -1 ? +m[1] : 6;
          var hoje = d.serie[d.serie.length - 1]["m" + prazo];
          var el = criarLinha("lf-al-linha", "<span>Avisa-me quando a Euribor a " + prazo + " meses</span>" +
            selInline("al-dir", [["abaixo", "descer abaixo de"], ["acima", "subir acima de"]], "abaixo") +
            numInline("al-etaxa", LFK.fmt(arredonda(hoje - 0.25, 0.05), { currency: false }), "%", 96), "Avisa-me quando a Euribor mudar");
          el.style.marginTop = "24px";
          a.parentNode.insertBefore(el, a);
          ligarLinha(el, function () {
            var t = LFK.num(val("al-etaxa")); if (!t) return null;
            return { EU_PRAZO: String(prazo), EU_DIR: val("al-dir"), EU_TAXA: String(t).replace(".", ",") };
          }, function (c) { return TIPOS.eu.hoje(d, c); });
        });
      });
    },
    "comparador-de-corretoras": function () {
      obterDados(TIPOS.co.dados, function (d) {
        function idDe(nome) { var c = d.corretoras.filter(function (x) { return nome.indexOf(x.name) > -1; })[0]; return c ? c.id : null; }
        function abrir(id) {
          var c = d.corretoras.filter(function (x) { return x.id === id; })[0]; if (!c) return;
          var velho = document.getElementById("lf-al-linha"); if (velho) velho.parentNode.removeChild(velho);
          var ancora = document.querySelector("#lf-cc .cc-table"); if (!ancora) return;
          var el = criarLinha("lf-al-linha", "<span>Avisa-me quando a <b>" + esc(c.name) + "</b> mudar comissões ou condições</span>");
          ancora.parentNode.insertBefore(el, ancora);
          ligarLinha(el, function () { return { CO_ID: c.id }; }, function (k) { return TIPOS.co.hoje(d, k); });
          /* As páginas usam o Lenis: o scroll tem de passar por ele para ser suave. */
          function nativo() { window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset - 120, behavior: "smooth" }); }
          if (window.lenis && window.lenis.scrollTo) window.lenis.scrollTo(el, { offset: -120 }); else nativo();
          /* No telemóvel o Lenis pode estar parado: se a linha não ficou à vista, usa o scroll do browser. */
          setTimeout(function () { var t = el.getBoundingClientRect().top; if (t < 0 || t > window.innerHeight - 80) window.scrollTo(0, t + window.pageYOffset - 120); }, 900);
          setTimeout(function () { var e = document.getElementById("al-email"); if (e) e.focus({ preventScroll: true }); }, 400);
        }
        /* Link "Seguir custos" debaixo de cada corretora do cabeçalho da tabela. */
        function links() {
          document.querySelectorAll("#lf-cc .cc-head .cc-hcell").forEach(function (cel) {
            if (cel.querySelector(".lf-al-seguir")) return;
            var n = cel.querySelector(".cc-hname"), id = n && idDe(n.textContent);
            if (!id) return;
            var a = document.createElement("button");
            a.type = "button"; a.className = "lf-al-seguir lfk-link";
            a.style.cssText = "display:inline-flex;align-items:center;gap:4px;margin-top:6px;background:none;border:0;padding:0;font:inherit;font-size:13px;cursor:pointer;color:#3a4454";
            a.innerHTML = SINO.replace(/18/g, "14") + "Seguir custos";
            a.addEventListener("click", function () { abrir(id); });
            cel.appendChild(a);
          });
        }
        var raizCc = document.getElementById("lf-cc"); if (!raizCc) return;
        links(); new MutationObserver(links).observe(raizCc, { childList: true, subtree: true });
      });
    }
  };

  /* Os índices desenham o seu div depois de carregar os dados: chamam window.LFAlertaDP() ou window.LFAlerta(). */
  window.LFAlerta = window.LFAlertaDP = iniciar;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
