<script setup>
import{RouterLink}from"vue-router"
import hero from "../assets/creme.jpeg"

const images={
hero,
mission:"https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=85",
cosmetiques:"https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=900&q=85",
sante:"https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=900&q=85",
fertilite:"https://images.unsplash.com/photo-1492725764893-90b379c2b6e7?auto=format&fit=crop&w=900&q=85",
dietetique:"https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=900&q=85",
products:"https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=1200&q=85"
}


</script>

<template>
<section class="about-page">

<section class="about-hero">
<div class="about-hero-background"></div>

<div class="container about-hero-container">
<div class="about-hero-content">

<span class="about-eyebrow">
<i class="fa-solid fa-sparkles"></i>
À PROPOS DE CLEVER
</span>

<h1>
Une boutique pensée
<span>pour votre bien-être.</span>
</h1>

<p>
CLEVER est un univers e-commerce dédié à la beauté, à la santé,
à la fertilité et au bien-être. Nous réunissons dans un même
espace une sélection de produits conçue pour vous accompagner
dans votre quotidien.
</p>

<div class="about-hero-actions">
<RouterLink
to="/boutique"
class="about-primary-button"
>
Découvrir la boutique
<i class="fa-solid fa-arrow-right"></i>
</RouterLink>


</div>

<div class="about-hero-signature">
<div class="signature-line"></div>
<span>BEAUTÉ · SANTÉ · FERTILITÉ · DIÉTÉTIQUE</span>
</div>

</div>

<div class="about-hero-visual">

<div class="hero-image-main">
<img
:src="images.hero"
alt="CLEVER - beauté et bien-être"
>
</div>

<div class="hero-floating-card hero-card-top">
<div class="floating-icon">
<i class="fa-solid fa-heart"></i>
</div>

<div>
<strong>Votre bien-être</strong>
<span>Notre priorité</span>
</div>
</div>

<div class="hero-floating-card hero-card-bottom">
<span>NOTRE UNIVERS</span>
<strong>CLEVER</strong>
</div>

</div>
</div>
</section>

<section
id="mission"
class="mission-section"
>
<div class="container">

<div class="mission-layout">

<div class="mission-image">

<img
:src="images.mission"
alt="Bien-être et soins CLEVER"
>

<div class="mission-image-overlay"></div>

<div class="mission-image-caption">
<span>NOTRE VISION</span>

<h3>
Prendre soin de soi
commence par de bons choix.
</h3>
</div>

</div>

<div class="mission-content">

<span class="section-eyebrow">
<i class="fa-solid fa-heart"></i>
NOTRE MISSION
</span>

<h2>
Plus qu'une boutique,
<span>un accompagnement.</span>
</h2>

<p>
Chez CLEVER, nous souhaitons rendre l'achat en ligne plus simple,
plus clair et plus agréable. Nous sélectionnons différents
univers de produits afin de vous permettre de trouver facilement
ce qui correspond à vos besoins.
</p>

<p>
Notre approche repose sur une idée simple : vous proposer une
expérience digitale moderne tout en conservant une relation
humaine et accessible avec nos clients.
</p>

<div class="mission-points">

<div class="mission-point">

<div class="mission-point-icon">
<i class="fa-solid fa-check"></i>
</div>

<div>
<h3>Une sélection réfléchie</h3>

<p>
Des produits choisis pour répondre à différents besoins.
</p>
</div>

</div>

<div class="mission-point">

<div class="mission-point-icon">
<i class="fa-solid fa-heart"></i>
</div>

<div>
<h3>Une expérience centrée sur vous</h3>

<p>
Une navigation simple, intuitive et agréable.
</p>
</div>

</div>

<div class="mission-point">

<div class="mission-point-icon">
<i class="fa-solid fa-headset"></i>
</div>

<div>
<h3>Une relation de proximité</h3>

<p>
Une équipe disponible pour vous accompagner.
</p>
</div>

</div>

</div>

