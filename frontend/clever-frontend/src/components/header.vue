<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { RouterLink, useRouter, useRoute } from "vue-router"
import api from "../services/api"

const router = useRouter()
const route = useRoute()

const searchQuery = ref("")
const cart = ref([])
const favoriteIds = ref([])
const favoritesLoading = ref(false)
const searchLoading = ref(false)
const searchResults = ref([])
const showSearchResults = ref(false)

let refreshInterval = null
let searchTimeout = null

const isAuthenticated = computed(() => {
    return !!localStorage.getItem("token")
})

const cartItemsCount = computed(() => {
    return cart.value.reduce(
        (total, item) => {
            return total + Number(item.quantity || 0)
        },
        0
    )
})

const favoritesCount = computed(() => {
    return favoriteIds.value.length
})

const getGuestId = () => {
    let guestId = localStorage.getItem("guest_id")
    if (!guestId) {
        if (window.crypto && window.crypto.randomUUID) {
            guestId = window.crypto.randomUUID()
        } else {
            guestId = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
                /[xy]/g,
                c => {
                    const r = Math.random() * 16 | 0
                    const v = c === "x" ? r : (r & 0x3 | 0x8)
                    return v.toString(16)
                }
            )
        }
        localStorage.setItem("guest_id", guestId)
    }
    return guestId
}

const getFavoriteHeaders = () => {
    if (isAuthenticated.value) {
        return {}
    }
    return {
        "X-Guest-ID": getGuestId()
    }
}

const extractFavoriteProductId = item => {
    if (!item) return 0
    if (typeof item === "number") {
        return Number(item)
    }
    if (typeof item === "string") {
        const id = Number(item)
        return Number.isFinite(id) ? id : 0
    }
    if (typeof item !== "object") {
        return 0
    }
    if (item.product_id) {
        const id = Number(item.product_id)
        if (Number.isFinite(id) && id > 0) {
            return id
        }
    }
    if (item.product !== undefined && item.product !== null) {
        if (typeof item.product === "number" || typeof item.product === "string") {
            const id = Number(item.product)
            if (Number.isFinite(id) && id > 0) {
                return id
            }
        }
        if (typeof item.product === "object" && item.product.id) {
            const id = Number(item.product.id)
            if (Number.isFinite(id) && id > 0) {
                return id
            }
        }
    }
    if (item.product_detail && typeof item.product_detail === "object" && item.product_detail.id) {
        const id = Number(item.product_detail.id)
        if (Number.isFinite(id) && id > 0) {
            return id
        }
    }
    if (item.product_data && typeof item.product_data === "object" && item.product_data.id) {
        const id = Number(item.product_data.id)
        if (Number.isFinite(id) && id > 0) {
            return id
        }
    }
    return 0
}

const normalizeCartItem = item => {
    if (!item) return null

    if (
        item.type === "range" ||
        item.item_type === "range" ||
        item.range_id !== undefined ||
        item.product_range_id !== undefined ||
        item.product_range !== undefined
    ) {
        const rangeId = Number(
            item.range_id ||
            item.product_range_id ||
            item.product_range ||
            item.id
        )
        if (!rangeId || Number.isNaN(rangeId)) {
            return null
        }
        return {
            type: "range",
            item_type: "range",
            range_id: rangeId,
            product_range: rangeId,
            id: `range_${rangeId}`,
            name: item.name || item.product_range_name || "Gamme",
            quantity: Number(item.quantity || 1)
        }
    }

    if (
        item.type === "product" ||
        item.item_type === "product" ||
        item.product_id !== undefined ||
        item.product !== undefined
    ) {
        const productId = Number(
            item.product_id ||
            item.product ||
            item.id
        )
        if (!productId || Number.isNaN(productId)) {
            return null
        }
        return {
            type: "product",
            item_type: "product",
            product_id: productId,
            product: productId,
            id: `product_${productId}`,
            name: item.name || item.product_name || "Produit",
            quantity: Number(item.quantity || 1)
        }
    }

    return null
}

const loadCart = () => {
    try {
        const savedCart = localStorage.getItem("shop_cart")

        if (!savedCart) {
            cart.value = []
            return
        }

        const parsedCart = JSON.parse(savedCart)

        if (!Array.isArray(parsedCart)) {
            cart.value = []
            return
        }

        cart.value = parsedCart
            .map(normalizeCartItem)
            .filter(Boolean)
    } catch (err) {
        console.error("Erreur chargement panier Header :", err)
        cart.value = []
    }
}

