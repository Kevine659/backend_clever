<script setup>
import { ref } from "vue"
import { RouterLink } from "vue-router"

const form = ref({
    name: "",
    email: "",
    phone: "",
    subject: "",
    message: ""
})

const sending = ref(false)
const success = ref(false)
const error = ref("")

const submitContact = async () => {
    success.value = false
    error.value = ""

    if (
        !form.value.name.trim() ||
        !form.value.email.trim() ||
        !form.value.subject ||
        !form.value.message.trim()
    ) {
        error.value = "Veuillez remplir tous les champs obligatoires."
        return
    }

    sending.value = true

    try {
        await new Promise(resolve => setTimeout(resolve, 1000))

        success.value = true

        form.value = {
            name: "",
            email: "",
            phone: "",
            subject: "",
            message: ""
        }
    } catch (err) {
        console.error("Erreur formulaire contact :", err)
        error.value = "Une erreur est survenue. Veuillez réessayer."
    } finally {
        sending.value = false
    }
}
</script>

<template>
<section class="contact-page">

    <!-- HERO -->
    <section class="contact-hero">
        <div class="contact-hero-glow contact-glow-one"></div>
        <div class="contact-hero-glow contact-glow-two"></div>

        <div class="container contact-hero-container">

            <div class="contact-hero-content">
                <span class="contact-eyebrow">
                    <i class="fa-solid fa-envelope"></i>
                    CONTACTEZ CLEVER
                </span>

                <h1>
                    Parlons de
                    <span>ce qui compte pour vous.</span>
                </h1>

                <p>
                    Une question sur un produit, une commande, une livraison
                    ou besoin d'un conseil ? Notre équipe est à votre écoute
                    pour vous accompagner simplement et efficacement.
                </p>

                <div class="contact-hero-actions">
                    <a
                        href="https://wa.me/237600000000"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="hero-whatsapp-button"
                    >
                        <i class="fa-brands fa-whatsapp"></i>
                        Nous écrire sur WhatsApp
                    </a>

                    <a
                        href="#contact-form"
                        class="hero-message-button"
                    >
                        Envoyer un message
                        <i class="fa-solid fa-arrow-down"></i>
                    </a>
                </div>

                <div class="hero-trust">
                    <div class="hero-trust-item">
                        <i class="fa-solid fa-circle-check"></i>
                        <span>Réponse personnalisée</span>
                    </div>

                    <div class="hero-trust-item">
                        <i class="fa-solid fa-clock"></i>
                        <span>Lun. - Sam. · 08h - 18h</span>
                    </div>
                </div>
            </div>

            <div class="contact-hero-visual">
                <div class="hero-visual-card">

                    <div class="hero-visual-top">
                        <span>UNE ÉQUIPE À VOTRE ÉCOUTE</span>

                        <div class="hero-headset">
                            <i class="fa-solid fa-headset"></i>
                        </div>
                    </div>

                    <h2>
                        Votre satisfaction
                        <span>reste notre priorité.</span>
                    </h2>

                    <p>
                        Nous faisons de notre mieux pour vous offrir une
                        expérience humaine, claire et rassurante à chaque étape.
                    </p>

                    <div class="hero-contact-mini">
                        <div class="mini-contact-icon">
                            <i class="fa-solid fa-location-dot"></i>
                        </div>

                        <div>
                            <span>LOCALISATION</span>
                            <strong>Cameroun</strong>
                        </div>
                    </div>

                    <div class="hero-contact-mini">
                        <div class="mini-contact-icon">
                            <i class="fa-solid fa-envelope"></i>
                        </div>

                        <div>
                            <span>EMAIL</span>
                            <strong>contact@clever.com</strong>
                        </div>
                    </div>

                </div>
            </div>

        </div>
    </section>

    <!-- CONTACT PRINCIPAL -->
    <section class="contact-main">
        <div class="container">
            <div class="contact-main-grid">

                <!-- INFORMATIONS -->
                <aside class="contact-sidebar">

                    <span class="section-eyebrow">
                        <i class="fa-solid fa-address-card"></i>
                        NOS COORDONNÉES
                    </span>

                    <h2>
                        Nous sommes
                        <span>à votre écoute.</span>
                    </h2>

                    <p class="sidebar-intro">
                        Choisissez le moyen de contact qui vous convient
                        le mieux. Notre équipe reste disponible pour vous
                        accompagner.
                    </p>

                    <div class="contact-list">

                        <div class="contact-item">
                            <div class="contact-item-icon">
                                <i class="fa-solid fa-phone"></i>
                            </div>

                            <div class="contact-item-content">
                                <span>TÉLÉPHONE</span>
                                <strong>+237 6XX XX XX XX</strong>
                                <small>Appel & WhatsApp</small>
                            </div>
                        </div>

                        <div class="contact-item">
                            <div class="contact-item-icon">
                                <i class="fa-solid fa-envelope"></i>
                            </div>

                            <div class="contact-item-content">
                                <span>EMAIL</span>
                                <strong>contact@clever.com</strong>
                                <small>Nous vous répondons rapidement</small>
                            </div>
                        </div>

                        <div class="contact-item">
                            <div class="contact-item-icon">
                                <i class="fa-solid fa-location-dot"></i>
                            </div>

                            <div class="contact-item-content">
                                <span>LOCALISATION</span>
                                <strong>Cameroun</strong>
                                <small>Livraison selon votre zone</small>
                            </div>
                        </div>

                        <div class="contact-item">
                            <div class="contact-item-icon">
                                <i class="fa-regular fa-clock"></i>
                            </div>

                            <div class="contact-item-content">
                                <span>HORAIRES</span>
                                <strong>Lundi - Samedi</strong>
                                <small>08:00 - 18:00</small>
                            </div>
                        </div>

                    </div>

                    <div class="sidebar-note">
                        <div class="note-icon">
                            <i class="fa-solid fa-heart"></i>
                        </div>

                        <div>
                            <strong>Une question avant d'acheter ?</strong>
                            <p>
                                Nous pouvons vous aider à mieux comprendre
                                nos produits avant votre commande.
                            </p>
                        </div>
                    </div>

                </aside>

                <!-- FORMULAIRE -->
                <div
                    id="contact-form"
                    class="contact-form-card"
                >

                    <div class="form-card-header">
                        <div>
                            <span class="section-eyebrow">
                                <i class="fa-solid fa-paper-plane"></i>
                                ÉCRIVEZ-NOUS
                            </span>

                            <h2>
                                Envoyez-nous
                                <span>un message.</span>
                            </h2>

                            <p>
                                Remplissez les informations ci-dessous et
                                expliquez-nous votre demande.
                            </p>
                        </div>

                        <div class="form-secure">
                            <i class="fa-solid fa-shield-halved"></i>
                            <span>Informations confidentielles</span>
                        </div>
                    </div>

                    <form
                        class="contact-form"
                        @submit.prevent="submitContact"
                    >

                        <div class="form-grid">

                            <div class="form-group">
                                <label>
                                    Nom complet
                                    <span>*</span>
                                </label>

                                <div class="input-wrapper">
                                    <i class="fa-solid fa-user"></i>

                                    <input
                                        v-model="form.name"
                                        type="text"
                                        placeholder="Votre nom complet"
                                    >
                                </div>
                            </div>

                            <div class="form-group">
                                <label>
                                    Adresse email
                                    <span>*</span>
                                </label>

                                <div class="input-wrapper">
                                    <i class="fa-solid fa-envelope"></i>

                                    <input
                                        v-model="form.email"
                                        type="email"
                                        placeholder="votre@email.com"
                                    >
                                </div>
                            </div>

                        </div>

                        <div class="form-grid">

                            <div class="form-group">
                                <label>
                                    Téléphone
                                </label>

                                <div class="input-wrapper">
                                    <i class="fa-solid fa-phone"></i>

                                    <input
                                        v-model="form.phone"
                                        type="tel"
                                        placeholder="+237 ..."
                                    >
                                </div>
                            </div>

                            <div class="form-group">
                                <label>
                                    Sujet
                                    <span>*</span>
                                </label>

                                <div class="input-wrapper">
                                    <i class="fa-solid fa-tag"></i>

                                    <select
                                        v-model="form.subject"
                                    >
                                        <option value="">
                                            Choisissez un sujet
                                        </option>

                                        <option value="Produit">
                                            Question sur un produit
                                        </option>

                                        <option value="Commande">
                                            Ma commande
                                        </option>

                                        <option value="Livraison">
                                            Livraison
                                        </option>

                                        <option value="Paiement">
                                            Paiement
                                        </option>

                                        <option value="Conseil">
                                            Besoin d'un conseil
                                        </option>

                                        <option value="Autre">
                                            Autre demande
                                        </option>
                                    </select>
                                </div>
                            </div>

                        </div>

                        <div class="form-group">
                            <label>
                                Votre message
                                <span>*</span>
                            </label>

                            <div class="input-wrapper textarea-wrapper">
                                <i class="fa-solid fa-message"></i>

                                <textarea
                                    v-model="form.message"
                                    rows="6"
                                    placeholder="Décrivez votre demande..."
                                ></textarea>
                            </div>
                        </div>

                        <div
                            v-if="error"
                            class="form-feedback feedback-error"
                        >
                            <i class="fa-solid fa-circle-exclamation"></i>
                            <span>{{ error }}</span>
                        </div>

                        <div
                            v-if="success"
                            class="form-feedback feedback-success"
                        >
                            <i class="fa-solid fa-circle-check"></i>
                            <span>
                                Votre message a bien été envoyé.
                                Merci de nous avoir contactés.
                            </span>
                        </div>

                        <div class="form-bottom">
                            <span class="required-note">
                                <span>*</span>
                                Champs obligatoires
                            </span>

                            <button
                                type="submit"
                                class="submit-button"
                                :disabled="sending"
                            >
                                <i
                                    v-if="sending"
                                    class="fa-solid fa-circle-notch fa-spin"
                                ></i>

                                <i
                                    v-else
                                    class="fa-solid fa-paper-plane"
                                ></i>

                                {{
                                    sending
                                        ? "Envoi en cours..."
                                        : "Envoyer mon message"
                                }}
                            </button>
                        </div>

                    </form>

                </div>

            </div>
        </div>
    </section>

    <!-- SERVICES -->
    <section class="contact-services">

        <div class="container">

            <div class="services-heading">

                <div>
                    <span class="section-eyebrow">
                        <i class="fa-solid fa-sparkles"></i>
                        POURQUOI NOUS CONTACTER ?
                    </span>

                    <h2>
                        Un service pensé
                        <span>pour vous.</span>
                    </h2>
                </div>

                <p>
                    Notre objectif est de rendre votre expérience CLEVER
                    aussi simple et rassurante que possible.
                </p>

            </div>

            <div class="services-grid">

                <article class="service-card">

                    <div class="service-card-number">
                        01
                    </div>

                    <div class="service-card-icon">
                        <i class="fa-solid fa-comments"></i>
                    </div>

                    <h3>
                        Conseils personnalisés
                    </h3>

                    <p>
                        Une question avant votre achat ? Notre équipe peut
                        vous orienter selon vos besoins.
                    </p>

                    <div class="service-card-line"></div>

                </article>

                <article class="service-card">

                    <div class="service-card-number">
                        02
                    </div>

                    <div class="service-card-icon">
                        <i class="fa-solid fa-box-open"></i>
                    </div>

                    <h3>
                        Suivi de commande
                    </h3>

                    <p>
                        Nous vous accompagnons pour toute demande concernant
                        vos commandes et leur évolution.
                    </p>

                    <div class="service-card-line"></div>

                </article>

                <article class="service-card">

                    <div class="service-card-number">
                        03
                    </div>

                    <div class="service-card-icon">
                        <i class="fa-solid fa-truck-fast"></i>
                    </div>

                    <h3>
                        Informations livraison
                    </h3>

                    <p>
                        Besoin de connaître les modalités de livraison ?
                        Nous vous renseignons selon votre zone.
                    </p>

                    <div class="service-card-line"></div>

                </article>

            </div>

        </div>

    </section>

    <!-- CTA -->
    <section class="contact-cta">

        <div class="cta-decoration cta-decoration-one"></div>
        <div class="cta-decoration cta-decoration-two"></div>

        <div class="container">

            <div class="contact-cta-content">

                <span class="section-eyebrow light-eyebrow">
                    <i class="fa-solid fa-bag-shopping"></i>
                    BESOIN D'INSPIRATION ?
                </span>

                <h2>
                    Et si vous découvriez
                    <span>nos univers ?</span>
                </h2>

                <p>
                    Explorez notre boutique et trouvez les produits
                    qui correspondent à vos besoins en beauté,
                    santé et bien-être.
                </p>

                <RouterLink
                    to="/boutique"
                    class="cta-button"
                >
                    Découvrir la boutique
                    <i class="fa-solid fa-arrow-right"></i>
                </RouterLink>

            </div>

        </div>

    </section>

