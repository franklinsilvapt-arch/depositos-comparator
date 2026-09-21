/* Staging igual a produção até ao próximo teste: carrega o JS de produção.
   Para testar alterações, acrescenta aqui as diferenças (ou gera este ficheiro a partir
   de scripts/comparador-template-staging.js quando o workflow o permitir). */
(function(){
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
