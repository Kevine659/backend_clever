<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

const login = async () => {
    errorMessage.value = ""
    successMessage.value = ""

    if (!email.value || !password.value) {
        errorMessage.value = "Veuillez remplir tous les champs."
        return
    }

    try {
        loading.value = true

        const response = await api.post(
            "/accounts/login/",
            {
                email: email.value,
                password: password.value
            }
        )

        const data = response.data

        if (data.token) {
            localStorage.setItem(
                "auth_token",
                data.token
            )

            localStorage.setItem(
                "token",
                data.token
            )
        }

        if (data.user) {
            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            )
        }

        successMessage.value =
            "Connexion réussie. Redirection..."

        setTimeout(() => {
            router.push("/")
        }, 700)

    } catch (error) {
        console.error(
            "Erreur de connexion :",
            error
        )

        if (error.response) {
            if (
                error.response.status === 401
            ) {
                errorMessage.value =
                    error.response.data?.message ||
                    "Email ou mot de passe incorrect."
            } else if (
                error.response.status === 400
            ) {
                errorMessage.value =
                    error.response.data?.message ||
                    "Veuillez vérifier les informations saisies."
            } else {
                errorMessage.value =
                    "Une erreur est survenue lors de la connexion."
            }
        } else {
            errorMessage.value =
                "Impossible de contacter le serveur."
        }

    } finally {
        loading.value = false
    }
}

const togglePassword = () => {
    showPassword.value =
        !showPassword.value
}
</script>

