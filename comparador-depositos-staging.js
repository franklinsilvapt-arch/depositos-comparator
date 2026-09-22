/* Staging do comparador: carrega o JS de produção e aplica por cima as diferenças em teste.
   Diferenças atuais:
   - subtítulo mais curto (opção A), para caber em duas linhas no desktop */
(function(){
  var LEAD='Compara os depósitos a prazo com melhor taxa em Portugal e vê quanto recebes em cada um. Taxas verificadas quinzenalmente.';
  new MutationObserver(function(){
    var el=document.querySelector('#lf-dp .dp-lead .text-align-center');
    if(el&&el.textContent!==LEAD)el.textContent=LEAD;
  }).observe(document.body,{childList:true,subtree:true});
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