</section>
</template>

<style scoped>
.contact-page{
width:100%;
background:#fff;
color:#202520;
overflow:hidden;
}

.contact-hero{
position:relative;
min-height:620px;
display:flex;
align-items:center;
overflow:hidden;
background:
linear-gradient(135deg,#f4faf5 0%,#f8fbf8 55%,#edf7ef 100%);
}

.contact-hero-glow{
position:absolute;
border-radius:50%;
pointer-events:none;
}

.contact-glow-one{
width:420px;
height:420px;
top:-220px;
right:-100px;
background:rgba(56,176,76,.09);
filter:blur(2px);
}

.contact-glow-two{
width:300px;
height:300px;
bottom:-180px;
left:-80px;
background:rgba(56,176,76,.06);
}

.contact-hero-container{
position:relative;
z-index:2;
display:grid;
grid-template-columns:1.08fr .92fr;
align-items:center;
gap:80px;
padding:85px 0;
}

.contact-hero-content{
max-width:680px;
}

.contact-eyebrow,
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

.contact-hero h1{
margin:18px 0 20px;
font-family:Georgia,"Times New Roman",serif;
font-size:57px;
font-weight:500;
line-height:1.03;
letter-spacing:-1.5px;
}

.contact-hero h1 span{
display:block;
color:#38B04C;
}

.contact-hero-content>p{
max-width:630px;
margin:0;
color:#727b73;
font-size:13px;
line-height:1.9;
}

.contact-hero-actions{
display:flex;
align-items:center;
gap:11px;
margin-top:32px;
}

.hero-whatsapp-button,
.hero-message-button{
height:46px;
display:inline-flex;
align-items:center;
justify-content:center;
gap:8px;
padding:0 18px;
font-size:10px;
font-weight:700;
text-decoration:none;
transition:.25s ease;
}

.hero-whatsapp-button{
background:#38B04C;
color:#fff;
}

.hero-whatsapp-button:hover{
background:#2f963f;
color:#fff;
transform:translateY(-2px);
}

.hero-message-button{
border:1px solid #d8e3d9;
background:rgba(255,255,255,.75);
color:#444;
}

.hero-message-button:hover{
border-color:#38B04C;
color:#38B04C;
}

.hero-trust{
display:flex;
align-items:center;
gap:22px;
margin-top:30px;
}

.hero-trust-item{
display:flex;
align-items:center;
gap:7px;
color:#7b857c;
font-size:9px;
}

.hero-trust-item i{
color:#38B04C;
font-size:9px;
}

.contact-hero-visual{
display:flex;
justify-content:center;
}

.hero-visual-card{
position:relative;
width:100%;
max-width:460px;
min-height:410px;
padding:42px;
overflow:hidden;
background:#1d2a20;
box-shadow:0 25px 60px rgba(0,0,0,.13);
}

.hero-visual-card:before{
content:"";
position:absolute;
width:240px;
height:240px;
right:-105px;
top:-105px;
border:1px solid rgba(120,215,130,.15);
border-radius:50%;
}

.hero-visual-card:after{
content:"";
position:absolute;
width:150px;
height:150px;
left:-90px;
bottom:-75px;
border:1px solid rgba(120,215,130,.1);
border-radius:50%;
}

.hero-visual-top{
position:relative;
z-index:2;
display:flex;
align-items:center;
justify-content:space-between;
}

.hero-visual-top>span{
color:#82d18b;
font-size:8px;
font-weight:800;
letter-spacing:1.7px;
}

.hero-headset{
width:52px;
height:52px;
display:flex;
align-items:center;
justify-content:center;
background:#38B04C;
color:#fff;
}

.hero-headset i{
font-size:19px;
}

.hero-visual-card h2{
position:relative;
z-index:2;
max-width:310px;
margin:35px 0 15px;
color:#fff;
font-family:Georgia,"Times New Roman",serif;
font-size:36px;
font-weight:500;
line-height:1.08;
}

.hero-visual-card h2 span{
color:#79d183;
}

.hero-visual-card>p{
position:relative;
z-index:2;
max-width:350px;
margin:0;
color:rgba(255,255,255,.65);
font-size:11px;
line-height:1.8;
}

.hero-contact-mini{
position:relative;
z-index:2;
display:flex;
align-items:center;
gap:11px;
margin-top:23px;
}

.mini-contact-icon{
width:35px;
height:35px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:rgba(56,176,76,.16);
color:#72d17c;
}

.mini-contact-icon i{
font-size:10px;
}

.hero-contact-mini span{
display:block;
margin-bottom:3px;
color:#6d7b70;
font-size:7px;
font-weight:800;
letter-spacing:1.2px;
}

.hero-contact-mini strong{
display:block;
color:#fff;
font-size:10px;
font-weight:600;
}

.contact-main{
padding:105px 0;
background:#fff;
}

.contact-main-grid{
display:grid;
grid-template-columns:.84fr 1.16fr;
gap:75px;
align-items:start;
}

.contact-sidebar{
padding-top:8px;
}

.contact-sidebar h2,
.form-card-header h2,
.services-heading h2,
.contact-cta-content h2{
font-family:Georgia,"Times New Roman",serif;
font-weight:500;
line-height:1.08;
}

.contact-sidebar h2{
margin:12px 0 15px;
font-size:42px;
}

.contact-sidebar h2 span,
.form-card-header h2 span,
.services-heading h2 span,
.contact-cta-content h2 span{
color:#38B04C;
}

.sidebar-intro{
max-width:470px;
margin:0;
color:#7d857e;
font-size:12px;
line-height:1.9;
}

.contact-list{
display:flex;
flex-direction:column;
margin-top:34px;
}

.contact-item{
display:flex;
align-items:flex-start;
gap:13px;
padding:17px 0;
border-bottom:1px solid #e4e9e4;
}

.contact-item:last-child{
border-bottom:0;
}

.contact-item-icon{
width:40px;
height:40px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:#eff8f1;
color:#38B04C;
}

.contact-item-icon i{
font-size:12px;
}

.contact-item-content span{
display:block;
margin-bottom:4px;
color:#9aa19b;
font-size:7px;
font-weight:800;
letter-spacing:1.4px;
}

.contact-item-content strong{
display:block;
color:#2e332f;
font-size:11px;
font-weight:700;
}

.contact-item-content small{
display:block;
margin-top:3px;
color:#999;
font-size:9px;
}

.sidebar-note{
display:flex;
align-items:flex-start;
gap:12px;
margin-top:25px;
padding:17px;
background:#f4f9f5;
}

.note-icon{
width:34px;
height:34px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
background:#38B04C;
color:#fff;
}

.note-icon i{
font-size:11px;
}

.sidebar-note strong{
display:block;
margin-bottom:4px;
color:#333;
font-size:10px;
}

.sidebar-note p{
margin:0;
color:#7f887f;
font-size:9px;
line-height:1.7;
}

.contact-form-card{
padding:37px;
border:1px solid #e2e9e2;
background:#fbfdfb;
box-shadow:0 18px 45px rgba(0,0,0,.035);
}

.form-card-header{
display:flex;
align-items:flex-start;
justify-content:space-between;
gap:20px;
padding-bottom:23px;
border-bottom:1px solid #e3e9e3;
}

.form-card-header h2{
margin:10px 0 10px;
font-size:35px;
}

.form-card-header p{
max-width:550px;
margin:0;
color:#858d86;
font-size:10px;
line-height:1.8;
}

.form-secure{
display:flex;
align-items:center;
gap:7px;
padding:8px 10px;
background:#eef8f0;
color:#5e7563;
font-size:8px;
white-space:nowrap;
}

.form-secure i{
color:#38B04C;
}

.contact-form{
padding-top:25px;
}

.form-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:15px;
}

