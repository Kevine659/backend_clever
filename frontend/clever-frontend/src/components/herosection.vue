<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import { RouterLink } from "vue-router"
import heroImage from "../assets/heroimage.png"
import dietImage from "../assets/herodietetique.jpeg"
import fertilityImage from "../assets/fertilite.jpeg"
const currentSlide = ref(0)
const isPaused = ref(false)
const mouseX = ref(0)
const mouseY = ref(0)
let slideInterval = null
const slides = [
    { image: heroImage, smallTitle: "COSMETIQUE", title: "Révélez votre", highlight: "beauté naturelle", description: "Découvrez notre sélection de produits soigneusement choisis pour prendre soin de votre beauté, votre bien-être et votre santé au quotidien.", feature1: "Produits sélectionnés", feature1Text: "Qualité & efficacité", feature2: "Qualité contrôlée", feature2Text: "Pour votre bien-être", feature3: "Votre satisfaction", feature3Text: "Notre priorité" },
    { image: dietImage, smallTitle: "DIÉTÉTIQUE & BIEN-ÊTRE", title: "Prenez soin de votre", highlight: "silhouette naturellement", description: "Découvrez notre sélection de thés minceur et ventre plat soigneusement choisis pour accompagner votre bien-être et prendre soin de votre silhouette au quotidien.", feature1: "Thés sélectionnés", feature1Text: "Qualité & naturel", feature2: "Bien-être quotidien", feature2Text: "Pour votre équilibre", feature3: "Votre satisfaction", feature3Text: "Notre priorité" },
    { image: fertilityImage, smallTitle: "SANTÉ FERTILE", title: "Prenez soin de votre", highlight: "projet de fertilité", description: "Découvrez notre sélection de produits dédiés au bien-être et à la santé fertile, soigneusement choisis pour vous accompagner dans votre parcours.", feature1: "Produits sélectionnés", feature1Text: "Qualité & efficacité", feature2: "Qualité contrôlée", feature2Text: "Pour votre santé", feature3: "Votre satisfaction", feature3Text: "Notre priorité" }
]
const current = computed(() => slides[currentSlide.value])
const titleWords = computed(() => `${current.value.title} ${current.value.highlight}`.split(" "))
const nextSlide = () => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
}
const goToSlide = (index) => {
    currentSlide.value = index
    restartSlider()
}
const restartSlider = () => {
    if (slideInterval) clearInterval(slideInterval)
    if (!isPaused.value) slideInterval = setInterval(nextSlide, 6500)
}
const pauseSlider = () => {
    isPaused.value = true
    if (slideInterval) clearInterval(slideInterval)
}
const resumeSlider = () => {
    isPaused.value = false
    restartSlider()
}
const handleMouseMove = (event) => {
    const rect = event.currentTarget.getBoundingClientRect()
    const x = (event.clientX - rect.left) / rect.width - .5
    const y = (event.clientY - rect.top) / rect.height - .5
    mouseX.value = -(x * 10)
    mouseY.value = -(y * 10)
}
const resetParallax = () => {
    mouseX.value = 0
    mouseY.value = 0
}
onMounted(() => {
    restartSlider()
})
onBeforeUnmount(() => {
    if (slideInterval) clearInterval(slideInterval)
})
</script>
<template>
    <section class="hero-section" @mouseenter="pauseSlider" @mouseleave="resumeSlider" @mousemove="handleMouseMove"
        @mouseleave.capture="resetParallax">
        <div class="hero-organic organic-one"></div>
        <div class="hero-organic organic-two"></div>
        <div class="hero-organic organic-three"></div>
        <div class="hero-glow"></div>
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <Transition name="hero-content" mode="out-in">
                        <div :key="currentSlide" class="hero-text-content">
                            <div class="hero-small-title">
                                <span class="small-line"></span>
                                <i class="fa-solid fa-leaf"></i>
                                <span>{{ current.smallTitle }}</span>
                            </div>
                            <h1 class="hero-title">
                                <span v-for="(word, index) in titleWords" :key="`${currentSlide}-${index}`"
                                    class="title-word" :style="{ animationDelay: `${0.45 + index * 0.09}s` }">{{ word
                                    }}&nbsp;</span>
                            </h1>
                            <p class="hero-description">{{ current.description }}</p>
                            <div class="hero-buttons">
                                <RouterLink to="/boutique" class="hero-btn">
                                    <span class="button-liquid"></span>
                                    <span class="button-content">Découvrir la boutique <i
                                            class="fa-solid fa-arrow-right"></i></span>
                                </RouterLink>
                                
                            </div>
                            <div class="hero-features">
                                <div class="hero-feature">
                                    <div class="feature-icon"><i class="fa-solid fa-leaf"></i></div>
                                    <div><strong>{{ current.feature1 }}</strong><span>{{ current.feature1Text }}</span>
                                    </div>
                                </div>
                                <div class="hero-feature">
                                    <div class="feature-icon"><i class="fa-solid fa-shield-heart"></i></div>
                                    <div><strong>{{ current.feature2 }}</strong><span>{{ current.feature2Text }}</span>
                                    </div>
                                </div>
                                <div class="hero-feature">
                                    <div class="feature-icon"><i class="fa-solid fa-heart"></i></div>
                                    <div><strong>{{ current.feature3 }}</strong><span>{{ current.feature3Text }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Transition>
                </div>
                <div class="hero-image-wrapper">
                    <Transition name="hero-image" mode="out-in">
                        <div :key="currentSlide" class="hero-image-stage">
                            <div class="image-orbit orbit-one"></div>
                            <div class="image-orbit orbit-two"></div>
                            <div class="image-soft-shadow"></div>
                            <img :src="current.image" :alt="current.smallTitle" class="hero-image"
                                :style="{ transform: `translate3d(${mouseX}px,${mouseY}px,0) scale(1.02)` }">
                            <div class="floating-badge badge-one">
                                <div class="badge-icon"><i class="fa-solid fa-leaf"></i></div>
                                <div><strong>{{ current.feature1 }}</strong><span>{{ current.feature1Text }}</span>
                                </div>
                            </div>
                            <div class="floating-badge badge-two">
                                <div class="badge-icon"><i class="fa-solid fa-shield-heart"></i></div>
                                <div><strong>{{ current.feature2 }}</strong><span>{{ current.feature2Text }}</span>
                                </div>
                            </div>
                        </div>
                    </Transition>
                </div>
            </div>
            <div class="hero-bottom">
                <div class="hero-indicators">
                    <button v-for="(slide, index) in slides" :key="index" type="button" class="hero-indicator"
                        :class="{ active: currentSlide === index }" @click="goToSlide(index)">
                        <span class="indicator-number">0{{ index + 1 }}</span>
                        <span class="indicator-track"><span></span></span>
                    </button>
                </div>
                <div class="hero-next-label">
                    <span>EXPLORER</span>
                    <i class="fa-solid fa-arrow-down"></i>
                </div>
            </div>
        </div>
    </section>
</template>
<style scoped>
*,
*::before,
*::after {
    box-sizing: border-box
}

.hero-section {
    width: 100%;
    background: linear-gradient(135deg, #f7fff8 0%, #fff 48%, #effbf1 100%);
    overflow: hidden;
    position: relative;
    isolation: isolate;
    animation: heroBackground 1s ease-out both
}

.hero-section::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 75% 45%, rgba(56, 181, 74, .08), transparent 35%);
    pointer-events: none;
    z-index: -1
}

