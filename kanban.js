 'use strict';
(()=>{
 const buttons=[...document.querySelectorAll('.kanban-person')], cards=[...document.querySelectorAll('.kanban-card')], remaining=[...document.querySelectorAll('.remaining-task')], label=document.getElementById('kanban-selection');
 function clear(){for(const c of cards){c.classList.remove('dim','selected');}for(const b of remaining){b.classList.remove('active');b.setAttribute('aria-pressed','false');}for(const b of buttons){const all=!b.dataset.owner;b.classList.toggle('active',all);b.setAttribute('aria-pressed',String(all));}label.textContent='전체 작업 '+cards.length+'개';}
 function focusTask(id){const card=cards.find(c=>c.dataset.task===id);if(!card)return;clear();for(const c of cards){c.classList.toggle('dim',c!==card);c.classList.toggle('selected',c===card);}for(const b of remaining){const active=b.dataset.taskTarget===id;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}card.open=true;card.scrollIntoView({behavior:'smooth',block:'nearest',inline:'nearest'});card.querySelector('summary').focus({preventScroll:true});label.textContent=id+' 선택';}
 for(const b of buttons)b.addEventListener('click',()=>{clear();const owner=b.dataset.owner;let n=0;for(const c of cards){const match=!owner||c.dataset.owners.split(' · ').includes(owner);c.classList.toggle('dim',!match);c.classList.toggle('selected',Boolean(owner)&&match);if(match)n++;}for(const x of buttons){x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b));}label.textContent=owner?owner+' 관련 작업 '+n+'개':'전체 작업 '+n+'개';});
 for(const b of document.querySelectorAll('[data-task-target]'))b.addEventListener('click',()=>focusTask(b.dataset.taskTarget));
 document.querySelector('.remaining-reset').addEventListener('click',clear);
})();
