/* STAGING (21 set 2026): carrega o JS de produção e aplica por cima a alteração em teste:
   "mais X prazos" passa a link que abre o cartão e desliza até à tabela "Taxas por prazo".
   Quando for aprovado, a mesma alteração vai para scripts/comparador-template.js e este ficheiro volta a ser só o loader. */
(function(){
  var P=[["return q>0?\"mais \"+q+(q>1?\" prazos\":\" prazo\"):\"&nbsp;\"","return q>0?'<button type=\"button\" class=\"dp-more-prazos\" data-prazos>mais '+q+(q>1?\" prazos\":\" prazo\")+\"</button>\":\"&nbsp;\""],["var e=o.closest(\"[data-toggle]\");","var PZ=o.closest(\"[data-prazos]\");if(PZ){var ID=PZ.closest(\".dp-c\").getAttribute(\"data-id\");d.open=ID,k();var SEL=window.CSS&&CSS.escape?CSS.escape(ID):ID,TB=document.querySelector('.dp-c[data-id=\"'+SEL+'\"] .dp-sub');return void(TB&&TB.scrollIntoView({behavior:\"smooth\",block:\"center\"}))}var e=o.closest(\"[data-toggle]\");"]];
  fetch('https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now())
    .then(function(r){return r.text()})
    .then(function(js){
      P.forEach(function(p){ if(js.indexOf(p[0])<0) console.warn('LF staging: patch não aplicado', p[0]); js=js.split(p[0]).join(p[1]); });
      var s=document.createElement('script'); s.text=js; document.body.appendChild(s);
    });
})();