<template>
    <section class="login-section">
        <div class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <div class="login-icon">
                        <i class="fa-solid fa-user"></i>
                    </div>

                    <span class="login-small-title">
                        ESPACE CLIENT
                    </span>

                    <h1>
                        Bon retour
                    </h1>

                    <p>
                        Connectez-vous à votre compte
                        pour continuer vos achats.
                    </p>
                </div>

                <div
                    v-if="errorMessage"
                    class="message error-message"
                >
                    <i class="fa-solid fa-circle-exclamation"></i>

                    <span>
                        {{ errorMessage }}
                    </span>
                </div>

                <div
                    v-if="successMessage"
                    class="message success-message"
                >
                    <i class="fa-solid fa-circle-check"></i>

                    <span>
                        {{ successMessage }}
                    </span>
                </div>

                <form
                    class="login-form"
                    @submit.prevent="login"
                >
                    <div class="form-group">
                        <label for="email">
                            Adresse email
                        </label>

                        <div class="input-wrapper">
                            <i class="fa-regular fa-envelope"></i>

                            <input
                                id="email"
                                v-model="email"
                                type="email"
                                placeholder="votre@email.com"
                                autocomplete="email"
                                :disabled="loading"
                            />
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="password">
                            Mot de passe
                        </label>

                        <div class="input-wrapper">
                            <i class="fa-solid fa-lock"></i>

                            <input
                                id="password"
                                v-model="password"
                                :type="
                                    showPassword
                                        ? 'text'
                                        : 'password'
                                "
                                placeholder="Votre mot de passe"
                                autocomplete="current-password"
                                :disabled="loading"
                            />

                            <button
                                type="button"
                                class="password-button"
                                @click="togglePassword"
                                :disabled="loading"
                                :aria-label="
                                    showPassword
                                        ? 'Masquer le mot de passe'
                                        : 'Afficher le mot de passe'
                                "
                            >
                                <i
                                    :class="
                                        showPassword
                                            ? 'fa-solid fa-eye-slash'
                                            : 'fa-solid fa-eye'
                                    "
                                ></i>
                            </button>
                        </div>
                    </div>

                    <div class="form-options">
                        <label class="remember-me">
                            <input
                                type="checkbox"
                            />

                            <span>
                                Se souvenir de moi
                            </span>
                        </label>

                        <RouterLink
                            to="/mot-de-passe-oublie"
                            class="forgot-password"
                        >
                            Mot de passe oublié ?
                        </RouterLink>
                    </div>

                    <button
                        type="submit"
                        class="login-button"
                        :disabled="loading"
                    >
                        <span
                            v-if="loading"
                            class="button-loader"
                        ></span>

                        <i
                            v-else
                            class="fa-solid fa-right-to-bracket"
                        ></i>

                        <span>
                            {{
                                loading
                                    ? "Connexion..."
                                    : "Se connecter"
                            }}
                        </span>
                    </button>
                </form>

                <div class="separator">
                    <span>
                        OU
                    </span>
                </div>

                <div class="register-section">
                    <p>
                        Vous n'avez pas encore de compte ?
                    </p>

                    <RouterLink
                        to="/inscription"
                        class="register-button"
                    >
                        <i class="fa-solid fa-user-plus"></i>

                        Créer un compte
                    </RouterLink>
                </div>

                <div class="login-footer">
                    <RouterLink to="/">
                        <i class="fa-solid fa-arrow-left"></i>

                        Retour à la boutique
                    </RouterLink>
                </div>
            </div>

            <div class="login-decoration">
                <div class="decoration-circle circle-one"></div>

                <div class="decoration-circle circle-two"></div>

                <div class="decoration-content">
                    <div class="decoration-icon">
                        <i class="fa-solid fa-leaf"></i>
                    </div>

                    <span>
                        VOTRE BIEN-ÊTRE
                    </span>

                    <h2>
                        Prenez soin de vous,
                        <strong>chaque jour.</strong>
                    </h2>

                    <p>
                        Retrouvez vos produits préférés
                        et profitez d'une expérience
                        d'achat simple et agréable.
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.login-section {
    width: 100%;
    min-height: calc(100vh - 80px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 50px 20px;
    background:
        linear-gradient(
            135deg,
            #f7fbf7 0%,
            #ffffff 50%,
            #eef8f0 100%
        );
}

.login-container {
    width: 100%;
    max-width: 1050px;
    min-height: 620px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    overflow: hidden;
    border: 1px solid #e5ebe6;
    border-radius: 16px;
    background: #ffffff;
    box-shadow:
        0 20px 60px rgba(0, 0, 0, .08);
}

.login-card {
    width: 100%;
    padding: 48px 55px;
    background: #ffffff;
}

.login-header {
    text-align: center;
    margin-bottom: 28px;
}

.login-icon {
    width: 54px;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    border-radius: 50%;
    background: #eef8f0;
    color: #38B04C;
}

.login-icon i {
    font-size: 18px;
}

.login-small-title {
    display: block;
    margin-bottom: 8px;
    color: #38B04C;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
}

.login-header h1 {
    margin: 0 0 8px;
    color: #202020;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 34px;
    font-weight: 500;
}

.login-header p {
    max-width: 340px;
    margin: 0 auto;
    color: #888;
    font-size: 12px;
    line-height: 1.7;
}

.message {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 18px;
    padding: 11px 13px;
    border-radius: 6px;
    font-size: 11px;
    line-height: 1.4;
}

.error-message {
    border: 1px solid #f1d6d6;
    background: #fff6f6;
    color: #c44;
}

.success-message {
    border: 1px solid #d4ead8;
    background: #f2faf3;
    color: #38B04C;
}

.message i {
    font-size: 12px;
}

.login-form {
    width: 100%;
}

.form-group {
    margin-bottom: 19px;
}

.form-group label {
    display: block;
    margin-bottom: 7px;
    color: #333;
    font-size: 11px;
    font-weight: 600;
}

.input-wrapper {
    width: 100%;
    height: 47px;
    position: relative;
    display: flex;
    align-items: center;
    border: 1px solid #dfe5e0;
    border-radius: 7px;
    background: #ffffff;
    transition: .25s ease;
}

.input-wrapper:focus-within {
    border-color: #38B04C;
    box-shadow:
        0 0 0 3px rgba(56, 176, 76, .08);
}

.input-wrapper > i {
    width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
    font-size: 13px;
}

.input-wrapper:focus-within > i {
    color: #38B04C;
}

.input-wrapper input {
    width: 100%;
    height: 100%;
    padding: 0 14px 0 0;
    border: 0;
    outline: 0;
    background: transparent;
    color: #222;
    font-family: inherit;
    font-size: 12px;
}

.input-wrapper input::placeholder {
    color: #aaa;
}

.input-wrapper input:disabled {
    opacity: .6;
}

.password-button {
    width: 42px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0;
    background: transparent;
    color: #999;
    cursor: pointer;
}

.password-button:hover {
    color: #38B04C;
}

.password-button i {
    font-size: 12px;
}

.form-options {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin: 2px 0 22px;
}

.remember-me {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #777;
    font-size: 10px;
    cursor: pointer;
}

.remember-me input {
    width: 13px;
    height: 13px;
    accent-color: #38B04C;
    cursor: pointer;
}

.forgot-password {
    color: #38B04C;
    font-size: 10px;
    text-decoration: none;
}

.forgot-password:hover {
    text-decoration: underline;
}

.login-button {
    width: 100%;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    border: 1px solid #38B04C;
    border-radius: 7px;
    background: #38B04C;
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: .25s ease;
}

.login-button:hover:not(:disabled) {
    background: #2f963f;
    border-color: #2f963f;
    transform: translateY(-1px);
    box-shadow:
        0 8px 18px rgba(56, 176, 76, .2);
}

.login-button:disabled {
    opacity: .7;
    cursor: not-allowed;
}

.login-button i {
    font-size: 11px;
}

.button-loader {
    width: 13px;
    height: 13px;
    display: inline-block;
    border: 2px solid rgba(255,255,255,.4);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: loginSpin .7s linear infinite;
}

@keyframes loginSpin {
    to {
        transform: rotate(360deg);
    }
}

.separator {
    width: 100%;
    height: 1px;
    position: relative;
    margin: 27px 0 22px;
    background: #eeeeee;
}

.separator span {
    position: absolute;
    top: 50%;
    left: 50%;
    padding: 0 12px;
    transform: translate(-50%, -50%);
    background: #ffffff;
    color: #aaa;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 1px;
}

.register-section {
    text-align: center;
}

.register-section p {
    margin: 0 0 12px;
    color: #888;
    font-size: 10px;
}

.register-button {
    min-height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 0 17px;
    border: 1px solid #dce6de;
    border-radius: 20px;
    background: #ffffff;
    color: #333;
    font-size: 10px;
    font-weight: 600;
    text-decoration: none;
    transition: .25s ease;
}

.register-button:hover {
    border-color: #38B04C;
    background: #38B04C;
    color: #ffffff;
    transform: translateY(-1px);
}

.register-button i {
    font-size: 10px;
}

.login-footer {
    margin-top: 27px;
    text-align: center;
}

.login-footer a {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #999;
    font-size: 9px;
    text-decoration: none;
    transition: .2s ease;
}

.login-footer a:hover {
    color: #38B04C;
}

.login-footer i {
    font-size: 8px;
}

.login-decoration {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background:
        linear-gradient(
            145deg,
            #38B04C 0%,
            #318f42 55%,
            #267537 100%
        );
}

.decoration-circle {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,.15);
}

