(function(){try{if(/Android/i.test(navigator.userAgent)){var n=document.getElementById('android-note');if(n)n.hidden=false}}catch(e){}})();
document.querySelectorAll('.langpick').forEach(function(d){
var q=d.querySelector('input'),items=[].slice.call(d.querySelectorAll('li'));
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
function filter(){var v=norm(q.value.trim());items.forEach(function(li){li.hidden=v&&norm(li.dataset.k).indexOf(v)<0;});}
d.addEventListener('toggle',function(){if(d.open){q.value='';filter();setTimeout(function(){q.focus();},0);}});
q.addEventListener('input',filter);
q.addEventListener('keydown',function(e){
if(e.key==='Enter'){var a=d.querySelector('li:not([hidden]) a');if(a){e.preventDefault();location.href=a.href;}}
if(e.key==='Escape'){d.open=false;d.querySelector('summary').focus();}
if(e.key==='ArrowDown'){var f=d.querySelector('li:not([hidden]) a');if(f){e.preventDefault();f.focus();}}});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.open=false;d.querySelector('summary').focus();}});
document.addEventListener('click',function(e){if(d.open&&!d.contains(e.target))d.open=false;});
});
