// Consulta à API de agregados do IBGE (SIDRA, v3) usada para a série histórica municipal do Atlas.
// Rodar em um navegador (console de uma página de servicodados.ibge.gov.br) ou em Node 18+ trocando
// fetch(u) por fetch('https://servicodados.ibge.gov.br'+u). O resultado foi salvo em sidra_serie_historica_rmvrc.json.
const MUN='5103403,5108402,5100102,5102678,5103007,5106109,5107800'; // Cuiabá, Várzea Grande, Acorizal, Campo Verde, Chapada dos Guimarães, N. S. do Livramento, S. A. de Leverger
const Q=[ // [chave, tabela, períodos, variável, classificações[categorias]]
 ['pop',202,'1991|2000|2010',93,'1[0,1]|2[0]'],          // população residente total e urbana
 ['pop22',9923,'2022',93,'1[6795,1]'],
 ['agua91',179,'1991',96,'1[0]|61[0,1033,1035]'],       // DPP: total; rede geral com e sem canalização interna
 ['esg91',180,'1991',96,'1[0]|1612[0,120451,120460,120453,120462]'], // rede geral e fossa séptica ligada à rede pluvial (só do domicílio e comum)
 ['lixo91',182,'1991',96,'1[0]|67[0,2520]'],            // lixo coletado
 ['agua00',1442,'2000',96,'1[0]|11557[0]|61[0,92853]'],
 ['esg00',1444,'2000',96,'1[0]|11557[0]|11558[0,92855]'],
 ['lixo00',1447,'2000',96,'1[0]|11557[0]|67[0,2520]'],
 ['agua10',3218,'2010',96,'61[0,92853]|299[0]|67[0]|309[0]'],
 ['lixo10',3218,'2010',96,'61[0]|299[0]|67[0,2520]|309[0]'],
 ['esg10p',3154,'2010',96,'299[2942,10941]'],           // Resultados Preliminares do Universo: rede geral de esgoto ou pluvial
 ['agua22',6804,'2022',381,'301[72053,31471]|1817[72125]'],
 ['esg22',6805,'2022',381,'11558[46292,46290,72110]'],  // total; rede, pluvial ou fossa ligada à rede; só rede geral ou pluvial
 ['lixo22',6892,'2022',381,'67[10972,2520]'],
 ['alf9100',204,'1991|2000',157,'59[0,1023]|58[0,1141,1142]'], // 5+ total e alfabetizadas; faixas 5–9 e 10–14 (para obter 15+)
 ['alf10',1379,'2010',138,'86[0]|59[93024,1023]|1[0]|287[0,7817,2659,93085]'],
 ['alf22',9542,'2022',950,'59[93024,1023]|2[6794]|86[95251]|287[100362]'],
 ['alf22t',9543,'2022',2513,'2[6794]|86[95251]|287[100362]'] // taxa publicada, usada só para conferir o cálculo
];
(async()=>{ const rows=[];
  for(const [k,t,p,v,c] of Q){
    const u=`/api/v3/agregados/${t}/periodos/${p}/variaveis/${v}?localidades=N6[${MUN}]&classificacao=${encodeURIComponent(c)}`;
    const j=await (await fetch(u)).json();
    for(const va of j) for(const r of va.resultados){ const cats=r.classificacoes.map(x=>x.id+':'+Object.keys(x.categoria)[0]).join('|');
      for(const s of r.series) for(const [per,val] of Object.entries(s.serie)) rows.push([k,cats,s.localidade.id,per,val]); }
  }
  console.log(JSON.stringify({consultado_em:new Date().toISOString(),rows}));
})();