.hero-section::after {
    content: "";
    position: absolute;
    width: 500px;
    height: 500px;
    right: -260px;
    bottom: -300px;
    border-radius: 50%;
    border: 1px solid rgba(56, 181, 74, .09);
    pointer-events: none;
    z-index: -1
}

.hero-glow {
    position: absolute;
    width: 420px;
    height: 420px;
    border-radius: 50%;
    right: 15%;
    top: 50%;
    transform: translateY(-50%);
    background: radial-gradient(circle, rgba(56, 181, 74, .10) 0%, rgba(56, 181, 74, .04) 45%, transparent 72%);
    filter: blur(4px);
    animation: glowFloat 7s ease-in-out infinite;
    pointer-events: none;
    z-index: -1
}

.hero-organic {
    position: absolute;
    border-radius: 50%;
    background: rgba(56, 181, 74, .055);
    border: 1px solid rgba(56, 181, 74, .08);
    pointer-events: none;
    z-index: -1
}

.organic-one {
    width: 170px;
    height: 260px;
    left: -70px;
    top: 12%;
    transform: rotate(35deg);
    animation: organicFloatOne 10s ease-in-out infinite
}

.organic-two {
    width: 110px;
    height: 180px;
    right: 8%;
    top: 5%;
    transform: rotate(-35deg);
    animation: organicFloatTwo 12s ease-in-out infinite
}