const loadGuestFavorites = () => {
    try {
        const saved = localStorage.getItem("shop_favorites")

        if (!saved) {
            favoriteIds.value = []
            return
        }

        const parsed = JSON.parse(saved)

        if (!Array.isArray(parsed)) {
            favoriteIds.value = []
            return
        }

        favoriteIds.value = [
            ...new Set(
                parsed
                    .map(id => Number(id))
                    .filter(
                        id => Number.isFinite(id) && id > 0
                    )
            )
        ]
    } catch (err) {
        console.error("Erreur chargement favoris visiteur Header :", err)
        favoriteIds.value = []
    }
}

const loadFavorites = async () => {
    try {
        favoritesLoading.value = true

        if (!isAuthenticated.value) {
            loadGuestFavorites()
            return
        }

        const response = await api.get(
            "/favorites/",
            {
                headers: getFavoriteHeaders()
            }
        )

        const data =
            response.data?.results ||
            response.data ||
            []

        if (!Array.isArray(data)) {
            favoriteIds.value = []
            return
        }

        favoriteIds.value = [
            ...new Set(
                data
                    .map(extractFavoriteProductId)
                    .filter(
                        id => Number.isFinite(id) && id > 0
                    )
            )
        ]
    } catch (err) {
        console.error("Erreur chargement favoris Header :", err)

        if (!isAuthenticated.value) {
            loadGuestFavorites()
        } else {
            favoriteIds.value = []
        }
    } finally {
        favoritesLoading.value = false
    }
}

const refreshHeader = async () => {
    loadCart()

    if (!isAuthenticated.value) {
        loadGuestFavorites()
        return
    }

    await loadFavorites()
}

const getProductImage = image => {
    if (!image || typeof image !== "string") {
        return null
    }

    image = image.trim()

    if (!image) {
        return null
    }

    if (
        image.startsWith("http://") ||
        image.startsWith("https://")
    ) {
        return image
    }

    if (image.startsWith("data:image")) {
        return image
    }

    const baseURL =
        api.defaults.baseURL ||
        "http://127.0.0.1:7000/api"

    const serverURL =
        baseURL
            .replace(/\/api\/?$/, "")
            .replace(/\/$/, "")

    return `${serverURL}${image.startsWith("/") ? image : `/${image}`}`
}

const formatPrice = price => {
    const number = Number(price || 0)

    if (!Number.isFinite(number)) {
        return "0 FCFA"
    }

    return new Intl.NumberFormat(
        "fr-FR",
        {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }
    ).format(number) + " FCFA"
}

const searchProducts = async () => {
    const search = searchQuery.value.trim()

    if (searchTimeout) {
        clearTimeout(searchTimeout)
        searchTimeout = null
    }

    showSearchResults.value = false

    if (!search) {
        searchResults.value = []
        await router.push({
            path: "/boutique",
            query: {}
        })
        return
    }

    await router.push({
        path: "/boutique",
        query: {
            search
        }
    })
}

const searchSuggestions = () => {
    const search = searchQuery.value.trim()

    if (searchTimeout) {
        clearTimeout(searchTimeout)
        searchTimeout = null
    }

    if (search.length < 2) {
        searchResults.value = []
        showSearchResults.value = false
        searchLoading.value = false
        return
    }

    showSearchResults.value = true

    searchTimeout = setTimeout(
        async () => {
            try {
                searchLoading.value = true

                const response = await api.get(
                    "/products/",
                    {
                        params: {
                            search
                        }
                    }
                )

                const data =
                    response.data?.results ||
                    response.data ||
                    []

                searchResults.value = Array.isArray(data)
                    ? data.slice(0, 6)
                    : []

            } catch (err) {
                console.error("Erreur recherche produits Header :", err)
                searchResults.value = []
            } finally {
                searchLoading.value = false
            }
        },
        350
    )
}

const handleSearchKeydown = event => {
    if (event.key === "Enter") {
        event.preventDefault()
        searchProducts()
    }
}

const selectSearchResult = async product => {
    if (!product || !product.slug) {
        return
    }

    showSearchResults.value = false
    searchResults.value = []
    searchQuery.value = product.name || ""

    await router.push({
        path: "/produit",
        query: {
            slug: product.slug
        }
    })
}

const clearSearch = () => {
    searchQuery.value = ""
    searchResults.value = []
    showSearchResults.value = false

    if (searchTimeout) {
        clearTimeout(searchTimeout)
        searchTimeout = null
    }
}

const handleOutsideSearch = event => {
    const searchElement = document.querySelector(".search-container")

    if (
        searchElement &&
        !searchElement.contains(event.target)
    ) {
        showSearchResults.value = false
    }
}

