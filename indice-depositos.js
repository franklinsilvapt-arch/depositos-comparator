/* Índice de depósitos a prazo do Literacia Financeira.
   Lê data/indice.json (gerado por scripts/gerar_indice.py) e desenha a página com o lf-kit do Diogo.
   Requer lf-kit.css e lf-kit.js carregados antes. Raiz: o div #lf-dp (ou #lf-indice) da página. */
(function () {
  var BASE = "https://franklinsilvapt-arch.github.io/depositos-comparator/";
  var KIT_IMG = "https://cdn.jsdelivr.net/gh/pedrofintech/lf-site-assets@63c25df227931cfeb49da2121df5719c1107cc46/kit/img/illustration-chart.png";
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var MES_CURTO = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];

  function pct(v) { return LFK.fmt(v, { currency: false }) + "%"; }
  function pp(v) { return LFK.fmt(v, { currency: false }); }
  function eur(v) { return LFK.fmt(v); }
  function eur0(v) { return LFK.fmt(v, { decimals: 0 }); }
  function dataLonga(iso) { var p = iso.split("-"); return +p[2] + " de " + MESES[+p[1] - 1] + " de " + p[0]; }
  function dataCurta(iso) { var p = iso.split("-"); return +p[2] + " " + MES_CURTO[+p[1] - 1]; }
  function mesLongo(ym) { var p = ym.split("-"); return MESES[+p[1] - 1] + " de " + p[0]; }
  function prazoTxt(p) { return p + " meses"; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function quem(m) {
    if (!m) return "";
    var extra = m.novos === "clientes" ? ", novos clientes" : m.novos === "montantes" ? ", dinheiro novo" : "";
    return esc(m.banco) + ", " + esc(m.produto) + extra;
  }
  function celula(m) {
    if (!m) return "-";
    return '<span class="lfk-strong">' + pct(m.tanb) + '</span><br><span class="lfk-xs lfk-muted">' + quem(m) + (m.sem_retencao ? ", sem retenção na fonte" : "") + "</span>";
  }
  function liquido(t, d) { return d.montante * t / 100 * (1 - d.retencao_irs); }

  function autores(d) {
    function a(img, label, nome, href) {
      var inner = '<span class="lfk-author-img"><img src="' + img + '" alt="' + nome + '"></span><span><span class="lfk-author-sub">' + label + '</span><span class="lfk-author-name">' + nome + "</span></span>";
      return href ? '<a class="lfk-author" href="' + href + '">' + inner + "</a>" : '<div class="lfk-author">' + inner + "</div>";
    }
    return '<div class="lfk-row">' +
      a("https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0ae5bc67fe0ef48466e_franklin-silva.avif", "Autor", "Franklin Silva", "https://www.literaciafinanceira.pt/autores/franklin-silva") +
      a("https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0f9b80a20ec1767fab5_Pedro-Braz.avif", "Revisor", "Pedro Braz", "https://www.literaciafinanceira.pt/autores/pedro-braz") +
      '<div class="lfk-stack is-sm"><span class="lfk-xs lfk-muted">Última verificação</span><span class="lfk-small lfk-strong">' + dataLonga(d.atualizado) + "</span></div>" +
      "</div>";
  }

  function numeros(d) {
    var p12 = d.prazos["12"], best = p12.melhor_sem_condicoes, ref = d.referencias;
    var h = '<div class="lfk-kpis">' +
      '<div class="lfk-stat is-brand"><div class="lfk-stat-l">Melhor taxa a 12 meses sem condições</div><div class="lfk-stat-v">' + pct(best.tanb) + '</div><div class="lfk-stat-s">' + quem(best) + ". " + eur0(d.montante) + " rendem " + eur(liquido(best.tanb, d)) + " líquidos</div></div>" +
      '<div class="lfk-stat"><div class="lfk-stat-l">Taxa mediana a 12 meses</div><div class="lfk-stat-v">' + pct(p12.mediana) + '</div><div class="lfk-stat-s">Metade dos ' + p12.n + " depósitos paga mais. " + eur0(d.montante) + " rendem " + eur(liquido(p12.mediana, d)) + " líquidos</div></div>";
    if (ref) h += '<div class="lfk-stat"><div class="lfk-stat-l">Média dos novos depósitos em Portugal</div><div class="lfk-stat-v">' + pct(ref.portugal) + '</div><div class="lfk-stat-s">Todos os prazos, ' + mesLongo(ref.mes) + " (Banco de Portugal). Na zona euro: " + pct(ref.zona_euro) + "</div></div>";
    h += "</div>";
    h += '<p class="lfk-foot">Juros líquidos a 12 meses com retenção de IRS de 28%.' + (ref ? ' Fonte da média nacional: <a class="lfk-link" href="' + ref.url + '" target="_blank" rel="noopener">' + esc(ref.titulo) + "</a> (Banco de Portugal, " + dataLonga(ref.publicado) + ")." : "") + "</p>";
    return h;
  }

  function cartao(id, titulo, corpo, nota) {
    return '<div class="lfk-card" id="' + id + '"><div class="lfk-card-head"><h2 class="lfk-h-sm">' + titulo + "</h2></div>" + corpo + (nota ? '<p class="lfk-table-note">' + nota + "</p>" : "") + "</div>";
  }

  function alteracoesHtml(d) {
    var a = d.alteracoes;
    if (!a) return "";
    function agrupar(lst) {
      var g = {}, ordem = [];
      lst.forEach(function (e) {
        var k = e.banco + "|" + e.produto;
        if (!g[k]) { g[k] = { banco: e.banco, produto: e.produto, prazos: [], antes: e.antes, depois: e.depois, delta: 0 }; ordem.push(k); }
        g[k].prazos.push(e.prazo);
        var dl = Math.abs(e.depois - e.antes);
        if (dl > g[k].delta) { g[k].delta = dl; g[k].antes = e.antes; g[k].depois = e.depois; }
      });
      return ordem.map(function (k) { return g[k]; }).sort(function (x, y) { return y.delta - x.delta; });
    }
    function prazosTxt(l) {
      l = l.slice().sort(function (x, y) { return x - y; });
      if (l.length === 1) return l[0] + " meses";
      return l.slice(0, -1).join(", ") + " e " + l[l.length - 1] + " meses";
    }
    function linhas(lst, max) {
      return agrupar(lst).slice(0, max).map(function (x) {
        var var_ = x.prazos.length > 1 ? "maior variação em " + prazosTxt(x.prazos) : prazosTxt(x.prazos);
        return '<div class="lfk-line"><div class="lfk-line-main"><span class="lfk-line-label">' + esc(x.banco) + ", " + esc(x.produto) + '</span><span class="lfk-line-value">' + pct(x.antes) + " → " + pct(x.depois) + '</span></div><div class="lfk-line-note">' + var_ + "</div></div>";
      }).join("");
    }
    var nS = a.subidas.length, nD = a.descidas.length;
    var intro = '<p class="lfk-text">Entre as verificações de ' + dataLonga(a.desde) + " e " + dataLonga(a.ate) + " houve " + (nS + nD) + " alterações de taxa: " + nS + (nS === 1 ? " subida" : " subidas") + " e " + nD + (nD === 1 ? " descida" : " descidas") + ". Entraram " + a.entraram.length + " depósitos no comparador e " + (a.sairam.length === 1 ? "saiu 1" : "saíram " + a.sairam.length) + ".</p>";
    var col = function (tag, cls, lst) {
      return '<div class="lfk-stack is-sm"><span class="lfk-tag ' + cls + '">' + tag + "</span>" + (lst.length ? linhas(lst, 6) : '<p class="lfk-small lfk-muted">Sem alterações.</p>') + "</div>";
    };
    return cartao("ix-mud", "O que mudou desde " + dataLonga(a.desde), intro + '<div class="lfk-grid is-2">' + col(nS + (nS === 1 ? " subida" : " subidas"), "is-ok", a.subidas) + col(nD + (nD === 1 ? " descida" : " descidas"), "is-err", a.descidas) + "</div>");
  }

  function citacao(d) {
    var txt = "Literacia Financeira, Índice de depósitos a prazo, " + mesLongo(d.atualizado.slice(0, 7)) + " (dados de " + d.atualizado.split("-").reverse().join("/") + "). literaciafinanceira.pt/indice-depositos-a-prazo";
    return '<div class="lfk-card is-soft"><div class="lfk-stack is-sm"><h2 class="lfk-h-sm">Como citar</h2><p class="lfk-text" id="ix-cit">' + esc(txt) + '</p><div><button type="button" class="lfk-btn is-secondary is-sm" id="ix-copy">Copiar citação</button></div></div></div>';
  }

  function desenhar(root, d) {
    var P = ["3", "6", "12", "24"];
    var h = '<div class="lfk"><div class="lfk-calc"><div class="lfk-stack is-lg">' + autores(d) + numeros(d);

    h += cartao("ix-prazos", "Taxas por prazo", '<p class="lfk-small lfk-muted">A melhor taxa costuma ser de uma campanha para novos clientes ou para dinheiro novo. "Sem condições" é a melhor taxa aberta a qualquer cliente.</p><div id="ix-t-prazos"></div>',
      "TANB para quem aplica " + eur0(d.montante) + ". " + d.universo.depositos + " depósitos de " + d.universo.bancos + " bancos, confirmados no site e na FIN de cada banco.");

    var temCamp = P.filter(function (p) { return d.prazos[p].mediana_campanhas != null && d.prazos[p].mediana_sem_condicoes != null; });
    if (temCamp.length) {
      var p12 = d.prazos["12"], dif = p12.mediana_campanhas != null ? p12.mediana_campanhas - p12.mediana_sem_condicoes : null;
      var lead = dif != null ? '<p class="lfk-text">A 12 meses, a taxa mediana das campanhas está ' + pp(dif) + " pontos acima da oferta sem condições. Em " + eur0(d.montante) + " isso dá " + eur(liquido(dif, d)) + " líquidos a mais num ano.</p>" : "";
      h += cartao("ix-camp", "Quanto vale ser cliente novo?", lead + '<div id="ix-t-camp"></div>', "Mediana da TANB. Campanhas são depósitos só para novos clientes ou para dinheiro novo no banco. Só entram prazos com pelo menos 3 depósitos em cada grupo.");
    }

    h += '<div class="lfk-card" id="ix-evol"><div class="lfk-card-head"><h2 class="lfk-h-sm">Evolução da taxa a 12 meses</h2></div>' +
      '<div class="lfk-chart-head"><div class="lfk-toggle" role="tablist"><button type="button" class="lfk-tab is-active" data-lfk-tab="g">Gráfico</button><button type="button" class="lfk-tab" data-lfk-tab="t">Tabela</button></div>' +
      '<div class="lfk-menu" data-chart="#ix-c-evol" data-table="#ix-t-evol" data-file="indice-depositos-12-meses"></div></div>' +
      '<div data-lfk-view="g"><div class="lfk-chart is-sm"><canvas id="ix-c-evol"></canvas></div></div><div data-lfk-view="t" hidden id="ix-t-evol"></div>' +
      '<p class="lfk-table-note">Índice encadeado: parte da média de ' + dataLonga(d.serie_12m[0].data) + " e soma, em cada verificação, a variação média dos depósitos a 12 meses presentes nas duas datas. Assim a série mede mudanças de taxa e não a entrada de novos depósitos no comparador.</p></div>";

    h += alteracoesHtml(d);

    if (d.edicoes && d.edicoes.length > 1) {
      h += cartao("ix-ed", "Edições mensais", '<div id="ix-t-ed"></div>', "Cada edição mensal guarda os números da primeira verificação do mês.");
    }

    h += '<a class="lfk-calc-card" href="https://www.literaciafinanceira.pt/comparador-depositos-a-prazo"><div class="lfk-calc-card-body"><h4 class="lfk-calc-card-title">Comparador de depósitos a prazo</h4><p class="lfk-ds-text">Vê todos os depósitos, filtra por montante e prazo e descobre quanto rende cada um.</p></div><img class="lfk-calc-card-img" src="' + KIT_IMG + '" alt=""></a>';
    h += citacao(d);
    h += "</div></div></div>";
    root.innerHTML = h;

    LFK.table(document.getElementById("ix-t-prazos"), {
      head: ["Prazo", "Melhor taxa", "Sem condições", "Mediana", "Depósitos"], num: [false, false, false, true, true],
      rows: P.map(function (p) {
        var x = d.prazos[p];
        return [prazoTxt(p), celula(x.melhor), celula(x.melhor_sem_condicoes), pct(x.mediana), String(x.n)];
      })
    });
    if (temCamp.length) LFK.table(document.getElementById("ix-t-camp"), {
      head: ["Prazo", "Campanhas", "Sem condições", "Diferença"], num: [false, true, true, true],
      rows: temCamp.map(function (p) {
        var x = d.prazos[p];
        return [prazoTxt(p), pct(x.mediana_campanhas) + " (" + x.n_campanhas + ")", pct(x.mediana_sem_condicoes) + " (" + x.n_sem_condicoes + ")", "+" + pp(x.mediana_campanhas - x.mediana_sem_condicoes) + " pontos"];
      })
    });

    var ev = document.getElementById("ix-evol");
    LFK.views(ev);
    var labels = d.serie_12m.map(function (s) { return dataCurta(s.data); });
    var chart = LFK.line(document.getElementById("ix-c-evol"), {
      labels: labels, money: pct,
      datasets: [{ label: "Taxa média a 12 meses", data: d.serie_12m.map(function (s) { return s.taxa; }) }]
    });
    if (chart && chart.then) chart.then(function (c) {
      c.options.scales.y.ticks.callback = function (v) { return pct(v); };
      c.options.scales.y.ticks.stepSize = 0.05;
      var vals = d.serie_12m.map(function (x) { return x.taxa; });
      c.options.scales.y.min = Math.floor(Math.min.apply(null, vals) * 20 - 1) / 20;
      c.options.scales.y.max = Math.ceil(Math.max.apply(null, vals) * 20 + 1) / 20;
      c.data.datasets[0].tension = 0;
      c.data.datasets[0].pointRadius = 3;
      c.update("none");
    });
    LFK.table(document.getElementById("ix-t-evol"), {
      head: ["Verificação", "Taxa média a 12 meses", "Depósitos comparados"], num: [false, true, true],
      rows: d.serie_12m.map(function (s) { return [dataLonga(s.data), pct(s.taxa), String(s.depositos)]; })
    });

    var ted = document.getElementById("ix-t-ed");
    if (ted) LFK.table(ted, {
      head: ["Edição", "Mediana a 12 meses", "Melhor a 12 meses sem condições"], num: [false, true, false],
      rows: d.edicoes.slice().reverse().map(function (e) {
        var m = e.melhor_12m_sem_condicoes;
        return [mesLongo(e.mes), pct(e.mediana_12m), celula(m)];
      })
    });

    var b = document.getElementById("ix-copy");
    b.addEventListener("click", function () {
      var t = document.getElementById("ix-cit").textContent;
      function ok() { b.textContent = "Copiado"; setTimeout(function () { b.textContent = "Copiar citação"; }, 2000); }
      function sel() { var r = document.createRange(); r.selectNodeContents(document.getElementById("ix-cit")); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
      try { navigator.clipboard.writeText(t).then(ok, sel); } catch (e) { sel(); }
    });
    if (window.ScrollTrigger && window.ScrollTrigger.refresh) window.ScrollTrigger.refresh();
  }

  function iniciar() {
    var root = document.getElementById("lf-indice") || document.getElementById("lf-dp");
    if (!root || !window.LFK) return;
    root.innerHTML = '<div class="lfk"><div class="lfk-empty"><p>A carregar o índice...</p></div></div>';
    fetch(BASE + "data/indice.json?v=" + Math.floor(Date.now() / 600000))
      .then(function (r) { return r.json(); })
      .then(function (d) { desenhar(root, d); })
      .catch(function () {
        root.innerHTML = '<div class="lfk"><div class="lfk-alert is-err">Não foi possível carregar o índice. Atualiza a página dentro de alguns minutos.</div></div>';
      });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
