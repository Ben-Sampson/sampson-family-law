(()=>{
const $=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>[...c.querySelectorAll(s)];
const hdr=$('.site-header'),toggle=$('.menu-toggle'),menu=$('#primary-menu'),scrim=$('.scrim'),top=$('.to-top');
function setMenu(open){if(!menu)return;menu.classList.toggle('open',open);toggle.setAttribute('aria-expanded',open);toggle.setAttribute('aria-label',open?'Close menu':'Open menu');scrim&&scrim.classList.toggle('show',open);document.body.classList.toggle('menu-open',open);document.body.style.overflow=open?'hidden':'';if(open){const f=$('a,button',menu);f&&f.focus()}}
toggle&&toggle.addEventListener('click',()=>setMenu(!menu.classList.contains('open')));
scrim&&scrim.addEventListener('click',()=>setMenu(false));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(menu&&menu.classList.contains('open')){setMenu(false);toggle.focus()}$$('.has-dd.open').forEach(d=>{d.classList.remove('open');$('button',d).setAttribute('aria-expanded','false')})}});
$$('.has-dd>button').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();const d=b.parentElement,o=!d.classList.contains('open');$$('.has-dd.open').forEach(x=>{if(x!==d){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')}});d.classList.toggle('open',o);b.setAttribute('aria-expanded',o)}));
document.addEventListener('click',e=>{if(!e.target.closest('.has-dd'))$$('.has-dd.open').forEach(d=>{d.classList.remove('open');$('button',d).setAttribute('aria-expanded','false')})});
const onScroll=()=>{const y=scrollY;hdr&&hdr.classList.toggle('scrolled',y>10);top&&top.classList.toggle('show',y>700)};addEventListener('scroll',onScroll,{passive:true});onScroll();
top&&top.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});$$('.reveal').forEach(el=>io.observe(el))}else $$('.reveal').forEach(el=>el.classList.add('in'));
// carousel
$$('.carousel').forEach(c=>{const sl=$$('.slide',c),dots=$('.dots',c);let i=0,t;const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 sl.forEach((s,k)=>{const b=document.createElement('button');b.type='button';b.setAttribute('role','tab');b.setAttribute('aria-label','Show testimonial '+(k+1)+' of '+sl.length);b.addEventListener('click',()=>{go(k);restart()});dots.appendChild(b)});
 function go(n){i=(n+sl.length)%sl.length;sl.forEach((s,k)=>{s.classList.toggle('active',k===i);s.setAttribute('aria-hidden',k!==i)});$$('button',dots).forEach((b,k)=>b.setAttribute('aria-selected',k===i))}
 function restart(){clearInterval(t);if(!reduce)t=setInterval(()=>go(i+1),7000)}
 $('.prev',c).addEventListener('click',()=>{go(i-1);restart()});$('.next',c).addEventListener('click',()=>{go(i+1);restart()});
 c.addEventListener('mouseenter',()=>clearInterval(t));c.addEventListener('mouseleave',restart);c.addEventListener('focusin',()=>clearInterval(t));
 go(0);restart()});
// counters
$$('[data-count]').forEach(el=>{const end=+el.dataset.count;let s=null;const run=ts=>{s=s||ts;const p=Math.min((ts-s)/1400,1);el.textContent=Math.round(end*(1-Math.pow(1-p,3)))+(el.dataset.suffix||'');if(p<1)requestAnimationFrame(run)};
 const io=new IntersectionObserver(es=>{if(es[0].isIntersecting){requestAnimationFrame(run);io.disconnect()}});io.observe(el)});
// demo form: never submits over the network
const f=$('#demo-form');if(f)f.addEventListener('submit',e=>{e.preventDefault();f.reset();const n=$('#demo-notice');n.classList.add('show');n.focus()});
const y=$('#yr');if(y)y.textContent=new Date().getFullYear();
})();
// character galleries: crossfade + Ken Burns (CSS), ~5s/slide, pause on hover/focus/button, reduced motion = no autoplay
(()=>{document.querySelectorAll('.gallery').forEach(g=>{const sl=[...g.querySelectorAll('.g-slide')];if(sl.length<2)return;
 const dots=g.querySelector('.dots'),pb=g.querySelector('.g-pause');let i=0,t,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,hover=false;
 sl.forEach((s,k)=>{const b=document.createElement('button');b.type='button';b.setAttribute('role','tab');b.setAttribute('aria-label','Show photo '+(k+1)+' of '+sl.length);b.addEventListener('click',()=>go(k));dots.appendChild(b)});
 function go(n){i=(n+sl.length)%sl.length;sl.forEach((s,k)=>{s.classList.toggle('active',k===i);s.setAttribute('aria-hidden',k!==i)});[...dots.children].forEach((b,k)=>b.setAttribute('aria-selected',k===i));arm()}
 function arm(){clearTimeout(t);if(!paused&&!hover)t=setTimeout(()=>go(i+1),5000)}
 function setP(v){paused=v;pb.textContent=v?'▶':'❚❚';pb.setAttribute('aria-label',v?'Play slideshow':'Pause slideshow');arm()}
 g.querySelector('.prev').addEventListener('click',()=>go(i-1));g.querySelector('.next').addEventListener('click',()=>go(i+1));pb.addEventListener('click',()=>setP(!paused));
 g.addEventListener('mouseenter',()=>{hover=true;clearTimeout(t)});g.addEventListener('mouseleave',()=>{hover=false;arm()});
 g.addEventListener('focusin',()=>{hover=true;clearTimeout(t)});g.addEventListener('focusout',()=>{hover=false;arm()});
 g.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')go(i-1);if(e.key==='ArrowRight')go(i+1)});
 setP(paused);go(0)})})();
