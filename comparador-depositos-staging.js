/* Staging igual a produção até ao próximo teste: carrega o JS de produção.
   Para testar alterações, aplica-as aqui por cima do JS de produção (ver histórico do ficheiro, 21 set 2026). */
(function(){
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