.form-group{
margin-bottom:16px;
}

.form-group label{
display:block;
margin-bottom:7px;
color:#4f5750;
font-size:9px;
font-weight:700;
}

.form-group label span{
color:#38B04C;
}

.input-wrapper{
position:relative;
}

.input-wrapper>i{
position:absolute;
left:13px;
top:50%;
color:#38B04C;
font-size:10px;
transform:translateY(-50%);
pointer-events:none;
}

.input-wrapper input,
.input-wrapper select,
.input-wrapper textarea{
width:100%;
box-sizing:border-box;
border:1px solid #dae3db;
outline:none;
background:#fff;
color:#333;
font-family:inherit;
font-size:10px;
transition:.2s ease;
}

.input-wrapper input,
.input-wrapper select{
height:43px;
padding:0 12px 0 34px;
}

.input-wrapper textarea{
min-height:145px;
padding:12px 12px 12px 34px;
resize:vertical;
}

.input-wrapper input::placeholder,
.input-wrapper textarea::placeholder{
color:#aaa;
}

.input-wrapper input:focus,
.input-wrapper select:focus,
.input-wrapper textarea:focus{
border-color:#38B04C;
box-shadow:0 0 0 3px rgba(56,176,76,.07);
}

.textarea-wrapper>i{
top:16px;
transform:none;
}