.organic-three {
    width: 190px;
    height: 120px;
    right: 25%;
    bottom: -75px;
    transform: rotate(25deg);
    animation: organicFloatThree 11s ease-in-out infinite
}

.container {
    position: relative;
    z-index: 2
}

.hero-content {
    min-height: 440px;
    display: flex;
    align-items: stretch;
    position: relative
}

.hero-text {
    width: 48%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 45px 20px 45px 35px;
    position: relative;
    z-index: 5
}

.hero-text-content {
    width: 100%
}

.hero-small-title {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1.2px;
    color: #38b54a;
    margin-bottom: 15px;
    text-transform: uppercase;
    opacity: 0;
    animation: fadeUp .7s .25s cubic-bezier(.22, 1, .36, 1) forwards
}

.small-line {
    width: 22px;
    height: 1px;
    background: #38b54a;
    display: block
}

.hero-small-title i {
    font-size: 12px
}

.hero-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 48px;
    line-height: 1.05;
    font-weight: 500;
    color: #202020;
    margin: 0 0 19px;
    max-width: 540px;
    overflow: visible
}

.title-word {
    display: inline-block;
    opacity: 0;
    transform: translateY(32px);
    animation: titleWord .65s cubic-bezier(.22, 1, .36, 1) forwards
}

.title-word:nth-last-child(-n+2) {
    color: #38b54a
}

.hero-description {
    max-width: 410px;
    font-size: 12px;
    line-height: 1.7;
    color: #666;
    margin: 0 0 25px;
    opacity: 0;
    transform: translateY(18px);
    animation: fadeUp .7s 1.05s cubic-bezier(.22, 1, .36, 1) forwards
}

.hero-buttons {
    display: flex;
    align-items: center;
    gap: 17px;
    margin-bottom: 34px;
    opacity: 0;
    transform: translateY(18px);
    animation: fadeUp .7s 1.25s cubic-bezier(.22, 1, .36, 1) forwards
}

.hero-btn {
    position: relative;
    display: inline-flex;
    align-items: center;
    overflow: hidden;
    padding: 11px 18px;
    border: 1px solid #38b54a;
    border-radius: 6px;
    background: #38b54a;
    color: #fff;
    font-size: 11px;
    font-weight: 500;
    text-decoration: none;
    box-shadow: 0 7px 18px rgba(56, 181, 74, .18);
    isolation: isolate;
    animation: buttonPulse 1s 2s ease-out 1
}

.button-liquid {
    position: absolute;
    left: -110%;
    top: 0;
    width: 100%;
    height: 100%;
    background: #2f9d40;
    transform: skewX(-18deg);
    transition: left .5s cubic-bezier(.22, 1, .36, 1);
    z-index: -1
}

.hero-btn:hover .button-liquid {
    left: -5%
}

.button-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 12px
}

.button-content i {
    font-size: 10px;
    transition: transform .3s ease
}

.hero-btn:hover {
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(56, 181, 74, .25)
}

.hero-btn:hover .button-content i {
    transform: translateX(4px)
}

.video-btn {
    display: flex;
    align-items: center;
    gap: 9px;
    border: 0;
    background: transparent;
    color: #333;
    font-size: 10px;
    cursor: pointer;
    padding: 0
}

.play-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 12px rgba(0, 0, 0, .08);
    border: 1px solid #edf2ed;
    transition: all .25s ease
}

