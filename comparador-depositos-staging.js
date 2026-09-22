/* Staging igual a produção até ao próximo teste: carrega o JS de produção.
   Para testar alterações, aplica-as aqui por cima do JS de produção; o CSS de teste vai em
   comparador-depositos-staging-teste.css, carregado sem cache (ver histórico, 22 set 2026). */
(function(){
  var c=document.createElement('link');c.rel='stylesheet';
  c.href='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos-staging-teste.css?v='+Date.now();
  document.head.appendChild(c);
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
