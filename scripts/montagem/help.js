<script>
(function(){
  const HELP={
    cls:['Quintis ou intervalos iguais','Define como os valores do indicador são repartidos entre as 5 cores do mapa.<br><b>Quintis</b>: cada cor reúne 20% dos setores. Serve para ver a posição de cada setor em relação aos demais.<br><b>Intervalos iguais</b>: divide a faixa entre o menor e o maior valor em 5 partes do mesmo tamanho. Mostra a distância real entre os valores, mas poucos setores extremos podem deixar quase tudo em uma só cor.'],
    exp:['Exportar o mapa','<b>Mapa em PDF</b>: gera uma folha A4 com o mapa como está na tela, mais legenda completa (tudo o que estiver ligado em Camadas), escala gráfica e numérica, norte, coordenadas dos cantos e fontes. A escala numérica vale para a impressão em tamanho real (100%, sem "ajustar à página"); em outro tamanho, use a escala gráfica.<br><b>PNG</b>: salva a mesma folha como imagem, para textos e apresentações. O mapa exportado sai sempre no tema claro.'],
    area:['Área urbana ou rural','<b>Área urbana</b>: mostra só os setores urbanos do Censo 2022.<br><b>Incluir rural</b>: acrescenta os setores rurais, que são grandes e pouco povoados. As médias, tabelas e o enquadramento do mapa passam a considerar todos.'],
    mun:['Recorte territorial','Escolha os 7 municípios do núcleo da RMVRC, a conurbação Cuiabá–Várzea Grande ou um município. O mapa enquadra o recorte, e os números de destaque, a tabela e as médias passam a valer só para ele.'],
    busca:['Buscar bairro','Digite o nome de um bairro e escolha na lista. O mapa aproxima o bairro e abre a ficha do primeiro setor.'],
    painel:['Indicadores e camadas','<b>Indicadores</b>: escolha o dado que colore os setores no mapa.<br><b>Camadas</b>: troque o fundo do mapa (vegetação, temperatura, cheias, solos, erosão etc.) e ligue ou desligue sobreposições, como rios, bacias, APP, grade UTM e equipamentos públicos.'],
    ppdf:['Gerar PDF','Gera um PDF em A4 desta página. As quebras de página são feitas entre blocos, sem cortar texto, tabelas ou gráficos. Na página <b>Tabelas</b>, gera um relatório com <b>todas as linhas</b> da tabela aberta.'],
    tema:['Tema claro ou escuro','Alterna as cores da página entre fundo claro e fundo escuro, para dar mais conforto conforme a luz do ambiente. A escolha fica guardada neste navegador. Os PDFs são sempre gerados no tema claro.'],
    sdper:['Período','Escolhe o ano mostrado nos números de destaque e na tabela por município: 2023, 2024, 2025 ou a média dos três anos.'],
    sdind:['Indicador da comparação','Escolhe o indicador do gráfico e da tabela de comparação entre 2023, 2024 e 2025. "Todas as internações" serve de referência: mostra se o volume total de atendimentos também mudou.']
  };
  const TIPS={'c-q':'Cada cor reúne 20% dos setores','c-e':'Faixas de valor do mesmo tamanho','ex-pdf':'Mapa em A4 com legenda, escala, norte e fontes','ex-png':'Salvar a imagem do mapa','a-urb':'Mostrar só setores urbanos','a-all':'Incluir também os setores rurais','pt-ind':'Escolher o dado que colore o mapa','pt-cam':'Trocar o fundo e ligar/desligar camadas','zin':'Aproximar','zout':'Afastar','zreset':'Enquadrar o recorte inteiro','munsel':'Escolher o recorte territorial','q':'Digite o nome do bairro'};
  for(const [id,t] of Object.entries(TIPS)){ const el=document.getElementById(id); if(el&&!el.title) el.title=t; }
  const mk=k=>{ const b=document.createElement('button'); b.type='button'; b.className='hlp'; b.dataset.h=k; b.setAttribute('aria-label','O que faz: '+HELP[k][0]); b.title='O que faz?'; b.textContent='?'; return b; };
  const after=(el,k)=>{ if(el&&!(el.nextElementSibling&&el.nextElementSibling.dataset&&el.nextElementSibling.dataset.h===k)) el.insertAdjacentElement('afterend',mk(k)); };
  after(document.querySelector('.seg[aria-label="Classificação"]'),'cls');
  after(document.querySelector('.seg[aria-label="Exportar mapa"]'),'exp');
  after(document.querySelector('.bar .seg[aria-label="Área"]'),'area');
  after(document.getElementById('munsel'),'mun');
  after(document.querySelector('.bar .search'),'busca');
  after(document.querySelector('.ptabs'),'painel');
  document.querySelectorAll('button.ppdf').forEach(b=>after(b,'ppdf'));
  after(document.getElementById('theme-btn'),'tema');
  after(document.getElementById('sd-per'),'sdper');
  after(document.getElementById('sd-ind'),'sdind');
  const pop=document.createElement('div'); pop.className='hlpop'; pop.hidden=true; pop.setAttribute('role','dialog'); document.body.appendChild(pop);
  let cur=null;
  function close(){ pop.hidden=true; if(cur) cur.setAttribute('aria-expanded','false'); cur=null; }
  document.addEventListener('click',e=>{ const b=e.target.closest('button.hlp');
    if(!b){ if(!e.target.closest('.hlpop')) close(); return; }
    e.preventDefault(); if(cur===b){ close(); return; }
    const [t,h]=HELP[b.dataset.h]; pop.innerHTML=`<div class="hlpop-h"><b>${t}</b><button type="button" class="hlpx" aria-label="Fechar">×</button></div><div class="hlpop-b">${h}</div>`;
    pop.hidden=false; cur=b; b.setAttribute('aria-expanded','true');
    const r=b.getBoundingClientRect(), pw=Math.min(340,window.innerWidth-24); pop.style.width=pw+'px';
    let x=Math.min(Math.max(12,r.left+r.width/2-pw/2),window.innerWidth-pw-12), y=r.bottom+8+window.scrollY;
    pop.style.left=(x+window.scrollX)+'px'; pop.style.top=y+'px';
    pop.querySelector('.hlpx').onclick=close; });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') close(); });
  window.addEventListener('scroll',()=>{ if(!pop.hidden) close(); },{passive:true});
})();
</script>
