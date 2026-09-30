/* Tabelas de IRS 2026 - literaciafinanceira.pt
   Escaloes: artigo 68.o do Codigo do IRS, redacao da Lei n.o 73-A/2025 (OE 2026).
   Retencao na fonte (continente): Despacho n.o 233-A/2026, de 6 de janeiro, Tabelas I a III.
   Reutiliza o CSS do comparador de depositos (#lf-dp .dp-*) mais tabelas-irs.css. */
(function () {
  'use strict';
  if (window.__lfIrsInit) return;
  window.__lfIrsInit = true;

  var VERIFICADO = '30 de setembro de 2026';
  var IAS = 537.13, DED_ESP = 8.54 * IAS, MIN_EXIST = 12880;
  /* [limite superior do rendimento coletavel, taxa, parcela a abater] */
  var ESC = [
    [8342, 12.5, 0], [12587, 15.7, 266.94], [17838, 21.2, 959.23], [23089, 24.1, 1476.53], [29397, 31.1, 3092.76],
    [43090, 34.9, 4209.85], [46566, 43.1, 7743.23], [86634, 44.6, 8441.72], [Infinity, 48, 11387.27]
  ];
  var MEDIA = ['12,500%', '13,579%', '15,823%', '17,705%', '20,579%', '25,130%', '26,472%', '34,856%', '–'];
  /* [remuneracao mensal ate, taxa marginal maxima, parcela a abater, parcela adicional por dependente] */
  var RET = [
    { k: 'I', l: 'Tabela I', t: 'Não casado sem dependentes ou casado com dois titulares', r: [
      ['920,00', '0,00%', '0,00', '0,00'], ['1 042,00', '12,50%', '12,50% × 2,60 × (1 273,85 − R)', '21,43'],
      ['1 108,00', '15,70%', '15,70% × 1,35 × (1 554,83 − R)', '21,43'], ['1 154,00', '15,70%', '94,71', '21,43'],
      ['1 212,00', '21,20%', '158,18', '21,43'], ['1 819,00', '24,10%', '193,33', '21,43'], ['2 119,00', '31,10%', '320,66', '21,43'],
      ['2 499,00', '34,90%', '401,19', '21,43'], ['3 305,00', '38,36%', '487,66', '21,43'], ['5 547,00', '39,69%', '531,62', '21,43'],
      ['20 221,00', '44,95%', '823,40', '21,43'], ['>20 221,00', '47,17%', '1 272,31', '21,43']] },
    { k: 'II', l: 'Tabela II', t: 'Não casado com um ou mais dependentes', r: [
      ['920,00', '0,00%', '0,00', '0,00'], ['1 042,00', '12,50%', '12,50% × 2,60 × (1 273,85 − R)', '34,29'],
      ['1 108,00', '15,70%', '15,70% × 1,35 × (1 554,83 − R)', '34,29'], ['1 154,00', '15,70%', '94,71', '34,29'],
      ['1 212,00', '21,20%', '158,18', '34,29'], ['1 819,00', '24,10%', '193,33', '34,29'], ['2 119,00', '31,10%', '320,66', '34,29'],
      ['2 499,00', '34,90%', '401,19', '34,29'], ['3 305,00', '38,36%', '487,66', '34,29'], ['5 547,00', '39,69%', '531,62', '34,29'],
      ['20 221,00', '44,95%', '823,40', '34,29'], ['>20 221,00', '47,17%', '1 272,31', '34,29']] },
    { k: 'III', l: 'Tabela III', t: 'Casado, único titular', r: [
      ['991,00', '0,00%', '0,00', '0,00'], ['1 042,00', '12,50%', '12,50% × 2,60 × (1 372,15 − R)', '42,86'],
      ['1 108,00', '12,50%', '12,50% × 1,35 × (1 677,85 − R)', '42,86'], ['1 119,00', '12,50%', '96,17', '42,86'],
      ['1 432,00', '12,72%', '98,64', '42,86'], ['1 962,00', '15,70%', '141,32', '42,86'], ['2 240,00', '19,38%', '213,53', '42,86'],
      ['2 773,00', '22,77%', '289,47', '42,86'], ['3 389,00', '25,70%', '370,72', '42,86'], ['5 965,00', '28,81%', '476,12', '42,86'],
      ['20 265,00', '38,43%', '1 049,96', '42,86'], ['>20 265,00', '47,17%', '2 821,13', '42,86']] }
  ];
  var L = {
    lei: 'https://diariodarepublica.pt/dr/detalhe/lei/73-a-2025-993270096',
    art68: 'https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cirs_rep/Pages/irs68.aspx',
    desp: 'https://diariodarepublica.pt/dr/detalhe/despacho/233-a-2026-998488151',
    circ: 'https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/legislacao/instrucoes_administrativas/Documents/Circular_1_2026.pdf',
    prop: 'https://eco.sapo.pt/2026/09/21/governo-ja-entregou-proposta-para-reduzir-irs-no-parlamento/',
    sal: 'https://www.literaciafinanceira.pt/simulador-salario-liquido'
  };

  var S = { bruto: 21000, tab: 'I', res: null };

  function milhar(s) { return s.replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function eur(v) { var p = Math.abs(v).toFixed(2).split('.'); return (v < 0 ? '-' : '') + milhar(p[0]) + ',' + p[1] + '€'; }
  function eurInt(v) { return milhar(String(Math.round(v))) + '€'; }
  function pct(v, d) { return v.toFixed(d).replace('.', ',') + '%'; }
  function pontos(s) { return s.replace(/(\d) (\d)/g, '$1.$2'); }
  function ico(path) { return '<svg class="dp-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + path + '</svg>'; }
  var CAL = '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>';

  function calcular(bruto) {
    var ss = bruto * 0.11, ded = Math.max(DED_ESP, ss), col = Math.max(0, bruto - ded), i = 0;
    while (col > ESC[i][0]) i++;
    var coleta = Math.max(0, col * ESC[i][1] / 100 - ESC[i][2]);
    return { bruto: bruto, ded: ded, col: col, i: i, taxa: ESC[i][1], coleta: coleta, media: col > 0 ? coleta / col * 100 : 0, isento: bruto <= MIN_EXIST };
  }

  function tabEscaloes(on) {
    var h = '<div class="irs-box"><table class="irs-t"><thead><tr><th>Escalão</th><th>Rendimento coletável</th><th class="num">Taxa</th><th class="num">Taxa média</th><th class="num">Parcela a abater</th></tr></thead><tbody>';
    ESC.forEach(function (e, i) {
      var de = i ? ESC[i - 1][0] : 0;
      var faixa = i === 0 ? 'Até ' + eurInt(e[0]) : e[0] === Infinity ? 'Mais de ' + eurInt(de) : 'De ' + eurInt(de) + ' a ' + eurInt(e[0]);
      h += '<tr' + (on === i ? ' class="is-on"' : '') + '><td>' + (i + 1) + '.º</td><td>' + faixa + '</td><td class="num">' + pct(e[1], 1) + '</td><td class="num">' + MEDIA[i] + '</td><td class="num">' + eur(e[2]) + '</td></tr>';
    });
    return h + '</tbody></table></div>';
  }
  function tabRetencao() {
    var t = RET.filter(function (x) { return x.k === S.tab; })[0];
    var h = '<div class="irs-box"><table class="irs-t"><thead><tr><th>Remuneração mensal</th><th class="num">Taxa</th><th class="num">Parcela a abater</th><th class="num">Por dependente</th></tr></thead><tbody>';
    t.r.forEach(function (r) {
      var ate = r[0].charAt(0) === '>' ? 'Mais de ' + pontos(r[0].slice(1)) + '€' : 'Até ' + pontos(r[0]) + '€';
      h += '<tr><td>' + ate + '</td><td class="num">' + r[1] + '</td><td class="num">' + pontos(r[2]) + (r[2].indexOf('×') > -1 ? '' : '€') + '</td><td class="num">' + r[3] + '€</td></tr>';
    });
    return h + '</tbody></table></div>';
  }

  function resultado() {
    var r = S.res;
    if (!r) return '';
    var row = function (a, b, hl) { return '<div class="irs-row' + (hl ? ' is-hl' : '') + '"><span>' + a + '</span><span>' + b + '</span></div>'; };
    var resumo = r.isento
      ? 'Com <strong>' + eurInt(r.bruto) + '</strong> brutos por ano ficas dentro do mínimo de existência (' + eurInt(MIN_EXIST) + '): <strong>não pagas IRS</strong>, mesmo que a conta pelos escalões dê imposto.'
      : 'Com <strong>' + eurInt(r.bruto) + '</strong> brutos por ano, o teu rendimento coletável é de <strong>' + eur(r.col) + '</strong> e ficas no <strong>' + (r.i + 1) + '.º escalão</strong>. A taxa de ' + pct(r.taxa, 1) + ' só se aplica à parte do rendimento que cai nesse escalão. No total, o imposto é de <strong>' + eur(r.coleta) + '</strong> antes das deduções à coleta (despesas de saúde, educação, habitação e dependentes), que baixam este valor.';
    return '<div class="irs-res" id="irsRes">' +
      row('Escalão de IRS', (r.i + 1) + '.º escalão', true) +
      row('Taxa do escalão (marginal)', pct(r.taxa, 1)) +
      row('Dedução específica', eur(r.ded)) +
      row('Rendimento coletável', eur(r.col)) +
      row('IRS antes das deduções à coleta', eur(r.isento ? 0 : r.coleta)) +
      row('Taxa média sobre o rendimento coletável', pct(r.isento ? 0 : r.media, 2)) +
      '<p class="irs-resumo">' + resumo + '</p>' +
      '<p class="dp-foot">Cálculo para um titular, com rendimentos só de trabalho por conta de outrem, em Portugal continental e sem tributação conjunta. A dedução específica é o maior valor entre ' + eur(DED_ESP) + ' (8,54 × IAS) e os descontos para a Segurança Social (11%). Não é aconselhamento fiscal.</p></div>';
  }

  function render() {
    var root = document.getElementById('lf-dp');
    if (!root) return;
    var tabs = RET.map(function (t) { return '<button type="button" class="dp-tab' + (S.tab === t.k ? ' is-active' : '') + '" data-tab="' + t.k + '">' + t.l + '</button>'; }).join('');
    var atual = RET.filter(function (x) { return x.k === S.tab; })[0];
    root.innerHTML =
      '<div class="max-width-37-5 dp-lead"><div class="text-color-secondary"><div class="text-size-large"><div class="text-align-center">Os escalões de IRS e as tabelas de retenção na fonte em vigor em 2026, com os valores oficiais. Vê em que escalão estás e quanto te podem reter no salário.</div></div></div></div>' +
      '<div class="dp-meta"><div class="dp-authors">' +
      '<a class="dp-author" href="https://www.literaciafinanceira.pt/autores/franklin-silva"><img class="dp-author-img" src="https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0ae5bc67fe0ef48466e_franklin-silva.avif" alt="Franklin Silva"><span><span class="dp-author-l">Autor</span><span class="dp-author-n">Franklin Silva</span></span></a>' +
      '<a class="dp-author" href="https://www.literaciafinanceira.pt/autores/pedro-braz"><img class="dp-author-img" src="https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf20/683ee0f9b80a20ec1767fab5_Pedro-Braz.avif" alt="Pedro Braz"><span><span class="dp-author-l">Revisor</span><span class="dp-author-n">Pedro Braz</span></span></a>' +
      '<span class="dp-author dp-author-date"><span class="dp-author-ico">' + ico(CAL) + '</span><span><span class="dp-author-l">Última verificação</span><span class="dp-author-n">' + VERIFICADO + '</span></span></span>' +
      '</div></div>' +

      '<div class="irs-card"><p class="irs-card-t">Em que escalão de IRS estás?</p><p class="irs-card-s">Indica o teu rendimento bruto anual (salário bruto × 14 meses).</p>' +
      '<div class="irs-form"><div><label class="dp-label" for="irsBruto">Rendimento bruto anual</label><div class="dp-input-wrap"><input id="irsBruto" class="dp-input" type="text" inputmode="numeric" autocomplete="off" value="' + milhar(String(S.bruto)) + '"><span class="dp-input-unit">€</span></div></div>' +
      '<div><label class="dp-label" for="irsMes">Ou o salário bruto mensal</label><div class="dp-input-wrap"><input id="irsMes" class="dp-input" type="text" inputmode="numeric" autocomplete="off" value="' + milhar(String(Math.round(S.bruto / 14))) + '"><span class="dp-input-unit">€</span></div></div>' +
      '<button type="button" class="dp-btn" id="irsCalc">Calcular</button></div>' + resultado() + '</div>' +

      '<div class="irs-sec"><h2 class="irs-h2">Escalões de IRS 2026</h2>' +
      '<p class="irs-p">Os escalões aplicam-se ao rendimento coletável de 2026, que declaras em 2027. Foram fixados pelo <a href="' + L.lei + '" target="_blank" rel="noopener">Orçamento do Estado para 2026 (Lei n.º 73-A/2025)</a>, que alterou o <a href="' + L.art68 + '" target="_blank" rel="noopener">artigo 68.º do Código do IRS</a>: os limites subiram 3,51% e as taxas do 2.º ao 5.º escalão desceram 0,3 pontos percentuais.</p>' +
      tabEscaloes(S.res && !S.res.isento ? S.res.i : -1) +
      '<p class="dp-foot">IRS = rendimento coletável × taxa do escalão − parcela a abater. A parcela a abater é calculada por nós a partir das taxas da lei e dá o mesmo resultado que aplicar cada taxa à sua fatia de rendimento. Rendimentos coletáveis acima de 80.000€ pagam ainda a taxa adicional de solidariedade (2,5% até 250.000€ e 5% acima).</p>' +
      '<div class="irs-aviso"><div><strong>Pode mudar ainda em 2026:</strong> o Governo entregou no Parlamento, a 21 de setembro de 2026, uma proposta para baixar as taxas do 1.º ao 6.º escalão (para 12,2%, 15,2%, 20,7%, 23,6%, 30,6% e 34,6%), com efeitos em todo o ano de 2026 e novas tabelas de retenção a partir de novembro. À data da última verificação ainda não era lei. <a href="' + L.prop + '" target="_blank" rel="noopener">Fonte: ECO</a>.</div></div></div>' +

      '<div class="irs-sec"><h2 class="irs-h2">Tabelas de retenção na fonte 2026</h2>' +
      '<p class="irs-p">A retenção na fonte é o IRS que a entidade patronal desconta todos os meses no teu salário, por conta do imposto final. As tabelas de 2026 para o continente estão no <a href="' + L.desp + '" target="_blank" rel="noopener">Despacho n.º 233-A/2026, de 6 de janeiro</a>, e aplicam-se desde 1 de janeiro. Escolhe a tabela da tua situação familiar.</p>' +
      '<div class="irs-tabs">' + tabs + '</div><p class="irs-p" style="margin-bottom:12px"><strong>' + atual.l + ':</strong> ' + atual.t.charAt(0).toLowerCase() + atual.t.slice(1) + ' (trabalho dependente).</p>' +
      tabRetencao() +
      '<p class="dp-foot">Retenção = R × taxa − parcela a abater − (parcela por dependente × número de dependentes), em que R é a remuneração mensal bruta. Exemplo na Tabela I, com 1.500€ e sem dependentes: 1.500€ × 24,10% − 193,33€ = 168,17€. O despacho tem mais oito tabelas, para pessoas com deficiência e para pensões, e os Açores e a Madeira têm tabelas próprias. Para o valor exato do teu salário líquido, usa o <a href="' + L.sal + '" style="color:inherit;text-decoration:underline">simulador de salário líquido</a>.</p>' +
      '<ul class="irs-fontes"><li><a href="' + L.lei + '" target="_blank" rel="noopener">Lei n.º 73-A/2025, de 30 de dezembro</a> (Orçamento do Estado para 2026): escalões de IRS.</li><li><a href="' + L.desp + '" target="_blank" rel="noopener">Despacho n.º 233-A/2026, de 6 de janeiro</a>: tabelas de retenção na fonte do continente.</li><li><a href="' + L.circ + '" target="_blank" rel="noopener">Circular n.º 1/2026 da Autoridade Tributária</a>: instruções de aplicação das tabelas.</li></ul></div>';
  }

  function num(id) { var el = document.getElementById(id); return el ? parseInt(String(el.value).replace(/\D/g, ''), 10) || 0 : 0; }
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t.closest || !t.closest('#lf-dp')) return;
    var tab = t.closest('[data-tab]');
    if (tab) { S.tab = tab.getAttribute('data-tab'); render(); return; }
    if (t.closest('#irsCalc')) {
      S.bruto = Math.min(num('irsBruto'), 100000000);
      S.res = calcular(S.bruto);
      render();
      var r = document.getElementById('irsRes');
      if (r && r.scrollIntoView) r.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
  document.addEventListener('input', function (e) {
    var id = e.target && e.target.id;
    if (id !== 'irsBruto' && id !== 'irsMes') return;
    var v = parseInt(String(e.target.value).replace(/\D/g, ''), 10);
    e.target.value = isNaN(v) ? '' : milhar(String(v));
    var outro = document.getElementById(id === 'irsBruto' ? 'irsMes' : 'irsBruto');
    if (outro) outro.value = isNaN(v) ? '' : milhar(String(id === 'irsBruto' ? Math.round(v / 14) : v * 14));
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target && (e.target.id === 'irsBruto' || e.target.id === 'irsMes')) { var b = document.getElementById('irsCalc'); if (b) b.click(); }
  });

  function montar() {
    if (!document.getElementById('lf-dp')) {
      var h1 = document.querySelector('h1.heading-style-h2'), div = document.createElement('div');
      div.id = 'lf-dp';
      if (h1 && h1.parentNode) h1.parentNode.appendChild(div); else return;
    }
    render();
  }
  window.__lfIrsCalc = calcular;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', montar); else montar();
})();
