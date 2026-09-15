<template>
<section class="why-clever-section">
<div class="container">
<div class="why-clever-header">
<span class="why-clever-label">
<i class="fa-solid fa-sparkles"></i>
POURQUOI CLEVER ?
</span>
<h2>
Plus qu'une boutique,
<span>un accompagnement.</span>
</h2>
<p>
Chez CLEVER, nous sélectionnons des produits pensés pour votre
bien-être et nous vous accompagnons pour vous aider à faire les
bons choix.
</p>
</div>

<div class="why-clever-grid">
<article class="why-clever-card">
<div class="why-clever-card-top">
<span class="why-clever-number">01</span>
<div class="why-clever-icon">
<i class="fa-solid fa-shield-heart"></i>
</div>
</div>
<div class="why-clever-content">
<h3>Des produits sélectionnés</h3>
<p>
Nous choisissons avec attention nos produits afin de vous proposer
une sélection adaptée à vos besoins en beauté, santé et bien-être.
</p>
</div>
<div class="why-clever-line"></div>
</article>

<article class="why-clever-card">
<div class="why-clever-card-top">
<span class="why-clever-number">02</span>
<div class="why-clever-icon">
<i class="fa-solid fa-circle-check"></i>
</div>
</div>
<div class="why-clever-content">
<h3>Qualité & confiance</h3>
<p>
Nous privilégions des produits fiables et une expérience d'achat
simple, claire et rassurante à chaque étape.
</p>
</div>
<div class="why-clever-line"></div>
</article>

<article class="why-clever-card">
<div class="why-clever-card-top">
<span class="why-clever-number">03</span>
<div class="why-clever-icon">
<i class="fa-solid fa-truck-fast"></i>
</div>
</div>
<div class="why-clever-content">
<h3>Une livraison simplifiée</h3>
<p>
Commandez facilement depuis chez vous et recevez vos produits dans
les meilleures conditions selon votre zone de livraison.
</p>
</div>
<div class="why-clever-line"></div>
</article>

<article class="why-clever-card">
<div class="why-clever-card-top">
<span class="why-clever-number">04</span>
<div class="why-clever-icon">
<i class="fa-solid fa-headset"></i>
</div>
</div>
<div class="why-clever-content">
<h3>Un service à votre écoute</h3>
<p>
Notre objectif est de vous offrir une expérience humaine et
personnalisée avant, pendant et après votre achat.
</p>
</div>
<div class="why-clever-line"></div>
</article>
</div>

<div class="why-clever-bottom">
<div class="why-clever-image">
<img
src="https://source.unsplash.com/1200x900/?african,woman,beauty,wellness,skincare"
alt="Femme africaine dans un univers beauté et bien-être"
>
<div class="why-clever-image-overlay"></div>
<div class="why-clever-image-decoration"></div>
<div class="why-clever-image-content">
<span>NOTRE ENGAGEMENT</span>
<div class="why-clever-image-divider"></div>
<h3>
Votre bien-être,
<br>
<span>notre priorité.</span>
</h3>
<p>
Une boutique pensée pour vous permettre de découvrir,
choisir et commander plus facilement.
</p>
</div>
</div>

<div class="why-clever-points">
<div class="why-clever-points-header">
<span>CE QUI NOUS DIFFÉRENCIE</span>
<h3>
Une expérience pensée
<span>pour vous.</span>
</h3>
</div>

<div class="why-point">
<div class="why-point-icon">
<i class="fa-solid fa-check"></i>
</div>
<div class="why-point-content">
<h4>Une sélection pensée pour vous</h4>
<p>
Des univers dédiés aux cosmétiques, à la santé, à la fertilité
et à la diététique.
</p>
</div>
</div>

<div class="why-point">
<div class="why-point-icon">
<i class="fa-solid fa-heart"></i>
</div>
<div class="why-point-content">
<h4>Une expérience simple</h4>
<p>
Recherchez, ajoutez aux favoris, composez votre panier et commandez
en quelques étapes.
</p>
</div>
</div>

<div class="why-point">
<div class="why-point-icon">
<i class="fa-solid fa-user-shield"></i>
</div>
<div class="why-point-content">
<h4>Une relation de confiance</h4>
<p>
Vos informations et votre parcours client sont gérés avec sérieux
et transparence.
</p>
</div>
</div>