</div>
</div>
</div>
</section>

<section class="values-section">

<div class="container">

<div class="section-heading">

<span class="section-eyebrow">
<i class="fa-solid fa-star"></i>
NOS VALEURS
</span>

<h2>
Ce qui guide
<span>CLEVER.</span>
</h2>

<p>
Notre identité repose sur des valeurs simples qui orientent
notre manière de sélectionner nos produits et de servir nos clients.
</p>

</div>

<div class="values-grid">

<article class="value-card">

<div class="value-card-top">

<span>01</span>

<div class="value-icon">
<i class="fa-solid fa-shield-heart"></i>
</div>

</div>

<h3>Confiance</h3>

<p>
Nous voulons construire une relation durable avec chaque client
grâce à une expérience claire et transparente.
</p>

<div class="value-line"></div>

</article>

<article class="value-card">

<div class="value-card-top">

<span>02</span>

<div class="value-icon">
<i class="fa-solid fa-circle-check"></i>
</div>

</div>

<h3>Qualité</h3>

<p>
Nous accordons une attention particulière aux produits présents
dans nos différents univers.
</p>

<div class="value-line"></div>

</article>

<article class="value-card">

<div class="value-card-top">

<span>03</span>

<div class="value-icon">
<i class="fa-solid fa-heart"></i>
</div>

</div>

<h3>Bien-être</h3>

<p>
Nous plaçons le confort, la beauté et le bien-être au centre de
notre expérience.
</p>

<div class="value-line"></div>

</article>

<article class="value-card">

<div class="value-card-top">

<span>04</span>

<div class="value-icon">
<i class="fa-solid fa-headset"></i>
</div>

</div>

<h3>Proximité</h3>

<p>
Nous souhaitons rester accessibles et proches de nos clients
avant, pendant et après leur achat.
</p>

<div class="value-line"></div>

</article>

</div>
</div>
</section>

<section class="univers-section">

<div class="container">

<div class="univers-heading">

<div>

<span class="section-eyebrow">
<i class="fa-solid fa-layer-group"></i>
NOS UNIVERS
</span>

<h2>
Quatre univers,
<span>une seule expérience.</span>
</h2>

</div>

<p>
CLEVER rassemble plusieurs catégories afin de vous permettre
d'explorer plus facilement les produits correspondant à votre
mode de vie et à vos besoins.
</p>

</div>

<div class="univers-grid">

<RouterLink
to="/cosmetiques"
class="univers-card"
>

<div class="univers-image">

<img
:src="images.cosmetiques"
alt="Cosmétiques CLEVER"
>

<div class="univers-overlay"></div>

</div>

<div class="univers-content">

<span>01</span>

<div class="univers-icon">
<i class="fa-solid fa-spa"></i>
</div>

<h3>Cosmétiques</h3>

<p>
Prendre soin de votre peau et de votre beauté au quotidien.
</p>

<i class="fa-solid fa-arrow-right univers-arrow"></i>

</div>

</RouterLink>

<RouterLink
to="/sante"
class="univers-card"
>

<div class="univers-image">

<img
:src="images.sante"
alt="Santé et bien-être CLEVER"
>

<div class="univers-overlay"></div>

</div>

<div class="univers-content">

<span>02</span>

<div class="univers-icon">
<i class="fa-solid fa-heart-pulse"></i>
</div>

<h3>Santé & Bien-être</h3>

<p>
Des produits pensés pour accompagner votre équilibre quotidien.
</p>

<i class="fa-solid fa-arrow-right univers-arrow"></i>

</div>

</RouterLink>

<RouterLink
to="/fertilite"
class="univers-card"
>

<div class="univers-image">

<img
:src="images.fertilite"
alt="Fertilité et bien-être CLEVER"
>

<div class="univers-overlay"></div>

</div>

<div class="univers-content">

<span>03</span>

<div class="univers-icon">
<i class="fa-solid fa-person-pregnant"></i>
</div>