.play-icon i {
    font-size: 10px;
    color: #38b54a;
    margin-left: 1px
}

.video-btn:hover .play-icon {
    background: #38b54a;
    border-color: #38b54a;
    transform: scale(1.08)
}

.video-btn:hover .play-icon i {
    color: #fff
}

.hero-features {
    display: flex;
    align-items: center;
    gap: 22px;
    opacity: 0;
    transform: translateY(18px);
    animation: fadeUp .7s 1.45s cubic-bezier(.22, 1, .36, 1) forwards
}

.hero-feature {
    display: flex;
    align-items: center;
    gap: 7px
}

.feature-icon {
    width: 29px;
    height: 29px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(56, 181, 74, .35);
    border-radius: 50%;
    color: #38b54a;
    font-size: 11px;
    background: rgba(56, 181, 74, .05);
    flex-shrink: 0;
    animation: badgeRotate 12s linear infinite
}

.hero-feature div:last-child {
    display: flex;
    flex-direction: column
}

.hero-feature strong {
    font-size: 12px;
    font-weight: 500;
    color: #444;
    white-space: nowrap
}

.hero-feature span {
    font-size: 10px;
    color: #999;
    margin-top: 2px;
    white-space: nowrap
}

.hero-image-wrapper {
    width: 200em;
    min-height: 450px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden
}

.hero-image-stage {
    width: 100%;
    height: 100%;
    min-height: 450px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center
}

.hero-image {
    width: 200em;
    height: 100%;
    max-height: 450px;
    margin-left: -15em;
    display: block;
    object-fit: contain;
    position: relative;
    z-index: 4;
    filter: blur(8px);
    opacity: 0;
    transform: translate3d(0, 0, 0) scale(.98);
    transition: transform .25s ease-out;
    animation: productReveal 1.2s .05s cubic-bezier(.22, 1, .36, 1) forwards, imageFloat 7s 1.3s ease-in-out infinite
}

.image-soft-shadow {
    position: absolute;
    width: 48%;
    height: 55px;
    bottom: 35px;
    left: 30%;
    border-radius: 50%;
    background: rgba(0, 0, 0, .10);
    filter: blur(25px);
    z-index: 1;
    opacity: 0;
    animation: shadowReveal 1.2s .3s ease forwards, shadowFloat 7s 1.5s ease-in-out infinite
}

.image-orbit {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(56, 181, 74, .12);
    z-index: 0;
    pointer-events: none
}

.orbit-one {
    width: 330px;
    height: 330px;
    animation: orbitRotate 20s linear infinite
}

.orbit-two {
    width: 420px;
    height: 420px;
    border-style: dashed;
    opacity: .5;
    animation: orbitRotateReverse 28s linear infinite
}

.floating-badge {
    position: absolute;
    z-index: 7;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 11px;
    background: rgba(255, 255, 255, .82);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, .95);
    border-radius: 8px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, .08);
    opacity: 0;
    animation: badgeReveal .7s 1.35s cubic-bezier(.22, 1, .36, 1) forwards, badgeFloat 6s 2.1s ease-in-out infinite
}

.badge-one {
    top: 70px;
    right: 15px
}

.badge-two {
    bottom: 55px;
    left: 15px;
    animation-delay: 1.55s, 3s
}

.badge-icon {
    width: 27px;
    height: 27px;
    border-radius: 50%;
    background: rgba(56, 181, 74, .08);
    color: #38b54a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px
}

.floating-badge strong {
    display: block;
    color: #333;
    font-size: 9px;
    font-weight: 600
}

.floating-badge span {
    display: block;
    color: #999;
    font-size: 8px;
    margin-top: 1px
}

.hero-bottom {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 45px;
    padding-bottom: 9px
}

.hero-indicators {
    display: flex;
    align-items: center;
    gap: 8px
}

.hero-indicator {
    width: 55px;
    height: 22px;
    padding: 0;
    border: 0;
    background: transparent;
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer
}

.indicator-number {
    font-size: 8px;
    color: #aaa;
    font-weight: 600
}