const syncSearchWithRoute = () => {
    const routeSearch = route.query.search

    if (typeof routeSearch === "string") {
        searchQuery.value = routeSearch
    } else {
        searchQuery.value = ""
    }

    searchResults.value = []
    showSearchResults.value = false
}

const logout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    favoriteIds.value = []
    cart.value = []
    router.push("/connexion")
}

watch(
    () => route.query.search,
    () => {
        syncSearchWithRoute()
    }
)

watch(
    searchQuery,
    () => {
        searchSuggestions()
    }
)

onMounted(async () => {
    syncSearchWithRoute()

    await refreshHeader()

    refreshInterval = setInterval(
        () => {
            refreshHeader()
        },
        1000
    )

    document.addEventListener(
        "click",
        handleOutsideSearch
    )
})

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
    }

    if (searchTimeout) {
        clearTimeout(searchTimeout)
        searchTimeout = null
    }

    document.removeEventListener(
        "click",
        handleOutsideSearch
    )
})
</script>

<template>
    <header class="site-header">
        <div class="top-header">
            <div class="container header-container">
                <RouterLink to="/" class="logo-link">
                    <img src="../assets/logo.png" alt="Logo boutique" class="logo">
                </RouterLink>

                <div class="search-container">
                    <form class="search-box" @submit.prevent="searchProducts">
                        <input v-model="searchQuery" type="text" placeholder="Rechercher un produit..."
                            autocomplete="off" @focus="showSearchResults = searchResults.length > 0"
                            @keydown="handleSearchKeydown">
                        <button type="submit" title="Rechercher">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </button>

                        <button v-if="searchQuery" type="button" class="clear-search-button" title="Effacer"
                            @click="clearSearch">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </form>

                    <div v-if="showSearchResults" class="search-results">
                        <div v-if="searchLoading" class="search-loading">
                            <i class="fa-solid fa-circle-notch fa-spin"></i>
                            <span>Recherche...</span>
                        </div>

                        <template v-else>
                            <button v-for="product in searchResults" :key="product.id" type="button"
                                class="search-result-item" @click="selectSearchResult(product)">
                                <div class="search-result-image">
                                    <img v-if="product.main_image" :src="getProductImage(product.main_image)"
                                        :alt="product.name">
                                    <div v-else class="search-no-image">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                </div>

                                <div class="search-result-info">
                                    <strong>
                                        {{ product.name }}
                                    </strong>

                                    <span v-if="product.subcategory_name">
                                        {{ product.subcategory_name }}
                                    </span>

                                    <strong class="search-result-price">
                                        {{
                                            formatPrice(
                                                product.current_price ??
                                                product.promotional_price ??
                                                product.price
                                            )
                                        }}
                                    </strong>
                                </div>

                                <i class="fa-solid fa-arrow-right"></i>
                            </button>

                            <button v-if="searchResults.length > 0" type="button" class="search-all-button"
                                @click="searchProducts">
                                Voir tous les résultats pour
                                <strong>
                                    "{{ searchQuery }}"
                                </strong>
                            </button>

                            <div v-if="
                                !searchLoading &&
                                searchResults.length === 0 &&
                                searchQuery.trim().length >= 2
                            " class="search-empty">
                                <i class="fa-solid fa-magnifying-glass"></i>
                                <span>Aucun produit trouvé.</span>
                            </div>
                        </template>
                    </div>
                </div>

                <div class="header-actions">
                    <RouterLink to="/" class="header-action">
                        <i class="fa-solid fa-house"></i>
                        <span>Accueil</span>
                    </RouterLink>

                    <RouterLink to="/a-propos" class="header-action">
                        <i class="fa-solid fa-circle-info"></i>
                        <span>À propos</span>
                    </RouterLink>

                    <RouterLink to="/contact" class="header-action">
                        <i class="fa-solid fa-envelope"></i>
                        <span>Contact</span>
                    </RouterLink>

                    <RouterLink to="/favoris" class="header-action">
                        <div class="icon-wrapper">
                            <i class="fa-regular fa-heart"></i>

                            <span v-if="favoritesCount > 0" class="action-badge">
                                {{ favoritesCount }}
                            </span>
                        </div>

                        <span>Favoris</span>
                    </RouterLink>

                    <RouterLink to="/panier" class="header-action">
                        <div class="icon-wrapper">
                            <i class="fa-solid fa-cart-shopping"></i>

                            <span v-if="cartItemsCount > 0" class="action-badge">
                                {{ cartItemsCount }}
                            </span>
                        </div>

                        <span>Panier</span>
                    </RouterLink>

                    <div v-if="isAuthenticated" class="account-menu">
                        <RouterLink to="/profil" class="header-action">
                            <i class="fa-regular fa-circle-user"></i>
                            <span>Mon compte</span>
                        </RouterLink>

                        <button type="button" class="logout-button" @click="logout" title="Déconnexion">
                            <i class="fa-solid fa-right-from-bracket"></i>
                        </button>
                    </div>

                    <RouterLink v-else to="/connexion" class="header-action">
                        <i class="fa-regular fa-circle-user"></i>
                        <span>Connexion</span>
                    </RouterLink>
                </div>
            </div>
        </div>

        <nav class="main-navigation">
            <div class="container navigation-container">
                <RouterLink to="/" class="nav-link">
                    <i class="fa-solid fa-house"></i>
                    Accueil
                </RouterLink>

                <RouterLink to="/boutique" class="nav-link">
                    <i class="fa-solid fa-store"></i>
                    Boutique
                </RouterLink>

                <RouterLink to="/cosmetiques" class="nav-link">
                    <i class="fa-solid fa-spa"></i>
                    Cosmétiques
                </RouterLink>

                <RouterLink to="/sante" class="nav-link">
                    <i class="fa-solid fa-heart-pulse"></i>
                    Santé
                </RouterLink>

                <RouterLink to="/fertilite" class="nav-link">
                    <i class="fa-solid fa-person-pregnant"></i>
                    Fertilité
                </RouterLink>

                <RouterLink to="/dietetique" class="nav-link">
                    <i class="fa-solid fa-leaf"></i>
                    Diététique
                </RouterLink>

                <RouterLink to="/promotions" class="nav-link promotion-link">
                    <i class="fa-solid fa-tag"></i>
                    Promotions
                </RouterLink>
            </div>
        </nav>
    </header>