<h3>Fertilité</h3>

<p>
Un univers dédié au bien-être féminin, masculin et à la fertilité.
</p>

<i class="fa-solid fa-arrow-right univers-arrow"></i>

</div>

</RouterLink>

<RouterLink
to="/dietetique"
class="univers-card"
>

<div class="univers-image">

<img
:src="images.dietetique"
alt="Diététique et alimentation équilibrée"
>

<div class="univers-overlay"></div>

</div>

<div class="univers-content">

<span>04</span>

<div class="univers-icon">
<i class="fa-solid fa-leaf"></i>
</div>

<h3>Diététique</h3>

<p>
Des solutions pensées pour accompagner vos objectifs de bien-être.
</p>

<i class="fa-solid fa-arrow-right univers-arrow"></i>

</div>

</RouterLink>

</div>
</div>
</section>

<section class="experience-section">

<div class="container">

<div class="experience-layout">

<div class="experience-content">

<span class="section-eyebrow">
<i class="fa-solid fa-sparkles"></i>
L'EXPÉRIENCE CLEVER
</span>

<h2>
Tout a été pensé
<span>pour vous.</span>
</h2>

<p>
Nous avons imaginé CLEVER pour que chaque étape de votre parcours
soit simple : découvrir, rechercher, sélectionner et commander.
</p>

<div class="experience-list">

<div class="experience-item">

<div class="experience-number">
01
</div>

<div>
<h3>Trouvez rapidement</h3>

<p>
Parcourez les catégories ou utilisez la recherche pour trouver
vos produits.
</p>
</div>

</div>

<div class="experience-item">

<div class="experience-number">
02
</div>

<div>
<h3>Enregistrez vos favoris</h3>

<p>
Gardez facilement les produits que vous souhaitez retrouver plus tard.
</p>
</div>

</div>

<div class="experience-item">

<div class="experience-number">
03
</div>

<div>
<h3>Commandez simplement</h3>

<p>
Ajoutez vos produits ou vos gammes au panier et finalisez votre commande.
</p>
</div>

</div>

</div>

<RouterLink
to="/boutique"
class="experience-button"
>
Explorer la boutique
<i class="fa-solid fa-arrow-right"></i>
</RouterLink>

</div>

<div class="experience-image">

<img
:src="images.products"
alt="Sélection de produits CLEVER"
>

<div class="experience-image-overlay"></div>

<div class="experience-image-text">

<span>NOTRE ENGAGEMENT</span>

<strong>
Une expérience
simple et élégante.
</strong>

</div>

</div>

</div>
</div>
</section>

<section class="about-cta">

<div class="about-cta-decoration about-decoration-one"></div>

<div class="about-cta-decoration about-decoration-two"></div>

<div class="container">

<div class="about-cta-content">

<span class="section-eyebrow">
<i class="fa-solid fa-sparkles"></i>
BIENVENUE CHEZ CLEVER
</span>

<h2>
Découvrez un univers
<span>pensé pour vous.</span>
</h2>

<p>
Explorez nos produits et trouvez facilement ce qui correspond
à vos besoins en beauté, santé et bien-être.
</p>

<RouterLink
to="/boutique"
class="cta-button"
>
Commencer mes achats
<i class="fa-solid fa-arrow-right"></i>
</RouterLink>

</div>
</div>
</section>

</section>
</template>