.hero-indicator.active .indicator-number {
    color: #38b54a
}

.indicator-track {
    height: 3px;
    width: 25px;
    background: rgba(56, 181, 74, .16);
    border-radius: 10px;
    overflow: hidden;
    display: block
}

.hero-indicator.active .indicator-track {
    width: 38px
}

.indicator-track span {
    display: block;
    width: 0;
    height: 100%;
    background: #38b54a;
    border-radius: 10px
}

.hero-indicator.active .indicator-track span {
    width: 100%;
    transition: width 6.5s linear
}

.hero-next-label {
    position: absolute;
    right: 4px;
    bottom: 12px;
    display: flex;
    align-items: center;
    gap: 7px;
    color: #aaa;
    font-size: 7px;
    letter-spacing: 1.5px
}

.hero-next-label i {
    font-size: 9px;
    animation: scrollDown 1.8s ease-in-out infinite
}

.hero-content-enter-active,
.hero-content-leave-active {
    transition: opacity .5s ease, transform .5s ease
}

.hero-content-enter-from {
    opacity: 0;
    transform: translateY(10px)
}

.hero-content-leave-to {
    opacity: 0;
    transform: translateY(-10px)
}

.hero-image-enter-active,
.hero-image-leave-active {
    transition: opacity .65s ease, transform .65s ease
}

.hero-image-enter-from {
    opacity: 0;
    transform: translateX(35px)
}

.hero-image-leave-to {
    opacity: 0;
    transform: translateX(-35px)
}

@keyframes heroBackground {
    from {
        opacity: 0
    }

    to {
        opacity: 1
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(22px)
    }

    to {
        opacity: 1;
        transform: translateY(0)
    }
}

@keyframes titleWord {
    from {
        opacity: 0;
        transform: translateY(32px)
    }

    to {
        opacity: 1;
        transform: translateY(0)
    }
}

@keyframes productReveal {
    0% {
        opacity: 0;
        filter: blur(10px);
        transform: translate3d(0, 0, 0) scale(.98)
    }

    60% {
        opacity: 1;
        filter: blur(2px);
        transform: translate3d(0, 0, 0) scale(1.01)
    }

    100% {
        opacity: 1;
        filter: blur(0);
        transform: translate3d(0, 0, 0) scale(1.02)
    }
}

@keyframes imageFloat {

    0%,
    100% {
        margin-top: 0
    }

    50% {
        margin-top: -7px
    }
}

@keyframes shadowReveal {
    from {
        opacity: 0;
        transform: scale(.7)
    }

    to {
        opacity: .5;
        transform: scale(1)
    }
}

@keyframes shadowFloat {

    0%,
    100% {
        transform: scale(1)
    }

    50% {
        transform: scale(.92)
    }
}

@keyframes badgeReveal {
    from {
        opacity: 0;
        transform: translateY(12px) rotate(-5deg)
    }

    to {
        opacity: 1;
        transform: translateY(0) rotate(0)
    }
}

@keyframes badgeFloat {

    0%,
    100% {
        margin-top: 0
    }

    50% {
        margin-top: -6px
    }
}

@keyframes badgeRotate {
    from {
        transform: rotate(0)
    }

    to {
        transform: rotate(360deg)
    }
}

@keyframes buttonPulse {
    0% {
        box-shadow: 0 7px 18px rgba(56, 181, 74, .18)
    }

    45% {
        box-shadow: 0 7px 18px rgba(56, 181, 74, .18), 0 0 0 7px rgba(56, 181, 74, .08)
    }

    100% {
        box-shadow: 0 7px 18px rgba(56, 181, 74, .18), 0 0 0 0 rgba(56, 181, 74, 0)
    }
}

@keyframes glowFloat {

    0%,
    100% {
        transform: translateY(-50%) scale(1);
        opacity: .8
    }

    50% {
        transform: translateY(-52%) scale(1.06);
        opacity: 1
    }
}

@keyframes organicFloatOne {

    0%,
    100% {
        margin-top: 0;
        transform: rotate(35deg)
    }

    50% {
        margin-top: -18px;
        transform: rotate(39deg)
    }
}

