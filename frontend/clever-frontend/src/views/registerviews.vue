<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
const router = useRouter()
const firstName = ref("")
const lastName = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const passwordConfirmation = ref("")
const loading = ref(false)
const error = ref("")
const success = ref("")
const showPassword = ref(false)
const showPasswordConfirmation = ref(false)
const register = async () => {
    error.value = ""
    success.value = ""
    if (
        !firstName.value ||
        !lastName.value ||
        !email.value ||
        !password.value ||
        !passwordConfirmation.value
    ) {
        error.value = "Veuillez remplir tous les champs obligatoires."
        return
    }
    if (password.value.length < 8) {
        error.value = "Le mot de passe doit contenir au moins 8 caractères."
        return
    }
    if (password.value !== passwordConfirmation.value) {
        error.value = "Les mots de passe ne correspondent pas."
        return
    }
    try {
        loading.value = true
        const response = await api.post(
            "/accounts/register/",
            {
                first_name: firstName.value,
                last_name: lastName.value,
                email: email.value,
                phone: phone.value,
                password: password.value,
                password_confirmation: passwordConfirmation.value
            }
        )
        if (response.data.token) {
            localStorage.setItem(
                "token",
                response.data.token
            )
        }
        if (response.data.user) {
            localStorage.setItem(
                "user",
                JSON.stringify(response.data.user)
            )
        }
        success.value = "Votre compte a été créé avec succès."
        setTimeout(() => {
            router.push("/")
        }, 1200)
    } catch (err) {
        console.error(
            "Erreur inscription :",
            err
        )
        if (err.response?.data) {
            const data = err.response.data
            if (data.email) {
                error.value = Array.isArray(data.email)
                    ? data.email[0]
                    : data.email
            } else if (data.password) {
                error.value = Array.isArray(data.password)
                    ? data.password[0]
                    : data.password
            } else if (data.detail) {
                error.value = data.detail
            } else if (data.message) {
                error.value = data.message
            } else {
                error.value = "Impossible de créer votre compte."
            }
        } else {
            error.value = "Une erreur est survenue. Vérifiez votre connexion."
        }
    } finally {
        loading.value = false
    }
}
</script>
<template>
    <main class="register-page">
        <section class="register-visual">
            <div class="visual-overlay"></div>
            <div class="visual-content">
                <div class="brand-mark">
                    <i class="fa-solid fa-leaf"></i>
                </div>
                <span class="visual-small-title">
                    BIENVENUE CHEZ
                </span>
                <h1>
                    Clever
                </h1>
                <p>
                    Prenez soin de vous avec des produits
                    sélectionnés pour votre bien-être.
                </p>
                <div class="visual-line"></div>
                <span class="visual-description">
                    Votre beauté, votre santé,
                    votre bien-être.
                </span>
            </div>
        </section>
        <section class="register-form-section">
            <div class="register-container">
                <div class="register-header">
                    <span class="mobile-brand">
                        <i class="fa-solid fa-leaf"></i>
                        Clever
                    </span>
                    <span class="form-small-title">
                        CRÉER UN COMPTE
                    </span>
                    <h2>
                        Bienvenue chez
                        <span>Clever</span>
                    </h2>
                    <p>
                        Créez votre compte et profitez
                        pleinement de notre boutique.
                    </p>
                </div>
                <Transition name="message">
                    <div
                        v-if="error"
                        class="form-message error-message"
                    >
                        <i class="fa-solid fa-circle-exclamation"></i>
                        <span>
                            {{ error }}
                        </span>
                    </div>
                </Transition>
                <Transition name="message">
                    <div
                        v-if="success"
                        class="form-message success-message"
                    >
                        <i class="fa-solid fa-circle-check"></i>
                        <span>
                            {{ success }}
                        </span>
                    </div>
                </Transition>
                <form
                    class="register-form"
                    @submit.prevent="register"
                >
                    <div class="form-row">
                        <div class="form-group">
                            <label>
                                Prénom
                            </label>
                            <div class="input-wrapper">
                                <i class="fa-regular fa-user"></i>
                                <input
                                    v-model="firstName"
                                    type="text"
                                    placeholder="Votre prénom"
                                    autocomplete="given-name"
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <label>
                                Nom
                            </label>
                            <div class="input-wrapper">
                                <i class="fa-regular fa-user"></i>
                                <input
                                    v-model="lastName"
                                    type="text"
                                    placeholder="Votre nom"
                                    autocomplete="family-name"
                                />
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            Adresse email
                        </label>
                        <div class="input-wrapper">
                            <i class="fa-regular fa-envelope"></i>
                            <input
                                v-model="email"
                                type="email"
                                placeholder="exemple@email.com"
                                autocomplete="email"
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            Téléphone
                            <small>(facultatif)</small>
                        </label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-phone"></i>
                            <input
                                v-model="phone"
                                type="tel"
                                placeholder="Votre numéro de téléphone"
                                autocomplete="tel"
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            Mot de passe
                        </label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-lock"></i>
                            <input
                                v-model="password"
                                :type="showPassword ? 'text' : 'password'"
                                placeholder="Minimum 8 caractères"
                                autocomplete="new-password"
                            />
                            <button
                                type="button"
                                class="password-button"
                                @click="showPassword = !showPassword"
                            >
                                <i
                                    :class="showPassword ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"
                                ></i>
                            </button>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            Confirmer le mot de passe
                        </label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-lock"></i>
                            <input
                                v-model="passwordConfirmation"
                                :type="showPasswordConfirmation ? 'text' : 'password'"
                                placeholder="Confirmez votre mot de passe"
                                autocomplete="new-password"
                            />
                            <button
                                type="button"
                                class="password-button"
                                @click="showPasswordConfirmation = !showPasswordConfirmation"
                            >
                                <i
                                    :class="showPasswordConfirmation ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"
                                ></i>
                            </button>
                        </div>
                    </div>
                    <div class="terms">
                        <i class="fa-solid fa-shield-heart"></i>
                        <p>
                            En créant votre compte, vous
                            acceptez nos conditions
                            d'utilisation et notre politique
                            de confidentialité.
                        </p>
                    </div>
                    <button
                        type="submit"
                        class="register-button"
                        :disabled="loading"
                    >
                        <span v-if="!loading">
                            Créer mon compte
                            <i class="fa-solid fa-arrow-right"></i>
                        </span>
                        <span
                            v-else
                            class="loading-content"
                        >
                            <i class="fa-solid fa-spinner fa-spin"></i>
                            Création du compte...
                        </span>
                    </button>
                </form>
                <div class="login-link">
                    <span>
                        Vous avez déjà un compte ?
                    </span>
                    <RouterLink to="/connexion">
                        Se connecter
                    </RouterLink>
                </div>
                <RouterLink
                    to="/"
                    class="back-home"
                >
                    <i class="fa-solid fa-arrow-left"></i>
                    Retour à l'accueil
                </RouterLink>
            </div>
        </section>
    </main>
