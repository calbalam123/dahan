const state={treasury:128400,population:34800000,gdp:2140,approval:72,stability:86,army:185000,relations:62,tax:18,turn:1};
const countries=[
  ["동해 연방","우호","무역 협정과 해상 교류가 활발합니다.",74],
  ["북방공화국","주의","국경 지역에서 긴장이 이어지고 있습니다.",42],
  ["태평양 연합","협력","기술·무역 분야의 협력 가능성이 큽니다.",68],
  ["서해 왕국","중립","문화 교류를 중심으로 관계를 유지합니다.",55]
];
const fmt=n=>new Intl.NumberFormat("ko-KR").format(Math.round(n));
const money=n=>fmt(n)+"억 원";
const $=id=>document.getElementById(id);
function toast(msg){const el=document.createElement("div");el.className="toast";el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2200)}
function metrics(){return `
<div class="grid">
<div class="card"><span>국고</span><strong class="gold">${money(state.treasury)}</strong></div>
<div class="card"><span>인구</span><strong>${fmt(state.population)}명</strong></div>
<div class="card"><span>국내총생산</span><strong>${fmt(state.gdp)}조 원</strong></div>
<div class="card"><span>국민 지지율</span><strong class="good">${state.approval}%</strong></div>
<div class="card"><span>사회 안정도</span><strong>${state.stability}%</strong></div>
<div class="card"><span>군사력</span><strong>${fmt(state.army)}명</strong></div>
<div class="card"><span>외교 관계</span><strong>${state.relations}</strong></div>
<div class="card"><span>세율</span><strong>${state.tax}%</strong></div>
</div>`}
function actionButton(title,desc,fn){return `<button class="action" onclick="${fn}"><b>${title}</b><small>${desc}</small></button>`}
function dashboard(){return `
<div class="hero"><h2>대한제국 국정 운영실</h2><p>경제, 사회, 외교, 국방 정책을 선택하여 가상의 국가를 운영합니다.</p></div>
${metrics()}
<div class="two"><div class="panel"><h3>국가 현황</h3>
<div class="row"><span>국가 체제</span><b>가상 제국 정부</b></div>
<div class="row"><span>수도</span><b>한성</b></div>
<div class="row"><span>국가 안정도</span><b>${state.stability}%</b></div>
<div class="row"><span>현재 세율</span><b>${state.tax}%</b></div>
<div class="row"><span>정책 실행 횟수</span><b>${state.turn-1}회</b></div>
</div><div class="panel"><h3>빠른 정책</h3><div class="actions">
${actionButton("산업 육성","국고 -8,000억 / GDP +2%","applyPolicy('industry')")}
${actionButton("교육 투자","국고 -4,000억 / 지지율 +3","applyPolicy('education')")}
${actionButton("해군 증강","국고 -6,000억 / 군사력 +10,000","applyPolicy('navy')")}
${actionButton("정상 회담","외교력 +7 / 지지율 +1","applyPolicy('summit')")}
</div></div></div>`}
function economy(){return `<div class="hero"><h2>경제·재정</h2><p>국가의 재정과 산업 정책을 관리합니다.</p></div>${metrics()}<div class="two"><div class="panel"><h3>경제 지표</h3><div class="row"><span>GDP 성장률</span><b class="good">+3.2%</b></div><div class="row"><span>물가 상승률</span><b>2.1%</b></div><div class="row"><span>국가 부채</span><b>GDP 대비 38%</b></div><div class="row"><span>조세 수입</span><b>${money(state.treasury*0.11)}</b></div></div><div class="panel"><h3>경제 정책</h3><div class="actions">${actionButton("산업 육성","제조업과 기반시설에 투자","applyPolicy('industry')")}${actionButton("디지털 전환","행정·산업 생산성 향상","applyPolicy('digital')")}${actionButton("세율 인하","세율 -2% / 지지율 +2","applyPolicy('taxdown')")}${actionButton("인프라 확충","국고 -5,000억 / GDP +1%","applyPolicy('infra')")}</div></div></div>`}
function citizens(){return `<div class="hero"><h2>국민·사회</h2><p>교육, 의료, 주거와 국민 생활을 관리합니다.</p></div>${metrics()}<div class="panel"><h3>사회 정책</h3><div class="actions">${actionButton("교육 대개혁","교육 투자 / 지지율 상승","applyPolicy('education')")}${actionButton("의료 확대","국고 -3,500억 / 안정도 +4","applyPolicy('medical')")}${actionButton("주거 공급","국고 -4,500억 / 안정도 +3","applyPolicy('housing')")}${actionButton("국가 축제","국고 -1,000억 / 지지율 +5","applyPolicy('festival')")}</div></div>`}
function diplomacy(){return `<div class="hero"><h2>외교부</h2><p>주변 국가와 조약, 정상 회담, 무역 협력을 진행합니다.</p></div><div class="grid"><div class="card"><span>평균 외교 관계</span><strong>${state.relations}</strong></div><div class="card"><span>무역 규모</span><strong>₩ 82조</strong></div><div class="card"><span>협정 체결</span><strong>12건</strong></div><div class="card"><span>외교 평판</span><strong class="good">안정</strong></div></div><div class="two"><div class="panel"><h3>주변국 관계</h3><table class="table"><thead><tr><th>국가</th><th>상태</th><th>관계도</th></tr></thead><tbody>${countries.map(c=>`<tr><td>${c[0]}</td><td><span class="tag">${c[1]}</span></td><td>${c[3]}</td></tr>`).join("")}</tbody></table></div><div class="panel"><h3>외교 행동</h3><div class="actions">${actionButton("정상 회담","전체 외교 관계 +7","applyPolicy('summit')")}${actionButton("무역 조약","국고 +7,000억 / 외교 +3","applyPolicy('treaty')")}</div></div></div>`}
function military(){return `<div class="hero"><h2>국방부</h2><p>국방 예산과 병력, 해군력을 관리합니다.</p></div>${metrics()}<div class="two"><div class="panel"><h3>전력 현황</h3><div class="row"><span>육군</span><b>${fmt(state.army)}명</b></div><div class="row"><span>해군</span><b>38,000명</b></div><div class="row"><span>공군</span><b>52,000명</b></div><div class="row"><span>국방 예산</span><b>GDP의 2.7%</b></div></div><div class="panel"><h3>국방 정책</h3><div class="actions">${actionButton("군 현대화","국고 -5,000억 / 군사력 +7,000","applyPolicy('training')")}${actionButton("해군 증강","국고 -6,000억 / 군사력 +10,000","applyPolicy('navy')")}${actionButton("재난 구조","국고 -1,500억 / 지지율 +3","applyPolicy('rescue')")}</div></div></div>`}
function laws(){return `<div class="hero"><h2>법률·정책</h2><p>국가 운영 방향을 결정하는 정책을 시행합니다. 모든 수치는 게임 내 가상 수치입니다.</p></div><div class="panel"><h3>현재 시행 정책</h3><div class="row"><span>경제 정책</span><b>산업 성장 우선</b></div><div class="row"><span>복지 정책</span><b>보편적 공공서비스</b></div><div class="row"><span>외교 정책</span><b>교역 및 협력</b></div><div class="row"><span>국방 정책</span><b>방어 역량 강화</b></div></div>`}
function applyPolicy(type){const effects={
industry:[-8000,0,2,0,0,0,2],"education":[-4000,0,0,3,2,0,1],"navy":[-6000,0,0,0,0,10000,1],
summit:[0,0,0,1,1,0,1],digital:[-2500,0,2,2,1,0,1],infra:[-5000,0,1,1,2,0,1],
taxdown:[-3000,0,0,2,0,0,1],medical:[-3500,0,0,1,4,0,1],housing:[-4500,0,0,2,3,0,1],
festival:[-1000,0,0,5,0,0,1],treaty:[7000,0,0,0,0,0,1],training:[-5000,0,0,0,0,7000,1],
rescue:[-1500,0,0,3,2,0,1]}[type]; if(!effects)return;
state.treasury+=effects[0];state.gdp+=effects[2];state.approval+=effects[3];state.stability+=effects[4];state.army+=effects[5];state.relations+=effects[6];state.turn++;
state.approval=Math.min(100,Math.max(0,state.approval));state.stability=Math.min(100,Math.max(0,state.stability));state.relations=Math.min(100,Math.max(0,state.relations));
render();toast("정책이 시행되었습니다.");}
const pages={dashboard:["국가 개요",dashboard],economy:["경제·재정",economy],citizens:["국민·사회",citizens],diplomacy:["외교",diplomacy],military:["국방",military],laws:["법률·정책",laws]};
function render(page=location.hash.slice(1)||"dashboard"){if(!pages[page])page="dashboard";$("pageTitle").textContent=pages[page][0];$("content").innerHTML=pages[page][1]();$("turn").textContent=state.turn+"년차";document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.page===page));location.hash=page;}
document.querySelectorAll(".nav").forEach(b=>b.addEventListener("click",()=>render(b.dataset.page)));
$("date").textContent=new Date().toLocaleDateString("ko-KR",{year:"numeric",month:"long",day:"numeric"});
render();