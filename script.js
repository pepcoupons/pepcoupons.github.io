(function(){
function fb(t){var a=document.createElement("textarea");a.value=t;a.style.cssText="position:fixed;opacity:0";document.body.appendChild(a);a.select();try{document.execCommand("copy")}catch(e){}a.remove()}
function copy(t,b){var s=b.querySelector("span")||b,o=s.textContent;
function ok(){s.textContent="Copied";b.classList.add("done");setTimeout(function(){s.textContent=o;b.classList.remove("done")},1400)}
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,function(){fb(t);ok()})}else{fb(t);ok()}}
document.addEventListener("click",function(e){var b=e.target.closest("[data-code]");if(b&&!b.disabled)copy(b.dataset.code,b)});
var q=document.getElementById("q");
if(q){var c=document.getElementById("fcty"),m=document.getElementById("fmin"),rows=document.querySelectorAll("#tb tr"),none=document.getElementById("none");
function f(){var t=q.value.trim().toLowerCase(),n=0;rows.forEach(function(r){var ok=(!t||r.dataset.n.indexOf(t)>-1)&&(!c.value||r.dataset.c===c.value)&&(+r.dataset.d>=+m.value);r.hidden=!ok;if(ok)n++});none.hidden=n>0}
q.oninput=f;c.onchange=f;m.onchange=f;
var go=document.getElementById("go");if(go)go.onclick=function(){document.getElementById("all").scrollIntoView()}}
var P=window.PC,hc=document.getElementById("hc");
if(P&&P.length&&hc){var fc=document.getElementById("fcard"),dots=document.getElementById("dots"),i=0,paused=false,tm;
function show(k){i=k;var d=P[k];
fc.innerHTML='<div class="slide"><div class="top"><div class="wm">'+d.discount+'%</div>'+(d.logo?'<img class="lg" src="'+d.logo+'" alt="">':'<div class="lg" style="background:'+d.color+'">'+d.name.split(" ").pop()[0]+'</div>')+'<p class="nm">'+d.name+'</p><span class="bdg">'+d.type+'</span></div><div class="bot"><p class="pc">'+d.discount+'%<small>OFF '+d.type.toLowerCase()+'</small></p><p class="ship">Ships from '+d.ship+'</p><button class="cbtn" type="button" data-code="'+d.code+'"><code>'+d.code+'</code><span>Tap to copy</span></button><a class="gl" href="'+d.slug+'/">See details</a></div></div>';
[].forEach.call(dots.children,function(b,j){b.setAttribute("aria-current",j===k?"true":"false")})}
function auto(){clearInterval(tm);if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;tm=setInterval(function(){if(!paused)show((i+1)%P.length)},4500)}
P.forEach(function(d,k){var b=document.createElement("button");b.type="button";b.setAttribute("aria-label","Show "+d.name);b.onclick=function(){show(k);auto()};dots.appendChild(b)});
hc.onmouseenter=function(){paused=true};hc.onmouseleave=function(){paused=false};
hc.addEventListener("focusin",function(){paused=true});hc.addEventListener("focusout",function(){paused=false});
hc.addEventListener("click",function(e){if(e.target.closest("[data-code]")){paused=true;setTimeout(function(){paused=false},2500)}});
show(0);auto()}
})();
