/* Comparador de eletricidade - literaciafinanceira.pt
   Dados: ofertas comerciais comunicadas a ERSE (eletricidade/data/ofertas.json, gerado por scripts/atualizar_ofertas.py).
   Calculo da fatura: mesma metodologia do simulador de precos da ERSE (validado ao centimo nos consumidores-tipo).
   Reutiliza o CSS do comparador de depositos (#lf-dp .dp-*) mais o suplemento comparador-eletricidade.css. */
(function () {
  'use strict';
  if (window.__lfElInit) return;
  window.__lfElInit = true;

  var SRC = (document.currentScript && document.currentScript.src) || '';
  var BASE = SRC ? SRC.replace(/[^\/]*(\?.*)?$/, '') : 'https://franklinsilvapt-arch.github.io/depositos-comparator/eletricidade/';
  var DATA_URL = BASE + 'data/ofertas.json';

  /* ---------- Parametros regulados (ERSE, 2026) ---------- */
  var POTS = [1.15, 2.3, 3.45, 4.6, 5.75, 6.9, 10.35, 13.8, 17.25, 20.7];
  /* Termo fixo das tarifas de acesso as redes em BTN, EUR/dia, em vigor desde 01/01/2026 */
  var TAR_POT = [0.0573, 0.1145, 0.1718, 0.2291, 0.2864, 0.3436, 0.5154, 0.6872, 0.8591, 1.0309];
  var IEC = 0.001;            /* imposto especial de consumo, EUR/kWh */
  var CAV = 2.85;             /* contribuicao audiovisual, EUR/mes */
  var LIM_IVA6 = 200 * 365 / 30; /* kWh/ano com IVA a 6% (200 kWh por 30 dias, potencias ate 6,9 kVA) */

  var NOMES = {
    TUR: 'Mercado regulado', ALFAENERGIA: 'Alfa Energia', AUDAX: 'Audax', COOP: 'Coopérnico', EDPC: 'EDP',
    END: 'Endesa', ENIPLENITUDE: 'Plenitude', EZUENERGIA: 'EZU Energia', GALP: 'Galp', GOLD: 'Goldenergy',
    IBD: 'Iberdrola', IBELECTRA: 'Ibelectra', JAFPLUS: 'JAFplus', LUZBOA: 'Luzboa', LUZIGAS: 'Luzigás',
    MEOENERGIA: 'MEO Energia', NABALIAENERGIA: 'Nabalia Energia', NOSSAENERGIA: 'Nossa Energia', OENEO: 'Oeneo',
    PORTULOGOS: 'Portulogos', REPSOL: 'Repsol', YESENERGY: 'Yes Energy', ACCIONA: 'Acciona', ELERGONE: 'Elergone',
    LOGICA: 'Logica Energy', 'ZUG POWER': 'Zug Power'
  };

  var PERFIS = [
    { k: 'p1', l: 'Casal sem filhos', kwh: 1900, pot: 2 },
    { k: 'p2', l: 'Casal com 2 filhos', kwh: 5000, pot: 5 },
    { k: 'p3', l: 'Casal com 4 filhos', kwh: 10900, pot: 7 }
  ];

  var FILTROS = [
    { k: 'fixo', i: 'lock', l: 'Preço fixo', f: function (o) { return o.f.charAt(3) === '0'; } },
    { k: 'semFid', i: 'unl', l: 'Sem fidelização', f: function (o) { return o.f.charAt(0) === '0'; } },
    { k: 'semServ', i: 'wal', l: 'Sem serviços adicionais', f: function (o) { return o.f.charAt(4) === '0'; } },
    { k: 'semCond', i: 'usr', l: 'Sem condições de acesso', f: function (o) { return o.f.charAt(2) === '0'; } },
    { k: 'verde', i: 'leaf', l: '100% renovável', f: function (o) { return o.f.charAt(1) === '1'; } }
  ];

  var S = {
    data: null, erro: false,
    kwhMes: 1900 / 12, pot: 2, tarifa: 'auto', vazio: 40, atual: 0,
    on: {}, novo: true, open: null, visible: 10, formOpen: false, perfil: 'p1'
  };

  /* ---------- Helpers ---------- */
  function esc(a) { return String(a == null ? '' : a).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function milhar(s) { return s.replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function eur(v) { var p = Math.abs(v).toFixed(2).split('.'); return (v < 0 ? '-' : '') + milhar(p[0]) + ',' + p[1] + '€'; }
  function eurInt(v) { return (v < 0 ? '-' : '') + milhar(String(Math.round(Math.abs(v)))) + '€'; }
  function num(v, d) { return v.toFixed(d).replace('.', ','); }
  function potTxt(p) { return String(p).replace('.', ',') + ' kVA'; }
  function dataPT(iso) {
    var M = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
    var p = String(iso || '').split('-'); if (p.length < 3) return '';
    return parseInt(p[2], 10) + ' de ' + M[parseInt(p[1], 10) - 1] + ' de ' + p[0];
  }
  function ico(path) { return '<svg class="dp-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + path + '</svg>'; }
  var IC = {
    cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    unl: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
    wal: '<path d="M20 12V8H6a2 2 0 0 1 0-4h12v4"/><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/>',
    usr: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    leaf: '<path d="M11 20A7 7 0 0 1 4 13c0-6 7-9 16-9 0 9-3 16-9 16Z"/><path d="M4 20c2-4 5-7 9-9"/>',
    gift: '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    out: '<path d="M7 17 17 7M7 7h10v10"/>'
  };
  var CARET = '<svg class="dp-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>';

  /* ---------- Calculo (metodologia do simulador da ERSE) ---------- */
  function calcOpcao(o, i, kwh, vzShare, novo, k) {
    var p = o[k] && o[k][i];
    if (!p) return null;
    var pot = POTS[i];
    var sh6 = pot <= 6.9 && kwh > 0 ? Math.min(1, LIM_IVA6 / kwh) : 0;
    var ivaE = sh6 * 1.06 + (1 - sh6) * 1.23;
    var kFV = k === 's' ? kwh : kwh * (1 - vzShare), kVz = k === 's' ? 0 : kwh * vzShare;
    var en = k === 's' ? p[1] * kwh : p[1] * kFV + p[2] * kVz;
    var tf = p[0] * 365, tar = TAR_POT[i] * 365;
    var tfIva = pot <= 3.45 ? tar * 1.06 + (tf - tar) * 1.23 : tf * 1.23;
    var enIva = en * ivaE, iec = kwh * IEC * 1.23, cav = CAV * 12 * 1.06;
    function desc(a) { return a ? a[0] + a[1] * tf * 1.23 + (a[2] * en + a[3] * kwh) * ivaE : 0; }
    var reemb = desc(o.r), dNovo = novo ? desc(o.d) : 0, serv = o.cs || 0;
    var total = enIva + tfIva + iec + cav + serv - reemb - dNovo;
    return {
      k: k, total: total, mes: total / 12, p: p,
      energia: en, potencia: tf, iva: (enIva - en) + (tfIva - tf) + kwh * IEC * 0.23 + CAV * 12 * 0.06,
      iec: kwh * IEC, cav: CAV * 12, serv: serv, reemb: reemb, dNovo: dNovo
    };
  }
  function calc(o, i, kwh, vzShare, novo, tarifa) {
    var a = tarifa === 'b' ? null : calcOpcao(o, i, kwh, vzShare, novo, 's');
    var b = tarifa === 's' ? null : calcOpcao(o, i, kwh, vzShare, novo, 'b');
    if (a && b) return a.total <= b.total ? a : b;
    return a || b;
  }

  function resultados() {
    var kwh = S.kwhMes * 12, vz = S.vazio / 100, porCom = {}, reg = null;
    S.data.ofertas.forEach(function (o) {
      var r = calc(o, S.pot, kwh, vz, S.novo, S.tarifa);
      if (!r) return;
      if (o.c === 'TUR') reg = r;
      for (var j = 0; j < FILTROS.length; j++) if (S.on[FILTROS[j].k] && !FILTROS[j].f(o)) return;
      if (!porCom[o.c] || r.total < porCom[o.c].r.total) porCom[o.c] = { o: o, r: r };
    });
    var lista = Object.keys(porCom).map(function (c) { return porCom[c]; });
    lista.sort(function (a, b) { return a.r.total - b.r.total; });
    return { lista: lista, reg: reg };
  }

  /* ---------- Render ---------- */
  function tags(o) {
    var t = [];
    if (o.c === 'TUR') t.push('<span class="dp-tag">Tarifa regulada</span>');
    if (o.f.charAt(3) === '1') t.push('<span class="dp-tag is-warn">Indexada ao mercado</span>');
    if (o.f.charAt(7) === '1') t.push('<span class="dp-tag is-warn">Só novos clientes</span>');
    if (o.f.charAt(0) === '1') t.push('<span class="dp-tag is-warn">Fidelização</span>');
    if (o.f.charAt(4) === '1') t.push('<span class="dp-tag is-warn">Serviços adicionais</span>');
    if (o.f.charAt(2) === '1') t.push('<span class="dp-tag">Condições de acesso</span>');
    return t.join(' ');
  }
  function iniciais(nome) {
    var w = nome.replace(/[^A-Za-zÀ-ÿ ]/g, '').split(' ').filter(Boolean);
    return (w.length > 1 ? w[0].charAt(0) + w[1].charAt(0) : nome.slice(0, 2)).toUpperCase();
  }
  function pagamento(o) {
    var t = [];
    if (o.pg && o.pg.charAt(0) === '1') t.push('débito direto');
    if (o.pg && o.pg.charAt(1) === '1') t.push('multibanco');
    if (o.pg && o.pg.charAt(2) === '1') t.push('outros meios');
    return t.length ? t.join(', ') : 'Não indicado';
  }
  function fatura(o) {
    var t = [];
    if (o.ft && o.ft.charAt(0) === '1') t.push('eletrónica');
    if (o.ft && o.ft.charAt(1) === '1') t.push('em papel');
    return t.length ? t.join(' ou ') : 'Não indicado';
  }

  function cartao(it, idx, base, baseLabel) {
    var o = it.o, r = it.r, nome = NOMES[o.c] || o.c, aberto = S.open === o.id;
    var dif = base != null ? base - r.total : null, poup;
    if (o.c === 'TUR' && !S.atual) poup = '<div class="dp-kpi-v is-plain" style="color:#697386">–</div><div class="dp-kpi-s">é a referência</div>';
    else if (dif == null) poup = '<div class="dp-kpi-v is-plain" style="color:#697386">–</div><div class="dp-kpi-s">&nbsp;</div>';
    else if (dif >= 0.5) poup = '<div class="dp-kpi-v el-pos">' + eurInt(dif) + '</div><div class="dp-kpi-s">a menos por ano</div>';
    else if (dif <= -0.5) poup = '<div class="dp-kpi-v is-plain el-neg">+' + eurInt(-dif) + '</div><div class="dp-kpi-s">a mais por ano</div>';
    else poup = '<div class="dp-kpi-v is-plain">Igual</div><div class="dp-kpi-s">&nbsp;</div>';

    var energiaTxt = num(r.p[1], 4) + '€';
    var energiaSub = r.k === 's' ? 'por kWh, sem IVA' : 'fora de vazio · ' + num(r.p[2], 4) + '€ em vazio';

    var cta = o.u ? '<a class="dp-btn" href="' + esc(o.u) + '" target="_blank" rel="nofollow noopener" data-stop>Ir para a ' + esc(o.c === 'TUR' ? 'SU Eletricidade' : nome) + ico(IC.out) + '</a>' : '';

    var h = '<div class="dp-c' + (aberto ? ' is-open' : '') + '" data-id="' + esc(o.id) + '"><div class="dp-c-main">' +
      '<div class="dp-rank">' + (idx + 1) + '</div>' +
      '<div class="dp-ent"><span class="dp-logo"><span class="dp-logo-ini">' + esc(iniciais(nome)) + '</span></span><div>' +
      '<div class="dp-c-head"><span class="dp-name">' + esc(nome) + '</span></div>' +
      '<div class="dp-prod">' + esc(o.n) + '</div>' + tags(o) + '</div></div>' +
      '<div class="dp-kpis">' +
      '<div class="dp-kpi"><div class="dp-kpi-l">Fatura por mês</div><div class="dp-kpi-v">' + eur(r.mes) + '</div><div class="dp-kpi-s">' + eurInt(r.total) + ' por ano</div></div>' +
      '<div class="dp-kpi"><div class="dp-kpi-l">Tarifa</div><div class="dp-kpi-v is-plain">' + (r.k === 's' ? 'Simples' : 'Bi-horária') + '</div><div class="dp-kpi-s">' + (S.tarifa === 'auto' ? 'a mais barata para ti' : '&nbsp;') + '</div></div>' +
      '<div class="dp-kpi"><div class="dp-kpi-l">Energia</div><div class="dp-kpi-v is-plain">' + energiaTxt + '</div><div class="dp-kpi-s">' + energiaSub + '</div></div>' +
      '<div class="dp-kpi"><div class="dp-kpi-l">Potência</div><div class="dp-kpi-v is-plain">' + num(r.p[0], 4) + '€</div><div class="dp-kpi-s">por dia, sem IVA</div></div>' +
      '<div class="dp-kpi"><div class="dp-kpi-l">' + esc(baseLabel) + '</div>' + poup + '</div>' +
      '</div>' +
      '<div class="dp-c-cta">' + cta + '<span class="dp-kpi-s">' + (o.f.charAt(3) === '1' ? 'Preço varia com o mercado' : (o.du ? 'Contrato de ' + o.du + (o.du === 1 ? ' mês' : ' meses') : '&nbsp;')) + '</span></div></div>';

    if (aberto) {
      var kv = function (a, b) { return '<div class="dp-kv"><span>' + a + '</span><span>' + b + '</span></div>'; };
      var linhas = '<table class="dp-sub"><thead><tr><th>Parcela</th><th class="num">Por ano</th></tr></thead><tbody>' +
        '<tr><td>Energia (' + milhar(String(Math.round(S.kwhMes * 12))) + ' kWh)</td><td class="num">' + eur(r.energia) + '</td></tr>' +
        '<tr><td>Potência contratada (' + potTxt(POTS[S.pot]) + ')</td><td class="num">' + eur(r.potencia) + '</td></tr>' +
        '<tr><td>Imposto especial de consumo</td><td class="num">' + eur(r.iec) + '</td></tr>' +
        '<tr><td>Contribuição audiovisual</td><td class="num">' + eur(r.cav) + '</td></tr>' +
        '<tr><td>IVA</td><td class="num">' + eur(r.iva) + '</td></tr>' +
        (r.serv ? '<tr><td>Serviços adicionais obrigatórios</td><td class="num">' + eur(r.serv) + '</td></tr>' : '') +
        (r.reemb ? '<tr><td>Descontos e reembolsos</td><td class="num">-' + eur(r.reemb) + '</td></tr>' : '') +
        (r.dNovo ? '<tr><td>Desconto de novo cliente (1.º ano)</td><td class="num">-' + eur(r.dNovo) + '</td></tr>' : '') +
        '<tr class="is-on"><td>Total</td><td class="num">' + eur(r.total) + '</td></tr></tbody></table>';
      var cond = kv('Tipo de preço', o.c === 'TUR' ? 'Regulado pela ERSE' : (o.f.charAt(3) === '1' ? 'Indexado ao mercado grossista' : 'Fixo')) +
        kv('Fidelização', o.f.charAt(0) === '1' ? 'Sim' : 'Não') +
        kv('Duração do contrato', o.du ? o.du + (o.du === 1 ? ' mês' : ' meses') : 'Não indicada') +
        kv('Pagamento', esc(pagamento(o))) + kv('Fatura', esc(fatura(o))) +
        kv('Energia 100% renovável', o.f.charAt(1) === '1' ? 'Sim' : 'Não') +
        kv('Tarifa social', o.f.charAt(5) === '1' ? 'Disponível' : 'Não disponível') +
        (o.m ? kv('Modalidade', esc(o.m)) : '');
      var notas = [];
      if (o.f.charAt(3) === '1') notas.push('Preço indexado: o valor mostrado é uma estimativa da ERSE com base no preço esperado do mercado grossista para os próximos três meses. A fatura real sobe e desce com o mercado.');
      if (o.tr) notas.push('Condições de acesso: ' + o.tr);
      if (o.ts) notas.push('Serviços adicionais: ' + o.ts);
      if (o.d && !S.novo) notas.push('Esta oferta tem um desconto para novos clientes que não está contado.');
      if (o.fim) notas.push('Preços comunicados à ERSE com validade até ' + o.fim + '.');
      h += '<div class="dp-c-detail"><div class="dp-detail-grid"><div><div class="dp-h">Como se chega a ' + eur(r.total) + ' por ano</div>' + linhas +
        '</div><div><div class="dp-h">Condições</div>' + cond + (notas.length ? '<ul class="dp-notes"><li>' + notas.map(esc).join('</li><li>') + '</li></ul>' : '') + '</div></div></div>';
    }
    return h + '<button type="button" class="dp-c-toggle" data-toggle>' + (aberto ? 'Menos detalhes' : 'Ver as contas e as condições') + CARET + '</button></div>';
  }

  var AR = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  function cabecalho() {
    var n = S.data ? Object.keys(S.data.ofertas.reduce(function (m, o) { m[o.c] = 1; return m; }, {})).length : 0;
    return '<div class="max-width-37-5 dp-lead"><div class="text-color-secondary"><div class="text-size-large"><div class="text-align-center">' +
      'Indica o teu consumo e vê quanto pagas por mês em ' + (n ? n + ' comercializadores' : 'cada comercializador') + '. Os preços são os que as empresas comunicam à ERSE, o regulador da energia.' +
      '</div></div></div></div>' +
      '<div class="dp-meta"><div class="dp-authors">' +
      '<a class="dp-author" href="https://www.literaciafinanceira.pt/autores/franklin-silva"><img class="dp-author-img" src="https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0ae5bc67fe0ef48466e_franklin-silva.avif" alt="Franklin Silva"><span><span class="dp-author-l">Autor</span><span class="dp-author-n">Franklin Silva</span></span></a>' +
      '<a class="dp-author" href="https://www.literaciafinanceira.pt/autores/pedro-braz"><img class="dp-author-img" src="https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0f9b80a20ec1767fab5_Pedro-Braz.avif" alt="Pedro Braz"><span><span class="dp-author-l">Revisor</span><span class="dp-author-n">Pedro Braz</span></span></a>' +
      '<span class="dp-author dp-author-date"><span class="dp-author-ico">' + ico(IC.cal) + '</span><span><span class="dp-author-l">Preços atualizados</span><span class="dp-author-n">' + (S.data ? dataPT(S.data.atualizado) : '...') + '</span></span></span>' +
      '</div></div>';
  }

  function render() {
    var root = document.getElementById('lf-dp');
    if (!root) return;
    if (S.erro) { root.innerHTML = cabecalho() + '<div class="dp-empty">Não foi possível carregar os preços. Atualiza a página dentro de momentos.</div>'; return; }
    if (!S.data) { root.innerHTML = cabecalho() + '<div class="dp-empty">A carregar os preços...</div>'; return; }

    var res = resultados(), lista = res.lista, vis = lista.slice(0, S.visible);
    var base = S.atual > 0 ? S.atual * 12 : (res.reg ? res.reg.total : null);
    var baseLabel = S.atual > 0 ? 'Face à tua fatura' : 'Face ao regulado';

    var potOpts = POTS.map(function (p, i) { return '<option value="' + i + '"' + (S.pot === i ? ' selected' : '') + '>' + potTxt(p) + '</option>'; }).join('');
    var tarifas = [['auto', 'A mais barata'], ['s', 'Simples'], ['b', 'Bi-horária']].map(function (t) {
      return '<button type="button" class="dp-tab' + (S.tarifa === t[0] ? ' is-active' : '') + '" data-tarifa="' + t[0] + '">' + t[1] + '</button>';
    }).join('');
    var vzOpts = [20, 30, 40, 50, 60, 70].map(function (v) { return '<option value="' + v + '"' + (S.vazio === v ? ' selected' : '') + '>' + v + '% em vazio</option>'; }).join('');
    var perfis = PERFIS.map(function (p) {
      return '<button type="button" class="dp-irs-b' + (S.perfil === p.k ? ' is-on' : '') + '" data-perfil="' + p.k + '">' + p.l + '</button>';
    }).join('');
    var chips = FILTROS.map(function (f) {
      return '<button type="button" class="dp-chip' + (S.on[f.k] ? ' is-on' : '') + '" data-f="' + f.k + '">' + ico(IC[f.i]) + esc(f.l) + '</button>';
    }).join('') + '<button type="button" class="dp-chip' + (S.novo ? ' is-on' : '') + '" data-novo>' + ico(IC.gift) + 'Contar descontos de novo cliente</button>';

    var AD = '<div class="table-results_wrapper is-pub dp-ad-card"><a class="button-arrow is-trigger w-inline-block" href="https://www.literaciafinanceira.pt/visita/trade-republic" target="_blank" rel="nofollow sponsored" data-stop><div class="calc-banner_wrapper"><div class="pub_wrapper"><div class="pub-left_wrapper"><div class="pub-logo-text_wrapper"><div class="pub-logo_wrapper is-big"><div class="pub-text-logo_wrapper"><div class="text-size-caps"><div class="text-color-quarterary"><div class="text-weight-medium">Anúncio</div></div></div><img class="image-102" src="https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf09/681e26cb7eaca82c7095d5c7_Trade_Republic_logo_2021.svg.avif" alt="logo Trade Republic" loading="lazy"></div><div class="pub-line-divider is-full-height"></div><div class="pub-title_wrapper"><div class="text-color-primary"><div class="text-size-large"><div class="text-weight-semibold">Ganha 3,00% em juros, até 50.000€ (novos clientes)</div></div></div><div class="max-width-31"><div class="text-color-tertiary"><div class="text-size-extra-extra-small is-0-75-mobile">Pagamentos mensais na tua conta. Flexibilidade total. Investir envolve risco. Este conteúdo é uma comunicação comercial da Trade Republic Bank GmbH.</div></div></div></div></div></div></div><div class="pub-right_wrapper"><div class="hide-mobile-landscape"><div class="button-arrow"><div class="text-weight-medium"><div class="text-size-small"><div class="text-weight-medium"><div>Sabe mais</div></div></div></div><div class="button-arrow_wrapper"><div class="button-arrow-icon w-embed">' + AR + '</div></div></div></div><div class="visible-mobile-landscape"><div class="banner-button-position"><div class="rotate-45"><div class="button-arrow_wrapper"><div class="button-arrow-icon w-embed">' + AR + '</div></div></div></div></div></div></div></div></a></div>';

    var cards = '';
    vis.forEach(function (it, i) { cards += cartao(it, i, base, baseLabel); if (i === 2) cards += AD; });
    if (vis.length && vis.length < 3) cards += AD;

    var resumo = milhar(String(Math.round(S.kwhMes))) + ' kWh por mês · ' + potTxt(POTS[S.pot]) + ' · ' + (S.tarifa === 'auto' ? 'Tarifa mais barata' : S.tarifa === 's' ? 'Simples' : 'Bi-horária');

    root.innerHTML = cabecalho() +
      '<div class="dp-card' + (S.formOpen ? ' is-open' : '') + '"><button type="button" class="dp-card-toggle" data-cardtoggle aria-expanded="' + (S.formOpen ? 'true' : 'false') + '"><span><span class="dp-card-toggle-t">Consumo, potência e tarifa</span><span class="dp-card-toggle-s">' + resumo + '</span></span>' + CARET + '</button>' +
      '<div class="dp-card-body"><div class="dp-form el-form">' +
      '<div><label class="dp-label" for="elKwh">Consumo por mês</label><div class="dp-input-wrap"><input id="elKwh" class="dp-input el-input-unit" type="text" inputmode="numeric" autocomplete="off" value="' + milhar(String(Math.round(S.kwhMes))) + '"><span class="dp-input-unit">kWh</span></div></div>' +
      '<div><span class="dp-label">Tarifa</span><div class="dp-toggle el-toggle3">' + tarifas + '</div></div>' +
      '<div><label class="dp-label" for="elPot">Potência contratada</label><select class="dp-input dp-input-select" id="elPot">' + potOpts + '</select></div>' +
      '</div><div class="dp-form el-form el-form2">' +
      '<div><label class="dp-label" for="elAtual">Fatura atual (opcional)</label><div class="dp-input-wrap"><input id="elAtual" class="dp-input el-input-unit2" type="text" inputmode="decimal" autocomplete="off" placeholder="0" value="' + (S.atual ? String(S.atual).replace('.', ',') : '') + '"><span class="dp-input-unit">€/mês</span></div></div>' +
      '<div><span class="dp-label">Não sabes o teu consumo? Escolhe o caso mais parecido</span><div class="el-perfis">' + perfis + '</div></div>' +
      '<div' + (S.tarifa === 's' ? ' class="el-off"' : '') + '><label class="dp-label" for="elVazio">Consumo em vazio</label><select class="dp-input dp-input-select" id="elVazio"' + (S.tarifa === 's' ? ' disabled' : '') + '>' + vzOpts + '</select></div>' +
      '</div><p class="dp-form-note">O consumo em kWh e a potência contratada estão na tua fatura. O vazio é o consumo à noite e, no ciclo semanal, ao fim de semana.</p></div></div>' +
      '<div class="dp-bar"><div class="dp-chips">' + chips + '</div></div>' +
      (lista.length ? '<div class="dp-cards">' + cards + '</div>' : '<div class="dp-empty">Nenhuma oferta cumpre estes filtros para ' + potTxt(POTS[S.pot]) + '. Tira um filtro ou muda a tarifa.</div>') +
      (lista.length > vis.length ? '<div class="dp-more"><button type="button" class="dp-btn is-secondary" id="elMore">Mostrar mais ' + (lista.length - vis.length) + '</button></div>' : '') +
      '<p class="dp-foot">Preços das ofertas comunicadas pelos comercializadores à ERSE, atualizados a ' + dataPT(S.data.atualizado) + '. Mostramos a oferta mais barata de cada comercializador para o teu consumo, em Portugal continental, para clientes domésticos e só de eletricidade (sem pacotes com gás). ' +
      'A fatura inclui energia, potência, IVA, imposto especial de consumo e contribuição audiovisual, segue a metodologia do simulador da ERSE e não inclui a taxa de exploração da DGEG (0,07€ por mês). ' +
      'Os descontos de novo cliente valem só no primeiro ano. Confirma sempre as condições no site do comercializador antes de mudares.</p>';
  }

  /* ---------- Eventos ---------- */
  function refocus(id) {
    var el = document.getElementById(id);
    if (el) { el.focus(); if (el.setSelectionRange && el.value) el.setSelectionRange(el.value.length, el.value.length); }
  }
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t.closest || !t.closest('#lf-dp') || t.closest('[data-stop]')) return;
    if (t.closest('[data-cardtoggle]')) { S.formOpen = !S.formOpen; render(); return; }
    var a = t.closest('[data-tarifa]');
    if (a) { S.tarifa = a.getAttribute('data-tarifa'); S.visible = 10; render(); return; }
    var p = t.closest('[data-perfil]');
    if (p) {
      var pf = PERFIS.filter(function (x) { return x.k === p.getAttribute('data-perfil'); })[0];
      if (pf) { S.perfil = pf.k; S.kwhMes = pf.kwh / 12; S.pot = pf.pot; S.visible = 10; render(); }
      return;
    }
    if (t.closest('[data-novo]')) { S.novo = !S.novo; render(); return; }
    var c = t.closest('.dp-chip');
    if (c) { var k = c.getAttribute('data-f'); if (S.on[k]) delete S.on[k]; else S.on[k] = true; S.visible = 10; render(); return; }
    if (t.closest('#elMore')) { S.visible += 10; render(); return; }
    var g = t.closest('[data-toggle]');
    if (g) { var id = g.closest('.dp-c').getAttribute('data-id'); S.open = S.open === id ? null : id; render(); }
  });
  document.addEventListener('input', function (e) {
    var id = e.target && e.target.id;
    if (id === 'elKwh') {
      var v = parseInt(String(e.target.value).replace(/\D/g, ''), 10);
      e.target.value = isNaN(v) ? '' : milhar(String(v));
      clearTimeout(window.__elT);
      window.__elT = setTimeout(function () {
        S.kwhMes = isNaN(v) || v < 0 ? 0 : Math.min(v, 5000); S.perfil = null;
        var foco = document.activeElement && document.activeElement.id === 'elKwh';
        render(); if (foco) refocus('elKwh');
      }, 350);
    }
    if (id === 'elAtual') {
      var raw = String(e.target.value).replace(/[^\d,\.]/g, '').replace('.', ',');
      e.target.value = raw;
      clearTimeout(window.__elT2);
      window.__elT2 = setTimeout(function () {
        var n = parseFloat(raw.replace(',', '.'));
        S.atual = isNaN(n) || n < 0 ? 0 : n;
        var foco = document.activeElement && document.activeElement.id === 'elAtual';
        render(); if (foco) refocus('elAtual');
      }, 450);
    }
  });
  document.addEventListener('change', function (e) {
    var id = e.target && e.target.id;
    if (id === 'elPot') { S.pot = parseInt(e.target.value, 10) || 0; S.perfil = null; S.visible = 10; render(); }
    if (id === 'elVazio') { S.vazio = parseInt(e.target.value, 10) || 40; render(); }
  });

  /* Formato compacto do JSON: s = [termosFixos[10], precoKwh], b = [termosFixos[10] ou 1 (= os de s), foraVazio, vazio].
     Cada preco de energia e um numero (igual em todas as potencias) ou uma lista por potencia. Expande para [[tf, ...], ...]. */
  function expandir(o) {
    function v(x, i) { return typeof x === 'number' ? x : x[i]; }
    var s = o.s, b = o.b, tfS = s && s.length === 2 && Array.isArray(s[0]) && s[0].length === 10 && !Array.isArray(s[0][0]) ? s[0] : null;
    if (tfS) o.s = tfS.map(function (tf, i) { return tf ? [tf, v(s[1], i)] : 0; });
    if (b && b.length === 3 && (b[0] === 1 || (Array.isArray(b[0]) && !Array.isArray(b[0][0])))) {
      var tfB = b[0] === 1 ? tfS : b[0];
      o.b = tfB.map(function (tf, i) { return tf && v(b[1], i) ? [tf, v(b[1], i), v(b[2], i)] : 0; });
    }
  }

  /* ---------- Arranque ---------- */
  function montar() {
    if (!document.getElementById('lf-dp')) {
      var alvo = document.getElementById('lf-pc-calc'), div = document.createElement('div');
      div.id = 'lf-dp';
      if (alvo) alvo.parentNode.replaceChild(div, alvo);
      else { var h1 = document.querySelector('h1.heading-style-h2'); if (h1 && h1.parentNode) h1.parentNode.appendChild(div); else return; }
    }
    render();
    var x = new XMLHttpRequest();
    x.open('GET', DATA_URL + '?d=' + new Date().toISOString().slice(0, 10));
    x.onload = function () {
      try { var d = JSON.parse(x.responseText); if (!d.ofertas || !d.ofertas.length) throw 0; d.ofertas.forEach(expandir); S.data = d; } catch (err) { S.erro = true; }
      render();
    };
    x.onerror = function () { S.erro = true; render(); };
    x.send();
  }
  window.__lfElCalc = calc; window.__lfElExpandir = expandir;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', montar); else montar();
})();