</template>
<style scoped>
.register-page {
    width: 100%;
    min-height: 100vh;
    display: grid;
    grid-template-columns: 43% 57%;
    background: #ffffff;
}
.register-visual {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(
            135deg,
            #38B04C 0%,
            #2f963f 55%,
            #267b34 100%
        );
}
.register-visual::before {
    content: "";
    position: absolute;
    width: 430px;
    height: 430px;
    top: -180px;
    left: -170px;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 50%;
}
.register-visual::after {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    right: -300px;
    bottom: -260px;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 50%;
}
.visual-overlay {
    position: absolute;
    inset: 0;
    background:
        radial-gradient(
            circle at 20% 20%,
            rgba(255,255,255,.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 80%,
            rgba(0,0,0,.10),
            transparent 35%
        );
}
.visual-content {
    position: relative;
    z-index: 2;
    max-width: 390px;
    padding: 40px;
    color: #ffffff;
    top: -5em;
}
.brand-mark {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 45px;
    border: 1px solid rgba(255,255,255,.35);
    border-radius: 50%;
    background: rgba(255,255,255,.12);
    backdrop-filter: blur(8px);
}
.brand-mark i {
    font-size: 21px;
}
.visual-small-title {
    display: block;
    margin-bottom: 8px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
}
.visual-content h1 {
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(55px, 7vw, 90px);
    font-weight: 400;
    line-height: .95;
}
.visual-content p {
    max-width: 330px;
    margin: 25px 0 0;
    color: rgba(255,255,255,.88);
    font-size: 13px;
    line-height: 1.8;
}
.visual-line {
    width: 48px;
    height: 1px;
    margin: 28px 0 15px;
    background: rgba(255,255,255,.7);
}
.visual-description {
    color: rgba(255,255,255,.75);
    font-size: 10px;
    letter-spacing: 1px;
}
.register-form-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 45px 50px;
}
.register-container {
    width: 100%;
    max-width: 560px;
}
.register-header {
    margin-bottom: 25px;
}
.mobile-brand {
    display: none;
}
.form-small-title {
    display: block;
    margin-bottom: 8px;
    color: #38B04C;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
}
.register-header h2 {
    margin: 0;
    color: #202020;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 34px;
    font-weight: 400;
    line-height: 1.2;
}
.register-header h2 span {
    color: #38B04C;
}
.register-header p {
    margin: 10px 0 0;
    color: #8b8b8b;
    font-size: 11px;
    line-height: 1.7;
}
.form-message {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 18px;
    padding: 11px 13px;
    border-radius: 6px;
    font-size: 10px;
}
.error-message {
    border: 1px solid #f2d3d3;
    background: #fff6f6;
    color: #c44;
}
.success-message {
    border: 1px solid #cfead4;
    background: #f2fbf4;
    color: #2f963f;
}
.register-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 13px;
}
.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.form-group label {
    color: #333;
    font-size: 10px;
    font-weight: 600;
}
.form-group label small {
    color: #aaa;
    font-size: 8px;
    font-weight: 400;
}
.input-wrapper {
    position: relative;
    width: 100%;
}
.input-wrapper > i {
    position: absolute;
    top: 50%;
    left: 14px;
    color: #a5a5a5;
    font-size: 11px;
    transform: translateY(-50%);
    pointer-events: none;
    transition: .25s ease;
}
.input-wrapper input {
    width: 100%;
    height: 43px;
    padding: 0 42px;
    border: 1px solid #e3e7e4;
    border-radius: 6px;
    outline: none;
    background: #ffffff;
    color: #222;
    font-family: inherit;
    font-size: 11px;
    transition: .25s ease;
    box-sizing: border-box;
}
.input-wrapper input::placeholder {
    color: #b8b8b8;
}
.input-wrapper input:focus {
    border-color: #38B04C;
    box-shadow: 0 0 0 3px rgba(56,176,76,.08);
}
.input-wrapper:focus-within > i {
    color: #38B04C;
}
.password-button {
    position: absolute;
    top: 50%;
    right: 11px;
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: 0;
    background: transparent;
    color: #999;
    cursor: pointer;
    transform: translateY(-50%);
}
.password-button:hover {
    color: #38B04C;
}
.password-button i {
    font-size: 11px;
}
.terms {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    margin-top: 2px;
}
.terms i {
    margin-top: 2px;
    color: #38B04C;
    font-size: 11px;
}
.terms p {
    margin: 0;
    color: #999;
    font-size: 9px;
    line-height: 1.6;
}
.register-button {
    width: 100%;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 3px;
    border: 0;
    border-radius: 6px;
    background: #38B04C;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: .3s ease;
}
.register-button:hover:not(:disabled) {
    background: #2f963f;
    box-shadow: 0 8px 20px rgba(56,176,76,.20);
    transform: translateY(-1px);
}
.register-button:disabled {
    opacity: .65;
    cursor: not-allowed;
}
.register-button span {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
}
.register-button i {
    font-size: 10px;
}
.loading-content {
    gap: 8px !important;
}
.login-link {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    margin-top: 23px;
    color: #999;
    font-size: 10px;
}
.login-link a {
    color: #38B04C;
    font-weight: 600;
    text-decoration: none;
}
.login-link a:hover {
    text-decoration: underline;
}
.back-home {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    margin-top: 22px;
    color: #aaa;
    font-size: 9px;
    text-decoration: none;
    transition: .2s ease;
}
.back-home:hover {
    color: #38B04C;
}
.back-home i {
    font-size: 8px;
}
.message-enter-active,
.message-leave-active {
    transition: all .25s ease;
}
.message-enter-from,
.message-leave-to {
    opacity: 0;
    transform: translateY(-5px);
}
@media (max-width: 1000px) {
    .register-page {
        grid-template-columns: 38% 62%;
    }
    .register-form-section {
        padding: 35px;
    }
    .visual-content {
        padding: 30px;
    }
    .register-header h2 {
        font-size: 29px;
    }
}
@media (max-width: 768px) {
    .register-page {
        display: block;
        min-height: 100vh;
    }
    .register-visual {
        min-height: 235px;
        height: 235px;
    }
    .visual-content {
        width: 100%;
        max-width: 500px;
        padding: 30px;
        text-align: center;
    }
    .brand-mark {
        width: 40px;
        height: 40px;
        margin: 0 auto 15px;
    }
    .brand-mark i {
        font-size: 16px;
    }
    .visual-small-title {
        font-size: 8px;
        letter-spacing: 2px;
    }
    .visual-content h1 {
        font-size: 48px;
    }
    .visual-content p {
        max-width: 350px;
        margin: 12px auto 0;
        font-size: 10px;
    }
    .visual-line,
    .visual-description {
        display: none;
    }
    .register-form-section {
        min-height: auto;
        padding: 35px 22px 45px;
    }
    .register-container {
        max-width: 500px;
    }
    .mobile-brand {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 22px;
        color: #38B04C;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 18px;
    }
    .mobile-brand i {
        font-size: 13px;
    }
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
}
@media (max-width: 480px) {
    .register-visual {
        min-height: 210px;
        height: 210px;
    }
    .visual-content h1 {
        font-size: 43px;
    }
    .register-form-section {
        padding: 30px 17px 40px;
    }
    .register-header h2 {
        font-size: 27px;
    }
    .register-header p {
        font-size: 10px;
    }
    .input-wrapper input {
        height: 45px;
    }
    .register-button {
        height: 46px;
    }
}
</style>