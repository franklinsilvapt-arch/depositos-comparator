/* Staging do comparador. Enquanto o workflow não gera este ficheiro a partir de
   scripts/comparador-template-staging.js, carrega o JS de produção e aplica por cima
   as diferenças em teste:
   - cartão de filtros sem título, texto explicativo nem nota (a nota passa para o rodapé)
   - no desktop, montante, prazo e banco numa barra sem moldura, com os filtros logo por baixo */
(function(){
  var st=document.createElement('style');
  st.textContent='#lf-dp .dp-card-title,#lf-dp .dp-card-sub,#lf-dp .dp-form-note{display:none}'+
    '@media (min-width:1001px){#lf-dp .dp-card{background:none;border:0;border-radius:0;padding:0}#lf-dp .dp-bar{margin-top:16px}}';
  document.head.appendChild(st);
  new MutationObserver(function(){
    var f=document.querySelector('#lf-dp .dp-foot');
    if(f&&!f.querySelector('.dp-foot-x')){
      var sp=document.createElement('span');sp.className='dp-foot-x';
      sp.textContent=' Sem prazo escolhido, cada depósito mostra a melhor taxa a que aceita o teu montante e o prazo a que se aplica. Comissões de conta não estão descontadas.';
      f.appendChild(sp);
    }
  }).observe(document.body,{childList:true,subtree:true});
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