.form-feedback{
display:flex;
align-items:center;
gap:8px;
padding:10px 12px;
margin-bottom:15px;
font-size:9px;
line-height:1.5;
}

.feedback-error{
background:#fff0f0;
color:#d9534f;
}

.feedback-success{
background:#eff9f1;
color:#2f963f;
}

.form-bottom{
display:flex;
align-items:center;
justify-content:space-between;
gap:15px;
margin-top:5px;
}

.required-note{
color:#999;
font-size:8px;
}

.required-note>span{
color:#38B04C;
}

.submit-button{
height:45px;
display:inline-flex;
align-items:center;
justify-content:center;
gap:8px;
padding:0 20px;
border:0;
background:#38B04C;
color:#fff;
font-size:10px;
font-weight:700;
cursor:pointer;
transition:.25s ease;
}

.submit-button:hover:not(:disabled){
background:#2f963f;
transform:translateY(-2px);
box-shadow:0 9px 18px rgba(56,176,76,.18);
}

.submit-button:disabled{
opacity:.6;
cursor:not-allowed;
}

.contact-services{
padding:95px 0;
background:#f7faf7;
}

.services-heading{
display:flex;
align-items:flex-end;
justify-content:space-between;
gap:40px;
margin-bottom:40px;
}

.services-heading h2{
margin:11px 0 0;
font-size:42px;
}

