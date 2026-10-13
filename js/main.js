document.addEventListener('DOMContentLoaded',()=>{
 const t=document.querySelector('.menu-toggle'),u=document.querySelector('nav ul');
 if(t)t.addEventListener('click',()=>{const o=u.classList.toggle('open');t.setAttribute('aria-expanded',o)});
 document.querySelectorAll('.dropdown>button').forEach(b=>b.addEventListener('click',e=>{const d=b.parentElement;const o=d.classList.toggle('open');b.setAttribute('aria-expanded',o);e.stopPropagation()}));
 document.addEventListener('click',()=>document.querySelectorAll('.dropdown.open').forEach(d=>d.classList.remove('open')));
 const f=document.getElementById('demo-form');
 if(f)f.addEventListener('submit',e=>{e.preventDefault();f.reset();document.getElementById('demo-notice').classList.add('show')});
});