</template>

<style scoped>
.site-header {
    width: 100%;
    background: #fff;
    border-bottom: 1px solid #eee;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 12px rgba(0, 0, 0, .04);
}

.top-header {
    background: #fff;
}

.header-container {
    min-height: 65px;
    display: flex;
    align-items: center;
    gap: 24px;
}

.logo-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    flex-shrink: 0;
}

.logo {
    width: 90px;
    height: auto;
    max-height: 40px;
    object-fit: contain;
    display: block;
}

.search-container {
    position: relative;
    flex: 1;
    max-width: 400px;
    margin: 0 auto;
}

.search-box {
    height: 34px;
    display: flex;
    align-items: center;
    width: 100%;
    border: 1px solid #e3e3e3;
    border-radius: 5px;
    overflow: hidden;
    background: #fafafa;
    transition: .2s ease;
}

.search-box:focus-within {
    border-color: #38b04c;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(56, 176, 76, .08);
}

.search-box input {
    height: 100%;
    flex: 1;
    min-width: 0;
    border: 0;
    outline: none;
    background: transparent;
    padding: 0 14px;
    font-size: 12px;
    color: #333;
}

.search-box input::placeholder {
    color: #999;
}

.search-box button {
    width: 42px;
    height: 100%;
    border: 0;
    background: #38b04c;
    color: #fff;
    font-size: 13px;
    cursor: pointer;
    transition: background .2s ease;
}

.search-box button:hover {
    background: #2f983f;
}

.search-box .clear-search-button {
    width: 30px;
    background: #fff;
    color: #999;
}

.search-box .clear-search-button:hover {
    background: #f4f7f4;
    color: #38b04c;
}

.search-results {
    position: absolute;
    top: calc(100% + 7px);
    left: 0;
    right: 0;
    background: #fff;
    border: 1px solid #e6ebe6;
    box-shadow: 0 12px 30px rgba(0, 0, 0, .10);
    z-index: 2000;
    overflow: hidden;
}

.search-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 18px;
    color: #777;
    font-size: 11px;
}

.search-loading i {
    color: #38b04c;
}

.search-result-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border: 0;
    border-bottom: 1px solid #f1f3f1;
    background: #fff;
    text-align: left;
    cursor: pointer;
    transition: .2s ease;
}

.search-result-item:hover {
    background: #f6faf7;
}

.search-result-image {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    overflow: hidden;
    background: #f8faf8;
}

.search-result-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 4px;
}

.search-no-image {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    color: #aaa;
    font-size: 15px;
}

.search-result-info {
    display: flex;
    flex-direction: column;
    gap: 3px;
    min-width: 0;
    flex: 1;
}