.services-heading>p{
max-width:430px;
margin:0;
color:#818a82;
font-size:11px;
line-height:1.8;
}

.services-grid{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:16px;
}

.service-card{
position:relative;
min-height:230px;
padding:28px;
overflow:hidden;
border:1px solid #e1e9e1;
background:#fff;
transition:.3s ease;
}

.service-card:hover{
transform:translateY(-6px);
border-color:#38B04C;
box-shadow:0 17px 35px rgba(0,0,0,.06);
}

.service-card-number{
position:absolute;
top:23px;
right:24px;
color:#c1c9c2;
font-size:9px;
font-weight:800;
letter-spacing:1px;
}

.service-card-icon{
width:50px;
height:50px;
display:flex;
align-items:center;
justify-content:center;
margin-bottom:22px;
background:#eef8f0;
color:#38B04C;
}

.service-card-icon i{
font-size:17px;
}

.service-card h3{
margin:0 0 9px;
color:#262b26;
font-family:Georgia,"Times New Roman",serif;
font-size:19px;
font-weight:500;
}

.service-card p{
max-width:310px;
margin:0;
color:#858d86;
font-size:10px;
line-height:1.8;
}

.service-card-line{
width:30px;
height:2px;
margin-top:22px;
background:#38B04C;
transition:.3s ease;
}