.circle-one {
    width: 430px;
    height: 430px;
    right: -190px;
    top: -160px;
}

.circle-two {
    width: 300px;
    height: 300px;
    left: -160px;
    bottom: -120px;
}

.decoration-content {
    position: relative;
    z-index: 2;
    max-width: 350px;
    padding: 40px;
    color: #ffffff;
}

.decoration-icon {
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,.35);
    border-radius: 50%;
    background: rgba(255,255,255,.1);
}

.decoration-icon i {
    font-size: 20px;
}

.decoration-content > span {
    display: block;
    margin-bottom: 12px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2px;
}

.decoration-content h2 {
    margin: 0 0 17px;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 37px;
    font-weight: 400;
    line-height: 1.15;
}

.decoration-content h2 strong {
    display: block;
    font-weight: 500;
}

.decoration-content p {
    max-width: 310px;
    margin: 0;
    color: rgba(255,255,255,.85);
    font-size: 12px;
    line-height: 1.8;
}

@media(max-width:850px) {
    .login-container {
        max-width: 600px;
        grid-template-columns: 1fr;
    }

    .login-decoration {
        display: none;
    }

    .login-card {
        padding: 45px 55px;
    }
}

@media(max-width:576px) {
    .login-section {
        min-height: 100vh;
        padding: 25px 14px;
    }

    .login-container {
        border-radius: 12px;
    }

    .login-card {
        padding: 35px 22px;
    }

    .login-header h1 {
        font-size: 30px;
    }

    .form-options {
        align-items: flex-start;
        flex-direction: column;
    }

    .forgot-password {
        align-self: flex-end;
    }
}
</style>