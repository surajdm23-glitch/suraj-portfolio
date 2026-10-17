/* Portfolio shell behaviour for project pages (work/*.html). Mirrors index.html. */
(()=>{
const CITY="Kodagu, Karnataka",TIMEZONE="Asia/Kolkata",EMAIL="surajdm23@gmail.com";
const root=document.documentElement,$=s=>document.querySelector(s),$$=s=>document.querySelectorAll(s);

/* Some original documents leave a <div> unclosed; lift shell blocks back to <body> so they span the full width. */
$$('body .pf').forEach(el=>{if(el.parentElement!==document.body)document.body.append(el)});

/* Theme: shared with index.html. Pages whose original document is light-only set data-pf-fixed. */
if(!root.dataset.pfFixed)$$('[data-theme-toggle]').forEach(b=>b.onclick=()=>{
  root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('theme',root.dataset.theme)}catch(e){}});

/* Clock */
const clock=$('#pfClock');
const tick=()=>{clock.innerHTML=`${CITY}<b>✳</b>${new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:TIMEZONE})} IST`};
tick();setInterval(tick,15000);

/* Menu + contact drawer */
const menu=$('#pfMenu'),drawer=$('#pfDrawer'),scrim=$('#pfScrim'),menuBtns=$$('[data-pf-menu]'),railL=$('#pfRailL'),railLabel=$('#pfRailLabel');
let last=null;
function open(el){close(false);last=document.activeElement;el.classList.add('open');scrim.classList.add('on');document.body.classList.add('pf-locked');
  if(el===drawer){railL.classList.add('active');railLabel.textContent='Close';railL.setAttribute('aria-label','Close contact')}
  if(el===menu){menuBtns.forEach(b=>b.setAttribute('aria-expanded','true'));menu.querySelectorAll('.pf-mlinks a').forEach((a,i)=>a.style.transitionDelay=(.08+i*.05)+'s')}
  setTimeout(()=>el.querySelector('a,button')?.focus(),60)}
function close(restore=true){[menu,drawer].forEach(x=>x.classList.remove('open'));menu.querySelectorAll('.pf-mlinks a').forEach(a=>a.style.transitionDelay='0s');
  scrim.classList.remove('on');document.body.classList.remove('pf-locked');menuBtns.forEach(b=>b.setAttribute('aria-expanded','false'));
  railL.classList.remove('active');railLabel.textContent='Get in touch';railL.setAttribute('aria-label','Get in touch');if(restore&&last)last.focus()}
menuBtns.forEach(b=>b.onclick=()=>open(menu));
$$('[data-pf-contact]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();if(b===railL&&drawer.classList.contains('open')){close();return}open(drawer)}));
$$('[data-pf-close]').forEach(b=>b.onclick=()=>close());
scrim.onclick=()=>close();
addEventListener('keydown',e=>{if(e.key==='Escape'&&(menu.classList.contains('open')||drawer.classList.contains('open')))close()});

/* Copy email */
$$('[data-pf-copy]').forEach(b=>b.onclick=async()=>{try{await navigator.clipboard.writeText(EMAIL);b.textContent='Copied'}catch(e){b.textContent=EMAIL}setTimeout(()=>b.textContent='Copy email',1800)});

/* Custom cursor */
const cur=$('#pfCursor');
if(cur&&matchMedia('(hover:hover)').matches&&!matchMedia('(prefers-reduced-motion: reduce)').matches){let x=0,y=0,cx=0,cy=0;
  addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;x=e.clientX;y=e.clientY;cur.classList.add('on')});
  document.addEventListener('pointerleave',()=>cur.classList.remove('on'));
  document.addEventListener('pointerover',e=>cur.classList.toggle('big',!!e.target.closest('a,button')));
  (function loop(){cx+=(x-cx)*.2;cy+=(y-cy)*.2;cur.style.left=cx+'px';cur.style.top=cy+'px';requestAnimationFrame(loop)})()}

$('#pfYear').textContent=new Date().getFullYear();
})();
