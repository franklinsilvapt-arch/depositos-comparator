/* Staging do comparador. Enquanto o workflow não gera este ficheiro a partir de
   scripts/comparador-template-staging.js, carrega o JS de produção e aplica por cima
   as diferenças em teste. Diferenças atuais: cartão de filtros sem título nem texto explicativo. */
(function(){
  var st=document.createElement('style');
  st.textContent='#lf-dp .dp-card-title,#lf-dp .dp-card-sub{display:none}';
  document.head.appendChild(st);
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