.search-result-info strong {
    overflow: hidden;
    color: #222;
    font-size: 11px;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.search-result-info span {
    overflow: hidden;
    color: #38b04c;
    font-size: 9px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.search-result-price {
    color: #38b04c !important;
    font-size: 9px !important;
}

.search-result-item>i {
    color: #aaa;
    font-size: 9px;
}

.search-all-button {
    width: 100%;
    padding: 12px;
    border: 0;
    background: #38b04c;
    color: #fff;
    font-size: 10px;
    cursor: pointer;
}

.search-all-button:hover {
    background: #2f983f;
}

.search-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 18px;
    color: #888;
    font-size: 10px;
}

.search-empty i {
    color: #38b04c;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-left: auto;
}

.header-action {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    text-decoration: none;
    color: #333;
    font-size: 12px;
    font-weight: 400;
    white-space: nowrap;
    transition: color .2s ease;
}

.header-action i {
    font-size: 16px;
}

.header-action:hover {
    color: #38b04c;
}

.icon-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.action-badge {
    position: absolute;
    top: -8px;
    right: -10px;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    border-radius: 20px;
    background: #38b04c;
    color: #fff;
    font-size: 9px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}

.account-menu {
    display: flex;
    align-items: center;
    gap: 5px;
}

.logout-button {
    width: 27px;
    height: 27px;
    border: 0;
    background: transparent;
    color: #777;
    font-size: 13px;
    cursor: pointer;
    border-radius: 5px;
    transition: all .2s ease;
}

.logout-button:hover {
    background: #f4f4f4;
    color: #d9534f;
}

.main-navigation {
    border-top: 1px solid #f1f1f1;
    background: #fff;
}

.navigation-container {
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.nav-link {
    height: 100%;
    padding: 0 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-decoration: none;
    color: #555;
    font-size: 12px;
    font-weight: 400;
    position: relative;
    transition: all .2s ease;
    flex: 1;
}

.nav-link i {
    font-size: 12px;
}

.nav-link::after {
    content: "";
    position: absolute;
    height: 2px;
    width: 0;
    left: 50%;
    bottom: 0;
    background: #38b04c;
    transform: translateX(-50%);
    transition: width .2s ease;
}

.nav-link:hover {
    color: #38b04c;
}

.nav-link:hover::after,
.router-link-active::after {
    width: 65%;
}

.router-link-active {
    color: #38b04c;
}

.promotion-link {
    color: #e79b16;
}

.promotion-link:hover {
    color: #d88c08;
}

.promotion-link::after {
    background: #e79b16;
}

@media(max-width:1100px) {
    .header-container {
        gap: 18px;
    }

    .header-actions {
        gap: 14px;
    }

    .header-action span {
        display: none;
    }

    .navigation-container {
        gap: 12px;
    }

    .nav-link {
        padding: 0 8px;
    }
}

@media(max-width:768px) {
    .site-header {
        position: relative;
    }

    .header-container {
        min-height: 68px;
        padding: 9px 15px;
        gap: 12px;
        flex-wrap: wrap;
    }

    .logo {
        width: 100px;
        max-height: 43px;
    }

    .search-container {
        order: 3;
        flex-basis: 100%;
        max-width: none;
    }

    .search-box {
        height: 36px;
    }

    .search-results {
        top: calc(100% + 5px);
    }

    .header-actions {
        gap: 12px;
    }

    .header-action i {
        font-size: 16px;
    }

    .navigation-container {
        height: auto;
        padding: 8px 10px;
        justify-content: flex-start;
        overflow-x: auto;
        scrollbar-width: none;
    }

    .navigation-container::-webkit-scrollbar {
        display: none;
    }

    .nav-link {
        height: 34px;
        padding: 0 11px;
        font-size: 11px;
        flex-shrink: 0;
        border: 1px solid #eee;
        border-radius: 4px;
    }

    .nav-link::after {
        display: none;
    }

    .nav-link i {
        font-size: 11px;
    }
}

@media(max-width:480px) {
    .header-container {
        gap: 8px;
    }

    .logo {
        width: 90px;
    }

    .header-actions {
        gap: 9px;
    }

    .header-action i {
        font-size: 15px;
    }

    .logout-button {
        display: none;
    }

    .search-box {
        height: 35px;
    }

    .search-results {
        max-height: 400px;
        overflow-y: auto;
    }

    .search-result-item {
        padding: 9px 10px;
    }

    .search-result-image {
        width: 42px;
        height: 42px;
    }
}
</style>