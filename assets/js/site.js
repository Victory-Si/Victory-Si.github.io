(() => {
 'use strict';
 document.documentElement.classList.add('js');
 document.querySelectorAll('.pub-filters').forEach(el=>el.hidden=false);
 const toggle = document.querySelector('.menu-toggle');
 const nav = document.querySelector('#primary-navigation');
 if(toggle&&nav){
   const close=()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false')};
   toggle.addEventListener('click',()=>{
     const open=toggle.getAttribute('aria-expanded')!=='true';
     toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);
   });
   nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
   document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
   document.addEventListener('click',e=>{if(!nav.contains(e.target)&&!toggle.contains(e.target))close()});
 }
 const buttons=[...document.querySelectorAll('.pub-filters [data-filter]')];
 const entries=[...document.querySelectorAll('.publication-item[data-kind]')];
 const filter=(kind)=>{
   buttons.forEach(btn=>{const active=btn.dataset.filter===kind;btn.classList.toggle('is-active',active);btn.setAttribute('aria-pressed',String(active))});
   entries.forEach(el=>el.hidden=!(kind==='all'||el.dataset.kind===kind));
 };
 buttons.forEach(btn=>btn.addEventListener('click',()=>filter(btn.dataset.filter)));
 if(buttons.length)filter('first');
 const expand=document.querySelector('.news-expand');
 const news=document.querySelector('.news-list');
 if(expand&&news){
   const hidden=[...news.querySelectorAll('.news-item[data-older="true"]')];
   hidden.forEach(item=>item.hidden=true);
   expand.hidden=!hidden.length;
   expand.addEventListener('click',()=>{
     const opening=expand.getAttribute('aria-expanded')!=='true';
     hidden.forEach(item=>item.hidden=!opening);
     expand.setAttribute('aria-expanded',String(opening));
     expand.textContent=opening?'Show fewer updates ↑':'Show earlier news ↓';
   });
 }
})();
