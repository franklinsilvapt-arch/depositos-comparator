/* Staging igual a produção até ao próximo teste: carrega o JS de produção.
   Para testar alterações, cria scripts/comparador-template-staging.js (cópia do template de
   produção com as alterações) e corre scripts/gerar_js.py, que gera este ficheiro a partir dele.
   O CSS de teste vai em comparador-depositos-staging.css, por cima do @import de produção. */
(function(){
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