.service-card:hover .service-card-line{
width:55px;
}

.contact-cta{
position:relative;
padding:100px 0;
overflow:hidden;
background:#1d2a20;
}

.cta-decoration{
position:absolute;
border:1px solid rgba(112,209,123,.13);
border-radius:50%;
}

.cta-decoration-one{
width:380px;
height:380px;
top:-210px;
left:-100px;
}

.cta-decoration-two{
width:280px;
height:280px;
right:-110px;
bottom:-150px;
}

.contact-cta-content{
position:relative;
z-index:2;
max-width:720px;
margin:auto;
text-align:center;
}

.light-eyebrow{
color:#72d07d;
}

.contact-cta-content h2{
margin:13px 0 15px;
color:#fff;
font-size:44px;
}

.contact-cta-content>p{
max-width:580px;
margin:0 auto;
color:rgba(255,255,255,.68);
font-size:11px;
line-height:1.8;
}

.cta-button{
display:inline-flex;
align-items:center;
justify-content:center;
gap:8px;
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

.cta-button i{
transition:.25s ease;
}

.cta-button:hover i{
transform:translateX(4px);
}

@media(max-width:1050px){
.contact-hero-container{
grid-template-columns:1fr;
gap:45px;
}

.contact-hero-content{
max-width:760px;
}

.contact-hero-visual{
justify-content:flex-start;
}

.hero-visual-card{
max-width:650px;
}

.contact-main-grid{
grid-template-columns:1fr;
gap:55px;
}

.contact-sidebar{
max-width:700px;
}

.services-heading{
align-items:flex-start;
flex-direction:column;
gap:18px;
}
}

@media(max-width:800px){
.contact-hero{
min-height:auto;
}

.contact-hero-container{
padding:65px 0 75px;
}

.contact-hero h1{
font-size:46px;
}

.hero-visual-card{
min-height:370px;
}

.services-grid{
grid-template-columns:1fr 1fr;
}
}

@media(max-width:600px){
.contact-hero-container{
padding:50px 0 60px;
}

.contact-hero h1{
font-size:35px;
letter-spacing:-.5px;
}

.contact-hero-content>p{
font-size:11px;
}

.contact-hero-actions{
align-items:stretch;
flex-direction:column;
}

.hero-whatsapp-button,
.hero-message-button{
width:100%;
}

.hero-trust{
align-items:flex-start;
flex-direction:column;
gap:10px;
}

.hero-visual-card{
padding:28px;
min-height:330px;
}

.hero-visual-card h2{
font-size:29px;
}

.contact-main,
.contact-services{
padding:65px 0;
}

.contact-sidebar h2,
.form-card-header h2,
.services-heading h2,
.contact-cta-content h2{
font-size:31px;
}

.contact-form-card{
padding:22px;
}

.form-card-header{
flex-direction:column;
}

.form-secure{
width:max-content;
}

.form-grid{
grid-template-columns:1fr;
gap:0;
}

.form-bottom{
align-items:flex-start;
flex-direction:column;
}

.submit-button{
width:100%;
}

.services-grid{
grid-template-columns:1fr;
}

.service-card{
min-height:auto;
}

.contact-cta{
padding:65px 0;
}

.contact-cta-content h2{
font-size:32px;
}
}
</style>