@keyframes organicFloatTwo {

    0%,
    100% {
        margin-top: 0;
        transform: rotate(-35deg)
    }

    50% {
        margin-top: 15px;
        transform: rotate(-31deg)
    }
}

@keyframes organicFloatThree {

    0%,
    100% {
        margin-top: 0;
        transform: rotate(25deg)
    }

    50% {
        margin-top: -12px;
        transform: rotate(29deg)
    }
}

@keyframes orbitRotate {
    from {
        transform: rotate(0)
    }

    to {
        transform: rotate(360deg)
    }
}

@keyframes orbitRotateReverse {
    from {
        transform: rotate(360deg)
    }

    to {
        transform: rotate(0)
    }
}

@keyframes scrollDown {

    0%,
    100% {
        transform: translateY(0)
    }

    50% {
        transform: translateY(5px)
    }
}

@media(max-width:991px) {
    .hero-content {
        min-height: 400px
    }

    .hero-text {
        padding-left: 25px
    }

    .hero-title {
        font-size: 42px
    }

    .hero-features {
        gap: 12px
    }

    .hero-feature strong {
        font-size: 8px
    }

    .hero-feature span {
        font-size: 7px
    }

    .hero-image-wrapper {
        min-height: 400px
    }

    .hero-image-stage {
        min-height: 400px
    }

    .hero-image {
        max-height: 400px
    }

    .orbit-one {
        width: 300px;
        height: 300px
    }

    .orbit-two {
        width: 370px;
        height: 370px
    }

    .badge-one {
        right: 0
    }

    .badge-two {
        left: 0
    }
}

@media(max-width:768px) {
    .hero-content {
        min-height: auto;
        display: flex;
        flex-direction: column
    }

    .hero-text {
        width: 100%;
        padding: 40px 25px 20px
    }

    .hero-title {
        font-size: 38px
    }

    .hero-description {
        max-width: 500px
    }

    .hero-image-wrapper {
        width: 100%;
        height: auto;
        min-height: 300px;
        padding: 0 20px 20px
    }

    .hero-image-stage {
        min-height: 300px
    }

    .hero-image {
        width: 100%;
        height: auto;
        max-height: none;
        object-fit: contain;
        margin-left: 0
    }

    .hero-features {
        flex-wrap: wrap;
        gap: 15px
    }

    .hero-image-stage .orbit-one {
        width: 250px;
        height: 250px
    }

    .hero-image-stage .orbit-two {
        width: 310px;
        height: 310px
    }

    .hero-bottom {
        padding-bottom: 15px
    }

    .hero-next-label {
        display: none
    }
}

@media(max-width:480px) {
    .hero-text {
        padding: 32px 18px 15px
    }

    .hero-title {
        font-size: 32px
    }

    .hero-description {
        font-size: 11px
    }

    .hero-buttons {
        gap: 12px;
        margin-bottom: 27px
    }

    .hero-btn {
        padding: 9px 13px;
        font-size: 10px
    }

    .hero-features {
        gap: 12px
    }

    .hero-feature {
        gap: 5px
    }

    .hero-feature strong {
        font-size: 7px
    }

    .hero-feature span {
        font-size: 6.5px
    }

    .hero-image-wrapper {
        min-height: 220px;
        padding: 0 10px 20px
    }

    .hero-image-stage {
        min-height: 220px
    }

    .hero-image-stage .orbit-one {
        width: 190px;
        height: 190px
    }

    .hero-image-stage .orbit-two {
        width: 240px;
        height: 240px
    }

    .floating-badge {
        transform: scale(.78)
    }

    .badge-one {
        right: -12px;
        top: 10px
    }

    .badge-two {
        left: -12px;
        bottom: 10px
    }

    .hero-indicator {
        width: 43px
    }

    .hero-indicator.active .indicator-track {
        width: 30px
    }

    .indicator-track {
        width: 18px
    }
}

@media(prefers-reduced-motion:reduce) {

    *,
    *::before,
    *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important
    }
}
</style>