<RouterLink
to="/boutique"
class="why-clever-button"
>
<span>Découvrir CLEVER</span>
<i class="fa-solid fa-arrow-right"></i>
</RouterLink>
</div>
</div>
</div>
</section>
</template>

<style scoped>
.why-clever-section{
width:100%;
padding:90px 0 100px;
background:
linear-gradient(180deg,#f8faf8 0%,#ffffff 100%);
}
.why-clever-header{
max-width:760px;
margin:0 auto 52px;
text-align:center;
}
.why-clever-label{
display:inline-flex;
align-items:center;
gap:8px;
margin-bottom:15px;
color:#38B04C;
font-size:10px;
font-weight:800;
letter-spacing:2.5px;
text-transform:uppercase;
}
.why-clever-label i{
font-size:10px;
}
.why-clever-header h2{
margin:0 0 16px;
color:#1d231e;
font-family:Georgia,"Times New Roman",serif;
font-size:43px;
font-weight:500;
line-height:1.1;
letter-spacing:-.5px;
}
.why-clever-header h2 span{
color:#38B04C;
}
.why-clever-header p{
max-width:680px;
margin:0 auto;
color:#747b75;
font-size:13px;
line-height:1.9;
}
.why-clever-grid{
display:grid;
grid-template-columns:repeat(4,minmax(0,1fr));
gap:16px;
}
.why-clever-card{
position:relative;
display:flex;
flex-direction:column;
min-height:250px;
padding:26px 24px 23px;
border:1px solid #e5ebe5;
background:#fff;
overflow:hidden;
transition:
transform .35s ease,
box-shadow .35s ease,
border-color .35s ease;
}
.why-clever-card:hover{
transform:translateY(-7px);
border-color:#b9dbbe;
box-shadow:0 18px 45px rgba(28,54,32,.08);
}
.why-clever-card-top{
display:flex;
align-items:flex-start;
justify-content:space-between;
margin-bottom:26px;
}
.why-clever-number{
color:#b8c0b9;
font-size:10px;
font-weight:800;
letter-spacing:1.5px;
}
.why-clever-icon{
width:52px;
height:52px;
display:flex;
align-items:center;
justify-content:center;
background:#edf7ef;
color:#38B04C;
transition:
background .3s ease,
color .3s ease,
transform .3s ease;
}
.why-clever-card:hover .why-clever-icon{
background:#38B04C;
color:#fff;
transform:translateY(-2px);
}
.why-clever-icon i{
font-size:18px;
}
.why-clever-content h3{
margin:0 0 11px;
color:#222722;
font-family:Georgia,"Times New Roman",serif;
font-size:18px;
font-weight:500;
line-height:1.25;
}
.why-clever-content p{
margin:0;
color:#858c86;
font-size:11px;
line-height:1.85;
}
.why-clever-line{
width:35px;
height:2px;
margin-top:auto;
background:#38B04C;
transition:width .3s ease;
}
.why-clever-card:hover .why-clever-line{
width:70px;
}
.why-clever-bottom{
display:grid;
grid-template-columns:1.04fr .96fr;
gap:55px;
align-items:stretch;
margin-top:60px;
}
.why-clever-image{
position:relative;
min-height:430px;
overflow:hidden;
background:#304536;
}
.why-clever-image img{
width:100%;
height:100%;
min-height:430px;
display:block;
object-fit:cover;
object-position:center;
transition:transform .8s ease;
}
.why-clever-image:hover img{
transform:scale(1.035);
}
.why-clever-image-overlay{
position:absolute;
inset:0;
background:
linear-gradient(
90deg,
rgba(15,30,19,.92) 0%,
rgba(15,30,19,.72) 40%,
rgba(15,30,19,.3) 72%,
rgba(15,30,19,.05) 100%
);
}
.why-clever-image-decoration{
position:absolute;
top:24px;
right:24px;
width:85px;
height:85px;
border-top:1px solid rgba(255,255,255,.45);
border-right:1px solid rgba(255,255,255,.45);
}
.why-clever-image-content{
position:absolute;
left:42px;
bottom:42px;
max-width:440px;
color:#fff;
}
.why-clever-image-content>span{
display:block;
margin-bottom:10px;
color:rgba(255,255,255,.72);
font-size:9px;
font-weight:800;
letter-spacing:2.1px;
}
.why-clever-image-divider{
width:42px;
height:2px;
margin-bottom:16px;
background:#38B04C;
}
.why-clever-image-content h3{
margin:0 0 15px;
font-family:Georgia,"Times New Roman",serif;
font-size:38px;
font-weight:500;
line-height:1.08;
}
.why-clever-image-content h3 span{
color:#7bd287;
}
.why-clever-image-content p{
max-width:400px;
margin:0;
color:rgba(255,255,255,.82);
font-size:12px;
line-height:1.8;
}
.why-clever-points{
display:flex;
flex-direction:column;
justify-content:center;
padding:5px 5px 5px 0;
}
.why-clever-points-header{
padding-bottom:22px;
border-bottom:1px solid #dfe7df;
margin-bottom:8px;
}
.why-clever-points-header>span{
display:block;
margin-bottom:8px;
color:#38B04C;
font-size:9px;
font-weight:800;
letter-spacing:1.7px;
}
.why-clever-points-header h3{
margin:0;
color:#222722;
font-family:Georgia,"Times New Roman",serif;
font-size:28px;
font-weight:500;
line-height:1.15;
}
.why-clever-points-header h3 span{
color:#38B04C;
}
.why-point{
display:flex;
align-items:flex-start;
gap:15px;
padding:19px 0;
border-bottom:1px solid #e1e7e1;
}
.why-point:last-of-type{
border-bottom:0;
}
.why-point-icon{
width:36px;
height:36px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:#edf7ef;
color:#38B04C;
}
.why-point-icon i{
font-size:11px;
}
.why-point-content h4{
margin:0 0 6px;
color:#272c28;
font-size:13px;
font-weight:700;
}
.why-point-content p{
margin:0;
color:#858c86;
font-size:10px;
line-height:1.75;
}
.why-clever-button{
display:inline-flex;
align-items:center;
justify-content:space-between;
gap:35px;
width:max-content;
min-width:170px;
margin-top:24px;
padding:13px 17px;
border:1px solid #38B04C;
background:#38B04C;
color:#fff;
font-size:10px;
font-weight:700;
text-decoration:none;
transition:
background .25s ease,
transform .25s ease,
box-shadow .25s ease;
}
.why-clever-button:hover{
background:#2f963f;
color:#fff;
transform:translateY(-3px);
box-shadow:0 10px 25px rgba(56,176,76,.2);
}
.why-clever-button i{
font-size:9px;
transition:transform .25s ease;
}
.why-clever-button:hover i{
transform:translateX(5px);
}
@media(max-width:1100px){
.why-clever-bottom{
gap:35px;
}
.why-clever-header h2{
font-size:39px;
}
}
@media(max-width:991px){
.why-clever-grid{
grid-template-columns:repeat(2,minmax(0,1fr));
}
.why-clever-bottom{
grid-template-columns:1fr;
}
.why-clever-image,
.why-clever-image img{
min-height:390px;
}
.why-clever-points{
padding-right:0;
}
}
@media(max-width:650px){
.why-clever-section{
padding:60px 0 70px;
}
.why-clever-header{
margin-bottom:35px;
}
.why-clever-header h2{
font-size:31px;
}
.why-clever-header p{
font-size:11px;
line-height:1.8;
}
.why-clever-grid{
grid-template-columns:1fr;
gap:12px;
}
.why-clever-card{
min-height:auto;
padding:22px;
}
.why-clever-bottom{
gap:30px;
margin-top:40px;
}
.why-clever-image,
.why-clever-image img{
min-height:390px;
}
.why-clever-image-content{
left:25px;
right:25px;
bottom:28px;
}
.why-clever-image-content h3{
font-size:31px;
}
.why-clever-points-header h3{
font-size:25px;
}
.why-clever-button{
width:100%;
}
}
@media(max-width:420px){
.why-clever-header h2{
font-size:28px;
}
.why-clever-image,
.why-clever-image img{
min-height:350px;
}
.why-clever-image-content h3{
font-size:27px;
}
}
</style>