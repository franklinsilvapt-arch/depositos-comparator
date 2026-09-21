/* STAGING (21 set 2026): carrega o JS de produção e aplica por cima a alteração em teste:
   retira o "mais X prazos" debaixo do prazo (os prazos ficam só em "Ver todos os detalhes"). */
(function(){
  var P=[["function(){var q=e.filter(function(P){return g(o,P)}).length-1;return q>0?'<button type=\"button\" class=\"dp-more-prazos\" data-prazos>mais '+q+(q>1?\" prazos\":\" prazo\")+\"</button>\":\"&nbsp;\"}()","\"&nbsp;\""]];
  fetch('https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now())
    .then(function(r){return r.text()})
    .then(function(js){
      P.forEach(function(p){ if(js.indexOf(p[0])<0) console.warn('LF staging: patch não aplicado', p[0]); js=js.split(p[0]).join(p[1]); });
      var s=document.createElement('script'); s.text=js; document.body.appendChild(s);
    });
})();