<style scoped>
.about-page{
width:100%;
background:#fff;
color:#202520;
}
.about-hero{
position:relative;
min-height:620px;
display:flex;
align-items:center;
overflow:hidden;
background:#f5faf6;
}
.about-hero-background{
position:absolute;
inset:0;
background:
radial-gradient(circle at 78% 20%,rgba(56,176,76,.15),transparent 24%),
radial-gradient(circle at 15% 90%,rgba(56,176,76,.07),transparent 28%);
}
.about-hero-container{
position:relative;
z-index:2;
display:grid;
grid-template-columns:1fr .9fr;
align-items:center;
gap:70px;
padding:85px 0;
}
.about-hero-content{
max-width:680px;
}
.about-eyebrow,
.section-eyebrow{
display:inline-flex;
align-items:center;
gap:8px;
color:#38B04C;
font-size:10px;
font-weight:800;
letter-spacing:2px;
text-transform:uppercase;
}
.about-eyebrow{
margin-bottom:18px;
}
.about-hero h1{
margin:0 0 20px;
font-family:Georgia,"Times New Roman",serif;
font-size:56px;
font-weight:500;
line-height:1.04;
letter-spacing:-1.2px;
}
.about-hero h1 span{
color:#38B04C;
}
.about-hero-content>p{
max-width:650px;
margin:0;
color:#707970;
font-size:14px;
line-height:1.9;
}
.about-hero-actions{
display:flex;
align-items:center;
gap:12px;
margin-top:30px;
}
.about-primary-button,
.about-secondary-button{
height:46px;
display:inline-flex;
align-items:center;
justify-content:center;
gap:9px;
padding:0 19px;
font-size:10px;
font-weight:700;
text-decoration:none;
transition:.25s ease;
}
.about-primary-button{
background:#38B04C;
color:#fff;
}
.about-primary-button:hover{
background:#2f963f;
color:#fff;
transform:translateY(-2px);
}
.about-primary-button i{
transition:.25s ease;
}
.about-primary-button:hover i{
transform:translateX(4px);
}
.about-secondary-button{
border:1px solid #d7e2d8;
background:rgba(255,255,255,.8);
color:#444;
}
.about-secondary-button:hover{
border-color:#38B04C;
color:#38B04C;
}
.about-hero-signature{
display:flex;
align-items:center;
gap:12px;
margin-top:35px;
}
.signature-line{
width:38px;
height:1px;
background:#38B04C;
}
.about-hero-signature span{
color:#8a938b;
font-size:8px;
font-weight:700;
letter-spacing:1.4px;
}
.about-hero-visual{
position:relative;
min-height:470px;
}
.hero-image-main{
position:absolute;
inset:25px 35px 0 40px;
overflow:hidden;
background:#dce9df;
  width: 300px;
  height: 500px;
  object-fit: cover;
}
.hero-image-main img{
width:100%;
height:100%;
display:block;
object-fit:cover;
}
.hero-floating-card{
position:absolute;
display:flex;
align-items:center;
gap:10px;
background:#fff;
box-shadow:0 15px 35px rgba(0,0,0,.10);
}
.hero-card-top{
top:0;
left:0;
padding:12px 15px;
}
.floating-icon{
width:36px;
height:36px;
display:flex;
align-items:center;
justify-content:center;
background:#eef8f0;
color:#38B04C;
}
.floating-icon i{
font-size:12px;
}
.hero-card-top strong{
display:block;
color:#222;
font-size:10px;
}
.hero-card-top span{
display:block;
margin-top:2px;
color:#999;
font-size:8px;
}
.hero-card-bottom{
right:0;
bottom:20px;
padding:13px 18px;
flex-direction:column;
align-items:flex-start;
gap:3px;
}
.hero-card-bottom span{
color:#999;
font-size:7px;
font-weight:800;
letter-spacing:1.6px;
}
.hero-card-bottom strong{
color:#38B04C;
font-family:Georgia,"Times New Roman",serif;
font-size:20px;
font-weight:500;
}
.mission-section{
padding:100px 0;
background:#fff;
}
.mission-layout{
display:grid;
grid-template-columns:1fr 1fr;
gap:75px;
align-items:center;
}
.mission-image{
position:relative;
min-height:490px;
overflow:hidden;
background:#26352a;
}
.mission-image img{
width:100%;
height:100%;
min-height:490px;
display:block;
object-fit:cover;
}
.mission-image-overlay{
position:absolute;
inset:0;
background:linear-gradient(180deg,rgba(15,30,18,.05) 20%,rgba(15,30,18,.78) 100%);
}
.mission-image-caption{
position:absolute;
left:35px;
right:35px;
bottom:32px;
color:#fff;
}
.mission-image-caption span{
display:block;
margin-bottom:9px;
color:#a5dfa9;
font-size:8px;
font-weight:800;
letter-spacing:1.8px;
}
.mission-image-caption h3{
margin:0;
max-width:400px;
font-family:Georgia,"Times New Roman",serif;
font-size:34px;
font-weight:500;
line-height:1.08;
}
.mission-content h2,
.section-heading h2,
.univers-heading h2,
.experience-content h2{
font-family:Georgia,"Times New Roman",serif;
font-weight:500;
line-height:1.1;
}
.mission-content h2{
margin:13px 0 18px;
font-size:42px;
}
.mission-content h2 span,
.section-heading h2 span,
.univers-heading h2 span,
.experience-content h2 span{
color:#38B04C;
}
.mission-content>p{
margin:0 0 14px;
color:#727a73;
font-size:12px;
line-height:1.9;
}
.mission-points{
display:flex;
flex-direction:column;
gap:16px;
margin-top:27px;
}
.mission-point{
display:flex;
align-items:flex-start;
gap:13px;
padding-bottom:16px;
border-bottom:1px solid #e1e8e1;
}
.mission-point:last-child{
border-bottom:0;
padding-bottom:0;
}
.mission-point-icon{
width:38px;
height:38px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:#edf7ef;
color:#38B04C;
}
.mission-point-icon i{
font-size:11px;
}
.mission-point h3{
margin:0 0 4px;
color:#272c27;
font-size:12px;
font-weight:700;
}
.mission-point p{
margin:0;
color:#8a918b;
font-size:10px;
line-height:1.7;
}
.values-section{
padding:95px 0;
background:#f7faf7;
}
.section-heading{
max-width:640px;
margin-bottom:42px;
}
.section-heading h2{
margin:11px 0 13px;
font-size:42px;
}
.section-heading p{
margin:0;
color:#808880;
font-size:12px;
line-height:1.8;
}
.values-grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:15px;
}
.value-card{
position:relative;
min-height:245px;
padding:25px;
background:#fff;
border:1px solid #e1e9e1;
transition:.3s ease;
overflow:hidden;
}
.value-card:hover{
transform:translateY(-5px);
border-color:#38B04C;
box-shadow:0 16px 35px rgba(0,0,0,.06);
}
.value-card-top{
display:flex;
align-items:center;
justify-content:space-between;
margin-bottom:27px;
}
.value-card-top>span{
color:#bbc4bc;
font-size:9px;
font-weight:800;
letter-spacing:1px;
}
.value-icon{
width:49px;
height:49px;
display:flex;
align-items:center;
justify-content:center;
background:#edf7ef;
color:#38B04C;
}
.value-icon i{
font-size:17px;
}
.value-card h3{
margin:0 0 10px;
font-family:Georgia,"Times New Roman",serif;
font-size:19px;
font-weight:500;
}
.value-card p{
margin:0;
color:#858d86;
font-size:10px;
line-height:1.8;
}
.value-line{
position:absolute;
left:25px;
bottom:20px;
width:30px;
height:2px;
background:#38B04C;
transition:.3s ease;
}
.value-card:hover .value-line{
width:55px;
}
.univers-section{
padding:100px 0;
background:#fff;
}
.univers-heading{
display:flex;
align-items:flex-end;
justify-content:space-between;
gap:45px;
margin-bottom:42px;
}
.univers-heading h2{
margin:11px 0 0;
font-size:42px;
}
.univers-heading>p{
max-width:420px;
margin:0;
color:#808880;
font-size:12px;
line-height:1.8;
}
.univers-grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:15px;
}
.univers-card{
position:relative;
min-height:390px;
display:flex;
flex-direction:column;
overflow:hidden;
border:1px solid #e0e7e0;
background:#fff;
text-decoration:none;
transition:.35s ease;
}
.univers-card:hover{
transform:translateY(-6px);
box-shadow:0 16px 35px rgba(0,0,0,.07);
}
.univers-image{
position:absolute;
inset:0;
height:100%;
}
.univers-image img{
width:100%;
height:100%;
display:block;
object-fit:cover;
transition:transform .5s ease;
}
.univers-card:hover .univers-image img{
transform:scale(1.06);
}
.univers-overlay{
position:absolute;
inset:0;
background:linear-gradient(180deg,rgba(17,30,20,.05) 25%,rgba(17,30,20,.84) 100%);
}
.univers-content{
position:relative;
z-index:2;
height:100%;
display:flex;
flex-direction:column;
justify-content:flex-end;
padding:25px;
color:#fff;
}
.univers-content>span{
margin-bottom:10px;
color:rgba(255,255,255,.65);
font-size:8px;
font-weight:800;
letter-spacing:1.5px;
}
.univers-icon{
width:42px;
height:42px;
display:flex;
align-items:center;
justify-content:center;
margin-bottom:15px;
background:#38B04C;
color:#fff;
}
.univers-icon i{
font-size:14px;
}
.univers-content h3{
margin:0 0 8px;
font-family:Georgia,"Times New Roman",serif;
font-size:21px;
font-weight:500;
}
.univers-content p{
max-width:240px;
margin:0;
color:rgba(255,255,255,.78);
font-size:10px;
line-height:1.7;
}
.univers-arrow{
position:absolute;
right:22px;
bottom:22px;
color:#fff;
font-size:12px;
transition:.25s ease;
}
.univers-card:hover .univers-arrow{
transform:translateX(5px);
}
.experience-section{
padding:95px 0;
background:#f7faf7;
}
.experience-layout{
display:grid;
grid-template-columns:1fr .9fr;
gap:70px;
align-items:center;
}
.experience-content h2{
margin:12px 0 16px;
font-size:42px;
}
.experience-content>p{
max-width:580px;
margin:0;
color:#7f877f;
font-size:12px;
line-height:1.9;
}
.experience-list{
display:flex;
flex-direction:column;
gap:18px;
margin-top:33px;
}
.experience-item{
display:flex;
align-items:flex-start;
gap:14px;
padding-bottom:18px;
border-bottom:1px solid #dfe7df;
}
.experience-item:last-child{
border-bottom:0;
padding-bottom:0;
}
.experience-number{
width:38px;
height:38px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:#38B04C;
color:#fff;
font-size:9px;
font-weight:800;
}
.experience-item h3{
margin:0 0 4px;
font-size:13px;
font-weight:700;
}
.experience-item p{
margin:0;
color:#858d86;
font-size:10px;
line-height:1.7;
}
.experience-button{
display:inline-flex;
align-items:center;
gap:9px;
margin-top:30px;
padding:12px 18px;
background:#38B04C;
color:#fff;
font-size:10px;
font-weight:700;
text-decoration:none;
transition:.25s ease;
}
.experience-button:hover{
background:#2f963f;
color:#fff;
transform:translateY(-2px);
}
.experience-button i{
transition:.25s ease;
}
.experience-button:hover i{
transform:translateX(4px);
}
.experience-image{
position:relative;
min-height:450px;
overflow:hidden;
background:#28372b;
}
.experience-image img{
width:100%;
height:100%;
min-height:450px;
display:block;
object-fit:cover;
}
.experience-image-overlay{
position:absolute;
inset:0;
background:linear-gradient(180deg,rgba(18,35,20,.05) 20%,rgba(18,35,20,.72) 100%);
}
.experience-image-text{
position:absolute;
left:30px;
right:30px;
bottom:30px;
color:#fff;
}
.experience-image-text span{
display:block;
margin-bottom:7px;
color:#9edca3;
font-size:8px;
font-weight:800;
letter-spacing:1.7px;
}
.experience-image-text strong{
display:block;
max-width:300px;
font-family:Georgia,"Times New Roman",serif;
font-size:32px;
font-weight:500;
line-height:1.08;
}
.about-cta{
position:relative;
padding:95px 0;
overflow:hidden;
background:#1d2a20;
}
.about-cta-decoration{
position:absolute;
border:1px solid rgba(112,209,123,.14);
border-radius:50%;
}
.about-decoration-one{
width:350px;
height:350px;
top:-180px;
left:-80px;
}
.about-decoration-two{
width:260px;
height:260px;
right:-100px;
bottom:-130px;
}
.about-cta-content{
position:relative;
z-index:2;
max-width:760px;
margin:auto;
text-align:center;
}
.about-cta-content h2{
margin:12px 0 15px;
color:#fff;
font-family:Georgia,"Times New Roman",serif;
font-size:44px;
font-weight:500;
line-height:1.1;
}
.about-cta-content h2 span{
color:#72d07d;
}
.about-cta-content>p{
max-width:620px;
margin:0 auto;
color:rgba(255,255,255,.7);
font-size:12px;
line-height:1.8;
}
.cta-button{
display:inline-flex;
align-items:center;
gap:9px;
margin-top:28px;
padding:13px 20px;
background:#38B04C;
color:#fff;
font-size:10px;
font-weight:700;
text-decoration:none;
transition:.25s ease;
}
.cta-button:hover{
background:#50c761;
color:#fff;
transform:translateY(-2px);
}
@media(max-width:1050px){
.about-hero-container{
grid-template-columns:1fr;
gap:45px;
}
.about-hero-content{
max-width:750px;
}
.about-hero-visual{
max-width:620px;
width:100%;
margin:0 auto;
}
.values-grid,
.univers-grid{
grid-template-columns:repeat(2,1fr);
}
.experience-layout{
grid-template-columns:1fr;
}
.experience-image{
max-width:650px;
width:100%;
margin:auto;
}
}
@media(max-width:800px){
.about-hero{
min-height:auto;
}
.about-hero-container{
padding:65px 0 75px;
}
.about-hero h1{
font-size:45px;
}
.mission-layout{
grid-template-columns:1fr;
gap:45px;
}
.mission-image{
min-height:400px;
}
.mission-image img{
min-height:400px;
}
.univers-heading{
align-items:flex-start;
flex-direction:column;
gap:18px;
}
}
@media(max-width:576px){
.about-hero-container{
padding:50px 0 60px;
}
.about-hero h1{
font-size:34px;
letter-spacing:-.4px;
}
.about-hero-content>p{
font-size:11px;
}
.about-hero-actions{
align-items:stretch;
flex-direction:column;
}
.about-primary-button,
.about-secondary-button{
width:100%;
}
.about-hero-signature{
margin-top:25px;
}
.about-hero-visual{
min-height:340px;
}
.hero-image-main{
inset:20px 20px 0 20px;
}
.hero-card-top{
left:0;
}
.hero-card-bottom{
right:0;
bottom:10px;
}
.mission-section,
.values-section,
.univers-section,
.experience-section{
padding:60px 0;
}
.mission-content h2,
.section-heading h2,
.univers-heading h2,
.experience-content h2{
font-size:31px;
}
.mission-image,
.mission-image img{
min-height:340px;
}
.mission-image-caption{
left:23px;
right:23px;
bottom:23px;
}
.mission-image-caption h3{
font-size:27px;
}
.values-grid,
.univers-grid{
grid-template-columns:1fr;
}
.value-card{
min-height:auto;
}
.univers-card{
min-height:350px;
}
.experience-image,
.experience-image img{
min-height:350px;
}
.experience-image-text strong{
font-size:27px;
}
.about-cta{
padding:65px 0;
}
.about-cta-content h2{
font-size:32px;
}
}
</style>