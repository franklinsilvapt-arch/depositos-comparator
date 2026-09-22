/* Staging do comparador: carrega o JS de produção e aplica por cima as diferenças em teste.
   Diferenças atuais (22 set 2026):
   - sem os três chips de estatísticas (depósitos comparados, critérios, melhor taxa)
   - subtítulo passa a dizer que se comparam "mais de X" depósitos (arredondado às dezenas, sem número exato)
   - sem o contador "X depósitos" ao lado da ordenação */
(function(){
  function lead(){
    var b=document.querySelector('#lf-dp .dp-stat b');
    var n=b?parseInt(b.textContent,10):51;
    var x=Math.floor((n-1)/10)*10;
    return 'Compara as taxas de mais de '+x+' depósitos a prazo em Portugal e vê quanto recebes em cada um. Taxas verificadas quinzenalmente.';
  }
  new MutationObserver(function(){
    var el=document.querySelector('#lf-dp .dp-lead .text-align-center');
    if(!el)return;
    var t=lead();
    if(el.textContent!==t)el.textContent=t;
  }).observe(document.body,{childList:true,subtree:true});
  var s=document.createElement('script');
  s.src='https://franklinsilvapt-arch.github.io/depositos-comparator/comparador-depositos.js?v='+Date.now();
  document.body.appendChild(s);
})();
