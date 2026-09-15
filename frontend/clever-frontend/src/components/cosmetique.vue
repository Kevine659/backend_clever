<script setup>
import { ref, computed, onMounted } from "vue"
import { RouterLink } from "vue-router"
import api from "../services/api"
const products = ref([])
const loading = ref(true)
const error = ref(false)
const cart = ref([])
const showCart = ref(false)
const favoriteIds = ref([])
const favoriteCounts = ref({})
const favoritesLoading = ref(false)
const favoriteProcessing = ref(null)
const isAuthenticated = computed(() => {
    return !!localStorage.getItem("token")
})
const favoritesCount = computed(() => {
    return favoriteIds.value.length
})
// Identifiant du visiteur
const getGuestId = () => {
    let guestId = localStorage.getItem("guest_id")
    if (!guestId) {
        if (window.crypto && window.crypto.randomUUID) {
            guestId = window.crypto.randomUUID()
        } else {
            guestId = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(c) {
                const r = Math.random() * 16 | 0
                const v = c === "x" ? r : (r & 0x3 | 0x8)
                return v.toString(16)
            })
        }
        localStorage.setItem("guest_id",guestId)
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
// Image du produit
const getProductImage = (image) => {
    if (!image || typeof image !== "string") return null
    image = image.trim()
    if (!image) return null
    if (image.startsWith("http://") || image.startsWith("https://")) {
        return image
    }
    if (image.startsWith("data:image")) {
        return image
    }
    const baseURL = api.defaults.baseURL || "https://backend-clever.onrender.com/api"
    const serverURL = baseURL.replace(/\/api\/?$/,"").replace(/\/$/,"")
    return `${serverURL}${image.startsWith("/") ? image : `/${image}`}`
}
// Prix du produit
const formatPrice = (price) => {
    if (price === null || price === undefined || price === "") {
        return "0 FCFA"
    }
    const number = Number(price)
    if (Number.isNaN(number)) {
        return "0 FCFA"
    }
    return new Intl.NumberFormat("fr-FR",{
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(number) + " FCFA"
}
const getProductPrice = (product) => {
    if (!product) return 0
    const price = product.current_price ?? product.promotional_price ?? product.price ?? 0
    return Number(price) || 0
}
// Compteur des favoris
const getFavoriteCount = (product) => {
    if (!product) return 0
    const productId = String(product.id)
    if (favoriteCounts.value[productId] !== undefined) {
        return Number(favoriteCounts.value[productId]) || 0
    }
    const possibleCount = product.favorite_count ?? product.favorites_count ?? product.favoriteCount ?? product.favoritesCount ?? product.total_favorites ?? product.totalFavorites ?? 0
    const count = Number(possibleCount)
    return Number.isFinite(count) && count >= 0 ? count : 0
}
const setFavoriteCount = (product,count) => {
    if (!product || !product.id) return
    const productId = String(product.id)
    const value = Math.max(0,Number(count) || 0)
    favoriteCounts.value = {
        ...favoriteCounts.value,
        [productId]: value
    }
    product.favorite_count = value
}
// Sauvegarde des favoris invité
const saveGuestFavorites = () => {
    if (isAuthenticated.value) return
    try {
        localStorage.setItem("shop_favorites",JSON.stringify(favoriteIds.value))
    } catch (err) {
        console.error("Erreur sauvegarde favoris :",err)
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
        favoriteIds.value = [...new Set(parsed.map(id => Number(id)).filter(id => Number.isFinite(id) && id > 0))]
    } catch (err) {
        console.error("Erreur chargement favoris :",err)
        favoriteIds.value = []
    }
}
// Extraction de l'identifiant du produit favori
const extractFavoriteProductId = (item) => {
    if (!item) return 0
    if (typeof item === "number") {
        return Number(item)
    }
    if (typeof item === "string") {
        const number = Number(item)
        return Number.isFinite(number) ? number : 0
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
    if (item.product) {
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
// Chargement des favoris
const loadFavorites = async () => {
    try {
        favoritesLoading.value = true
        if (!isAuthenticated.value) {
            loadGuestFavorites()
        } else {
            const response = await api.get("/favorites/",{
                headers: getFavoriteHeaders()
            })
            console.log("Réponse favoris Django :",response.data)
            const data = response.data?.results || response.data || []
            if (Array.isArray(data)) {
                const ids = data.map(extractFavoriteProductId).filter(id => Number.isFinite(id) && id > 0)
                favoriteIds.value = [...new Set(ids)]
            } else {
                favoriteIds.value = []
            }
        }
        const countsResponse = await api.get("/favorites/counts/",{
            headers: getFavoriteHeaders()
        })
        console.log("Compteurs favoris Django :",countsResponse.data)
        if (countsResponse.data && typeof countsResponse.data === "object" && !Array.isArray(countsResponse.data)) {
            favoriteCounts.value = {...countsResponse.data}
        }
    } catch (err) {
        console.error("Erreur chargement favoris :",err)
        if (!isAuthenticated.value) {
            loadGuestFavorites()
        } else {
            favoriteIds.value = []
        }
    } finally {
        favoritesLoading.value = false
    }
}
const isFavorite = (productId) => {
    const id = Number(productId)
    if (!Number.isFinite(id) || id <= 0) {
        return false
    }
    return favoriteIds.value.includes(id)
}
// Ajouter aux favoris
const addFavorite = async (product) => {
    if (!product || !product.id) return
    const productId = Number(product.id)
    if (!Number.isFinite(productId) || productId <= 0) return
    if (isFavorite(productId)) return
    if (favoriteProcessing.value !== null) return
    try {
        favoriteProcessing.value = productId
        const response = await api.post("/favorites/add/",{
            product: productId
        },{
            headers: getFavoriteHeaders()
        })
        console.log("Ajout favori :",response.data)
        if (!favoriteIds.value.includes(productId)) {
            favoriteIds.value = [...favoriteIds.value,productId]
        }
        if (!isAuthenticated.value) {
            saveGuestFavorites()
        }
        const count = response.data?.favorites_count
        if (count !== undefined) {
            setFavoriteCount(product,count)
        }
    } catch (err) {
        console.error("Erreur ajout favori :",err)
    } finally {
        favoriteProcessing.value = null
    }
}
// Supprimer des favoris
const removeFavorite = async (product) => {
    if (!product || !product.id) return
    const productId = Number(product.id)
    if (!Number.isFinite(productId) || productId <= 0) return
    if (!isFavorite(productId)) return
    if (favoriteProcessing.value !== null) return
    try {
        favoriteProcessing.value = productId
        const response = await api.delete(`/favorites/${productId}/remove/`,{
            headers: getFavoriteHeaders()
        })
        console.log("Suppression favori :",response.data)
        favoriteIds.value = favoriteIds.value.filter(id => Number(id) !== productId)
        if (!isAuthenticated.value) {
            saveGuestFavorites()
        }
        const count = response.data?.favorites_count
        if (count !== undefined) {
            setFavoriteCount(product,count)
        }
    } catch (err) {
        console.error("Erreur suppression favori :",err)
    } finally {
        favoriteProcessing.value = null
    }
}
const toggleFavorite = async (product) => {
    if (!product || !product.id) return
    if (favoriteProcessing.value !== null) return
    if (isFavorite(product.id)) {
        await removeFavorite(product)
    } else {
        await addFavorite(product)
    }
}
// Vérification de la catégorie
const isCosmetique = (product) => {
    if (!product) return false
    const normalize = (value) => {
        if (value === null || value === undefined) return ""
        return String(value)
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g,"")
            .trim()
            .toLowerCase()
    }
    const categoryValues = [
        product.category_name,
        product.category,
        product.category_title,
        product.category_label,
        product.subcategory_category_name,
        product.subcategory_category,
        product.subcategory?.category_name,
        product.subcategory?.category?.name,
        product.subcategory?.category?.title
    ]
    return categoryValues.some(value => {
        if (typeof value === "object" && value !== null) {
            return [
                value.name,
                value.title,
                value.label,
                value.slug
            ].some(item => {
                const normalized = normalize(item)
                return normalized === "cosmetique" || normalized === "cosmetiques"
            })
        }
        const normalized = normalize(value)
        return normalized === "cosmetique" || normalized === "cosmetiques"
    })
}
// Chargement uniquement des produits cosmétiques
const loadProducts = async () => {
    try {
        loading.value = true
        error.value = false
        const response = await api.get("/products/")
        console.log("Réponse produits Django :",response.data)
        const data = response.data?.results || response.data || []
        if (!Array.isArray(data)) {
            products.value = []
            return
        }
        products.value = data
            .filter(product => product && product.is_active !== false)
            .filter(product => isCosmetique(product))
            .map(product => {
                const count = favoriteCounts.value[String(product.id)]
                return {
                    ...product,
                    favorite_count: count !== undefined
                        ? Number(count) || 0
                        : Number(product.favorite_count || product.favorites_count || 0) || 0
                }
            })
        console.log("Produits cosmétiques :",products.value)
    } catch (err) {
        console.error("Erreur chargement produits cosmétiques :",err)
        error.value = true
        products.value = []
    } finally {
        loading.value = false
    }
}
// Panier
const getProductCartKey = (item) => {
    if (!item) return null
    const productId = Number(item.product_id || item.product || item.id)
    if (!productId || Number.isNaN(productId)) return null
    return `product_${productId}`
}
const getRangeCartKey = (item) => {
    if (!item) return null
    const rangeId = Number(item.range_id || item.product_range_id || item.product_range)
    if (!rangeId || Number.isNaN(rangeId)) return null
    return `range_${rangeId}`
}
const normalizeCartItem = (item) => {
    if (!item) return null
    if (item.type === "range" || item.item_type === "range" || item.range_id !== undefined || item.product_range_id !== undefined || item.product_range !== undefined) {
        const rangeId = Number(item.range_id || item.product_range_id || item.product_range || item.id)
        if (!rangeId || Number.isNaN(rangeId)) return null
        return {
            type: "range",
            item_type: "range",
            range_id: rangeId,
            product_range: rangeId,
            id: `range_${rangeId}`,
            name: item.name || item.product_range_name || "Gamme",
            slug: item.slug || "",
            image: item.image || item.range_image || item.product_range_image || null,
            price: Number(item.price ?? item.unit_price ?? item.current_price ?? item.promotional_price ?? 0) || 0,
            stock: 0,
            quantity: Number(item.quantity || 1)
        }
    }
    if (item.type === "product" || item.item_type === "product" || item.product_id !== undefined || item.product !== undefined) {
        const productId = Number(item.product_id || item.product || item.id)
        if (!productId || Number.isNaN(productId)) return null
        return {
            type: "product",
            item_type: "product",
            product_id: productId,
            product: productId,
            id: `product_${productId}`,
            name: item.name || item.product_name || "Produit",
            slug: item.slug || "",
            image: item.image || item.product_image || item.main_image || null,
            price: Number(item.price ?? item.unit_price ?? item.current_price ?? item.promotional_price ?? 0) || 0,
            stock: Number(item.stock || 0),
            quantity: Number(item.quantity || 1)
        }
    }
    return null
}
const saveCart = () => {
    try {
        localStorage.setItem("shop_cart",JSON.stringify(cart.value))
    } catch (err) {
        console.error("Erreur sauvegarde panier :",err)
    }
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
        cart.value = parsedCart.map(normalizeCartItem).filter(Boolean)
        saveCart()
    } catch (err) {
        console.error("Erreur chargement panier :",err)
        cart.value = []
    }
}
const addToCart = (product) => {
    if (!product || !product.id) return
    const productId = Number(product.id)
    if (!productId || Number.isNaN(productId)) return
    if (Number(product.stock) <= 0) return
    const existingProduct = cart.value.find(item => item.type === "product" && Number(item.product_id) === productId)
    if (existingProduct) {
        if (Number(existingProduct.quantity) < Number(product.stock)) {
            existingProduct.quantity = Number(existingProduct.quantity || 0) + 1
        }
    } else {
        cart.value.push({
            type: "product",
            item_type: "product",
            product_id: productId,
            product: productId,
            id: `product_${productId}`,
            name: product.name || "Produit",
            slug: product.slug || "",
            image: product.main_image ? getProductImage(product.main_image) : null,
            price: getProductPrice(product),
            quantity: 1,
            stock: Number(product.stock) || 0
        })
    }
    saveCart()
    showCart.value = true
}
const increaseCartQuantity = (item) => {
    if (!item) return
    if (item.type === "product") {
        const stock = Number(item.stock || 0)
        if (stock > 0 && Number(item.quantity) >= stock) return
    }
    item.quantity = Number(item.quantity || 0) + 1
    saveCart()
}
const decreaseCartQuantity = (item) => {
    if (!item) return
    const quantity = Number(item.quantity || 0)
    if (quantity <= 1) return
    item.quantity = quantity - 1
    saveCart()
}
const removeFromCart = (item) => {
    if (!item) return
    const key = item.type === "range" ? getRangeCartKey(item) : getProductCartKey(item)
    if (!key) return
    cart.value = cart.value.filter(current => {
        const currentKey = current.type === "range" ? getRangeCartKey(current) : getProductCartKey(current)
        return currentKey !== key
    })
    saveCart()
}
const clearCart = () => {
    cart.value = []
    saveCart()
}
const cartItemsCount = computed(() => {
    return cart.value.reduce((total,item) => {
        return total + Number(item.quantity || 0)
    },0)
})
const cartTotal = computed(() => {
    return cart.value.reduce((total,item) => {
        return total + Number(item.price || 0) * Number(item.quantity || 0)
    },0)
})
const getItemTotal = (item) => {
    return Number(item.price || 0) * Number(item.quantity || 0)
}
const closeCart = () => {
    showCart.value = false
}
onMounted(async () => {
    await loadFavorites()
    await Promise.all([
        loadProducts(),
        loadCart()
    ])
})
</script>

<template>
    <section class="products-section">
        <div class="container">
            <div class="products-header">
                <div class="products-title-block">
                    <span class="products-small-title">
                        <i class="fa-solid fa-box-open"></i>
                        Découvrez
                    </span>
                    <h2>
                        Nos differents produits
                        <span>cosmétiques</span>
                    </h2>
                </div>
                <div class="header-actions">
                    <RouterLink to="/favoris" class="header-favorite-button">
                        <i class="fa-regular fa-heart"></i>
                        <span>Favoris</span>
                        <strong v-if="favoritesCount > 0" class="favorite-header-count">
                            {{ favoritesCount }}
                        </strong>
                    </RouterLink>
                    <button type="button" class="header-cart-button" @click="showCart = true">
                        <i class="fa-solid fa-cart-shopping"></i>
                        <span>Panier</span>
                        <strong v-if="cartItemsCount > 0" class="cart-count">
                            {{ cartItemsCount }}
                        </strong>
                    </button>
                    <RouterLink to="/boutique?category=cosmetiques" class="view-all-button">
                        Voir tous les cosmétiques
                        <i class="fa-solid fa-arrow-right"></i>
                    </RouterLink>
                </div>
            </div>
            <div v-if="loading" class="products-grid">
                <div v-for="n in 4" :key="n" class="product-card skeleton-card">
                    <div class="skeleton-image"></div>
                    <div class="skeleton-content">
                        <div class="skeleton-line category"></div>
                        <div class="skeleton-line title"></div>
                        <div class="skeleton-line rating"></div>
                        <div class="skeleton-line price"></div>
                    </div>
                </div>
            </div>
            <div v-else-if="error" class="products-message">
                <i class="fa-solid fa-circle-exclamation"></i>
                <p>Impossible de charger les produits cosmétiques.</p>
                <button type="button" @click="loadProducts">
                    Réessayer
                </button>
            </div>
            <div v-else-if="products.length > 0" class="products-grid">
                <article v-for="product in products" :key="product.id" class="product-card">
                    <div class="product-image-container">
                        <RouterLink :to="{path:'/produit',query:{slug:product.slug}}" class="product-image-link">
                            <img v-if="product.main_image" :src="getProductImage(product.main_image)" :alt="product.name" class="product-image" />
                            <div v-else class="no-product-image">
                                <i class="fa-solid fa-image"></i>
                                <span>Image indisponible</span>
                            </div>
                        </RouterLink>
                        <RouterLink :to="{path:'/produit',query:{slug:product.slug}}" class="view-details-button">
                            <i class="fa-solid fa-eye"></i>
                            <span>Voir les détails</span>
                        </RouterLink>
                        <span v-if="product.is_on_sale" class="sale-badge">
                            PROMO
                        </span>
                        <button type="button" class="favorite-button" :class="{active:isFavorite(product.id)}" :title="isFavorite(product.id) ? 'Retirer des favoris' : 'Ajouter aux favoris'" :disabled="favoritesLoading" @click.stop="toggleFavorite(product)">
                            <i :class="isFavorite(product.id) ? 'fa-solid fa-heart' : 'fa-regular fa-heart'"></i>
                        </button>
                        <div class="favorite-counter">
                            <i class="fa-solid fa-heart"></i>
                            <span>{{ getFavoriteCount(product) }}</span>
                        </div>
                        <span v-if="Number(product.stock) <= 0" class="out-of-stock">
                            Rupture de stock
                        </span>
                    </div>
                    <div class="product-info">
                        <span v-if="product.subcategory_name" class="product-category">
                            {{ product.subcategory_name }}
                        </span>
                        <h3 class="product-name">
                            <RouterLink :to="{path:'/produit',query:{slug:product.slug}}">
                                {{ product.name }}
                            </RouterLink>
                        </h3>
                        <div class="product-rating">
                            <i class="fa-solid fa-star"></i>
                            <i class="fa-solid fa-star"></i>
                            <i class="fa-solid fa-star"></i>
                            <i class="fa-solid fa-star"></i>
                            <i class="fa-regular fa-star"></i>
                        </div>
                        <div class="product-bottom">
                            <div class="product-prices">
                                <template v-if="product.is_on_sale">
                                    <strong class="current-price sale-price">
                                        {{ formatPrice(product.current_price ?? product.promotional_price ?? product.price) }}
                                    </strong>
                                    <span class="old-price">
                                        {{ formatPrice(product.price) }}
                                    </span>
                                </template>
                                <strong v-else class="current-price">
                                    {{ formatPrice(product.price) }}
                                </strong>
                            </div>
                            <button type="button" class="add-to-cart-button" :disabled="Number(product.stock) <= 0" title="Ajouter au panier" @click="addToCart(product)">
                                <i class="fa-solid fa-cart-shopping"></i>
                                <span>Ajouter au panier</span>
                            </button>
                        </div>
                    </div>
                </article>
            </div>
            <div v-else class="products-message">
                <i class="fa-solid fa-box-open"></i>
                <p>Aucun produit cosmétique disponible pour le moment.</p>
            </div>
        </div>
    </section>
    <Transition name="cart-fade">
        <div v-if="showCart" class="cart-overlay" @click.self="closeCart">
            <Transition name="cart-slide">
                <aside v-if="showCart" class="cart-panel">
                    <div class="cart-header">
                        <div class="cart-header-title">
                            <div class="cart-icon">
                                <i class="fa-solid fa-cart-shopping"></i>
                            </div>
                            <div>
                                <h3>Mon panier</h3>
                                <span>
                                    {{ cartItemsCount }}
                                    {{ cartItemsCount > 1 ? "articles" : "article" }}
                                </span>
                            </div>
                        </div>
                        <button type="button" class="cart-close-button" @click="closeCart">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                    <div v-if="cart.length === 0" class="empty-cart">
                        <div class="empty-cart-icon">
                            <i class="fa-solid fa-cart-shopping"></i>
                        </div>
                        <h3>Votre panier est vide</h3>
                        <p>
                            Ajoutez vos produits préférés pour les retrouver ici.
                        </p>
                        <button type="button" class="continue-shopping-button" @click="closeCart">
                            <i class="fa-solid fa-arrow-left"></i>
                            Continuer mes achats
                        </button>
                    </div>
                    <template v-else>
                        <div class="cart-content">
                            <div class="cart-products">
                                <div v-for="item in cart" :key="item.id" class="cart-item">
                                    <div class="cart-item-image">
                                        <img v-if="item.image" :src="getProductImage(item.image)" :alt="item.name" @error="$event.target.style.display='none'" />
                                        <div v-else class="cart-no-image">
                                            <i class="fa-solid fa-image"></i>
                                        </div>
                                    </div>
                                    <div class="cart-item-info">
                                        <span class="cart-item-type">
                                            {{ item.type === "range" ? "GAMME" : "PRODUIT" }}
                                        </span>
                                        <h4>{{ item.name }}</h4>
                                        <strong class="cart-item-price">
                                            {{ formatPrice(item.price) }}
                                        </strong>
                                        <div class="cart-item-bottom">
                                            <div class="cart-quantity">
                                                <button type="button" @click="decreaseCartQuantity(item)" :disabled="item.quantity <= 1">
                                                    <i class="fa-solid fa-minus"></i>
                                                </button>
                                                <span>{{ item.quantity }}</span>
                                                <button type="button" @click="increaseCartQuantity(item)" :disabled="item.type === 'product' && item.stock > 0 && item.quantity >= item.stock">
                                                    <i class="fa-solid fa-plus"></i>
                                                </button>
                                            </div>
                                            <strong class="cart-item-total">
                                                {{ formatPrice(getItemTotal(item)) }}
                                            </strong>
                                        </div>
                                    </div>
                                    <button type="button" class="remove-cart-item" title="Supprimer" @click="removeFromCart(item)">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="cart-footer">
                            <div class="cart-summary">
                                <div class="summary-line">
                                    <span>Sous-total</span>
                                    <strong>{{ formatPrice(cartTotal) }}</strong>
                                </div>
                                <div class="summary-line">
                                    <span>Livraison</span>
                                    <span class="delivery-free">
                                        À confirmer
                                    </span>
                                </div>
                                <div class="summary-total">
                                    <span>Total</span>
                                    <strong>{{ formatPrice(cartTotal) }}</strong>
                                </div>
                            </div>
                            <RouterLink to="/panier" class="checkout-button" @click="closeCart">
                                <i class="fa-solid fa-cart-shopping"></i>
                                Voir mon panier
                            </RouterLink>
                            <button type="button" class="continue-button" @click="closeCart">
                                Continuer mes achats
                            </button>
                            <button type="button" class="clear-cart-button" @click="clearCart">
                                <i class="fa-solid fa-trash-can"></i>
                                Vider le panier
                            </button>
                        </div>
                    </template>
                </aside>
            </Transition>
        </div>
    </Transition>
</template>

<style scoped>
.products-section{width:100%;padding:50px 0 65px;background:#fff}
.products-header{width:100%;display:flex;align-items:flex-end;justify-content:space-between;gap:25px;margin-bottom:25px}
.products-title-block{display:flex;flex-direction:column;align-items:flex-start}
.products-small-title{display:flex;align-items:center;gap:7px;margin-bottom:7px;color:#38B04C;font-size:10px;font-weight:600;letter-spacing:1.6px;text-transform:uppercase}
.products-small-title i{font-size:10px}
.products-header h2{margin:0;color:#202020;font-family:Georgia,"Times New Roman",serif;font-size:34px;font-weight:500;line-height:1.1}
.products-header h2 span{color:#38B04C}
.header-actions{display:flex;align-items:center;gap:10px}
.header-cart-button,.header-favorite-button{position:relative;height:38px;display:inline-flex;align-items:center;justify-content:center;gap:7px;padding:0 14px;border:1px solid #dfe8e1;border-radius:20px;background:#fff;color:#333;font-size:10px;font-weight:600;cursor:pointer;transition:.25s ease;text-decoration:none}
.header-cart-button:hover,.header-favorite-button:hover{background:#38B04C;border-color:#38B04C;color:#fff}
.header-cart-button i,.header-favorite-button i{font-size:11px}
.cart-count,.favorite-header-count{min-width:18px;height:18px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#38B04C;color:#fff;font-size:8px}
.header-cart-button:hover .cart-count,.header-favorite-button:hover .favorite-header-count{background:#fff;color:#38B04C}
.view-all-button{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:8px 15px;border:1px solid #e0e6e1;border-radius:20px;background:#fff;color:#333;font-size:10px;font-weight:500;text-decoration:none;transition:.25s ease}
.view-all-button:hover{border-color:#38B04C;background:#38B04C;color:#fff;transform:translateY(-2px)}
.view-all-button i{font-size:8px}
.products-grid{width:100%;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.product-card{width:100%;overflow:hidden;border:1px solid #eee;border-radius:8px;background:#fff;transition:.3s ease}
.product-card:hover{transform:translateY(-4px);border-color:#e4e9e4;box-shadow:0 12px 30px rgba(0,0,0,.07)}
.product-image-container{width:100%;height:220px;position:relative;overflow:hidden;background:#fff}
.product-image-link{width:100%;height:100%;display:flex;align-items:center;justify-content:center;text-decoration:none}
.product-image{width:100%;height:100%;object-fit:contain;padding:12px;transition:transform .45s ease}
.product-card:hover .product-image{transform:scale(1.05)}
.no-product-image{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;color:#aaa;font-size:11px}
.no-product-image i{font-size:24px}
.view-details-button{position:absolute;left:50%;bottom:16px;display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:7px 12px;border:1px solid rgba(255,255,255,.95);border-radius:20px;background:rgba(255,255,255,.97);color:#202020;font-size:9px;font-weight:600;text-decoration:none;opacity:0;visibility:hidden;transform:translate(-50%,12px);z-index:8;transition:.3s ease}
.product-card:hover .view-details-button{opacity:1;visibility:visible;transform:translate(-50%,0)}
.view-details-button:hover{background:#38B04C;border-color:#38B04C;color:#fff}
.sale-badge{position:absolute;top:9px;left:9px;padding:5px 8px;border-radius:3px;background:#38B04C;color:#fff;font-size:8px;font-weight:700;z-index:9}
.favorite-button{position:absolute;top:9px;right:9px;width:30px;height:30px;display:flex;align-items:center;justify-content:center;border:0;border-radius:50%;background:#fff;color:#555;box-shadow:0 3px 10px rgba(0,0,0,.08);cursor:pointer;z-index:11;transition:.25s ease}
.favorite-button:hover{background:#38B04C;color:#fff;transform:scale(1.08)}
.favorite-button.active{background:#38B04C;color:#fff}
.favorite-button:disabled{opacity:.6;cursor:not-allowed}
.favorite-button i{font-size:11px}
.favorite-counter{position:absolute;top:44px;right:12px;display:flex;align-items:center;justify-content:center;gap:4px;min-width:28px;height:18px;padding:0 6px;border-radius:10px;background:#fff;color:#555;box-shadow:0 3px 10px rgba(0,0,0,.08);font-size:8px;font-weight:600;z-index:10}
.favorite-counter i{color:#38B04C;font-size:8px}
.favorite-counter span{font-size:8px}
.out-of-stock{position:absolute;left:9px;bottom:9px;padding:5px 8px;border-radius:3px;background:#202020;color:#fff;font-size:8px;z-index:10}
.product-info{width:100%;padding:11px 13px 12px}
.product-category{display:block;margin-bottom:4px;color:#38B04C;font-size:8px;font-weight:600;text-transform:uppercase}
.product-name{min-height:34px;margin:0 0 6px;overflow:hidden}
.product-name a{display:-webkit-box;overflow:hidden;color:#202020;font-family:Georgia,"Times New Roman",serif;font-size:15px;line-height:1.2;text-decoration:none;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.product-name a:hover{color:#38B04C}
.product-rating{display:flex;gap:2px;margin-bottom:8px}
.product-rating i{color:#38B04C;font-size:8px}
.product-bottom{width:100%;display:flex;align-items:center;justify-content:space-between;gap:8px}
.product-prices{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px}
.current-price{color:#202020;font-size:12px;font-weight:700}
.sale-price{color:#38B04C}
.old-price{color:#999;font-size:8px;text-decoration:line-through}
.add-to-cart-button{height:29px;min-width:29px;display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:0 8px;border:1px solid #dce6dd;border-radius:18px;background:#fff;color:#333;cursor:pointer;flex-shrink:0;transition:.3s ease}
.add-to-cart-button i{font-size:9px}
.add-to-cart-button span{display:none;font-size:8px}
.product-card:hover .add-to-cart-button{min-width:110px;border-color:#38B04C;background:#38B04C;color:#fff}
.product-card:hover .add-to-cart-button span{display:inline}
.add-to-cart-button:hover:not(:disabled){background:#2f963f;border-color:#2f963f}
.add-to-cart-button:disabled{opacity:.4;cursor:not-allowed}
.cart-overlay{position:fixed;inset:0;z-index:9999;display:flex;justify-content:flex-end;background:rgba(0,0,0,.45);backdrop-filter:blur(3px)}
.cart-panel{width:440px;max-width:95%;height:100vh;display:flex;flex-direction:column;background:#fff;box-shadow:-10px 0 40px rgba(0,0,0,.15)}
.cart-header{min-height:82px;display:flex;align-items:center;justify-content:space-between;padding:18px 22px;border-bottom:1px solid #eee}
.cart-header-title{display:flex;align-items:center;gap:12px}
.cart-icon{width:42px;height:42px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#eef8f0;color:#38B04C}
.cart-icon i{font-size:15px}
.cart-header h3{margin:0;color:#202020;font-family:Georgia,"Times New Roman",serif;font-size:21px;font-weight:500}
.cart-header-title span{color:#999;font-size:10px}
.cart-close-button{width:34px;height:34px;display:flex;align-items:center;justify-content:center;border:0;border-radius:50%;background:#f6f6f6;color:#555;cursor:pointer;transition:.25s ease}
.cart-close-button:hover{background:#38B04C;color:#fff}
.cart-content{flex:1;overflow-y:auto;padding:18px}
.cart-products{display:flex;flex-direction:column;gap:12px}
.cart-item{position:relative;display:flex;gap:12px;padding:12px;border:1px solid #eee;border-radius:8px;background:#fff;transition:.25s ease}
.cart-item:hover{border-color:#dce8df;box-shadow:0 5px 15px rgba(0,0,0,.04)}
.cart-item-image{width:82px;height:82px;flex-shrink:0;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:6px;background:#f9faf9}
.cart-item-image img{width:100%;height:100%;object-fit:contain;padding:6px}
.cart-no-image{color:#aaa}
.cart-item-info{flex:1;min-width:0;padding-right:20px}
.cart-item-type{display:block;margin-bottom:3px;color:#38B04C;font-size:8px;font-weight:800;letter-spacing:1.3px}
.cart-item-info h4{margin:2px 0 7px;color:#222;font-family:Georgia,"Times New Roman",serif;font-size:14px;font-weight:600;line-height:1.3}
.cart-item-price{color:#38B04C;font-size:11px}
.cart-item-bottom{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:11px}
.cart-quantity{height:28px;display:flex;align-items:center;border:1px solid #ddd;border-radius:5px;overflow:hidden}
.cart-quantity button{width:27px;height:100%;display:flex;align-items:center;justify-content:center;border:0;background:#fff;color:#555;cursor:pointer}
.cart-quantity button:hover:not(:disabled){background:#38B04C;color:#fff}
.cart-quantity button:disabled{opacity:.35;cursor:not-allowed}
.cart-quantity button i{font-size:8px}
.cart-quantity span{width:30px;text-align:center;color:#333;font-size:10px;font-weight:600}
.cart-item-total{color:#222;font-size:11px}
.remove-cart-item{position:absolute;top:9px;right:9px;border:0;background:transparent;color:#aaa;cursor:pointer;transition:.2s ease}
.remove-cart-item:hover{color:#d9534f}
.remove-cart-item i{font-size:10px}
.cart-footer{padding:18px 20px;border-top:1px solid #eee;background:#fff;box-shadow:0 -5px 20px rgba(0,0,0,.04)}
.summary-line,.summary-total{display:flex;align-items:center;justify-content:space-between}
.summary-line{margin-bottom:9px;color:#777;font-size:11px}
.summary-line strong{color:#333}
.delivery-free{color:#38B04C}
.summary-total{margin-top:12px;padding-top:13px;border-top:1px solid #eee;color:#222;font-size:14px;font-weight:600}
.summary-total strong{color:#38B04C;font-size:17px}
.checkout-button{width:100%;height:43px;display:flex;align-items:center;justify-content:center;gap:8px;margin-top:16px;border-radius:5px;background:#38B04C;color:#fff;font-size:12px;font-weight:600;text-decoration:none;transition:.25s ease}
.checkout-button:hover{background:#2f963f;color:#fff}
.continue-button{width:100%;height:38px;margin-top:8px;border:1px solid #ddd;border-radius:5px;background:#fff;color:#555;font-size:11px;cursor:pointer}
.continue-button:hover{border-color:#38B04C;color:#38B04C}
.clear-cart-button{width:100%;margin-top:12px;border:0;background:transparent;color:#999;font-size:10px;cursor:pointer}
.clear-cart-button:hover{color:#d9534f}
.empty-cart{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;text-align:center}
.empty-cart-icon{width:75px;height:75px;display:flex;align-items:center;justify-content:center;margin-bottom:18px;border-radius:50%;background:#f1f8f3;color:#38B04C}
.empty-cart-icon i{font-size:27px}
.empty-cart h3{margin:0 0 8px;color:#222;font-family:Georgia,"Times New Roman",serif;font-size:21px;font-weight:500}
.empty-cart p{max-width:260px;margin:0;color:#999;font-size:11px;line-height:1.7}
.continue-shopping-button{display:inline-flex;align-items:center;gap:8px;margin-top:20px;padding:10px 16px;border:0;border-radius:5px;background:#38B04C;color:#fff;font-size:11px;cursor:pointer}
.continue-shopping-button:hover{background:#2f963f}
.cart-fade-enter-active,.cart-fade-leave-active{transition:opacity .3s ease}
.cart-fade-enter-from,.cart-fade-leave-to{opacity:0}
.cart-slide-enter-active,.cart-slide-leave-active{transition:transform .35s ease}
.cart-slide-enter-from,.cart-slide-leave-to{transform:translateX(100%)}
.skeleton-card{pointer-events:none}
.skeleton-image{width:100%;height:220px;background:linear-gradient(90deg,#f5f5f5 25%,#fff 50%,#f5f5f5 75%);background-size:200% 100%;animation:skeletonAnimation 1.5s infinite}
.skeleton-content{padding:13px}
.skeleton-line{height:9px;margin-bottom:8px;border-radius:3px;background:linear-gradient(90deg,#f5f5f5 25%,#fff 50%,#f5f5f5 75%);background-size:200% 100%;animation:skeletonAnimation 1.5s infinite}
.skeleton-line.category{width:30%}
.skeleton-line.title{width:75%;height:13px}
.skeleton-line.rating{width:45%}
.skeleton-line.price{width:35%;height:11px}
@keyframes skeletonAnimation{0%{background-position:200% 0}100%{background-position:-200% 0}}
.products-message{width:100%;min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#999}
.products-message i{color:#38B04C;font-size:28px}
.products-message p{margin:0;font-size:12px}
.products-message button{padding:8px 15px;border:0;border-radius:4px;background:#38B04C;color:#fff;font-size:10px;cursor:pointer}
@media(max-width:991px){.products-header{align-items:flex-start;flex-direction:column;gap:14px}.header-actions{width:100%}.products-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.product-image-container,.skeleton-image{height:205px}}
@media(max-width:768px){.products-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.product-image-container,.skeleton-image{height:215px}.cart-panel{width:430px}}
@media(max-width:576px){.products-section{padding:35px 0 45px}.products-header h2{font-size:27px}.header-actions{align-items:stretch;flex-direction:column}.header-cart-button,.header-favorite-button,.view-all-button{width:100%}.products-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.product-image-container,.skeleton-image{height:175px}.product-image{padding:7px}.product-info{padding:9px}.product-name a{font-size:12px}.current-price{font-size:10px}.add-to-cart-button{height:27px;min-width:27px;padding:0 7px}.product-card:hover .add-to-cart-button{min-width:98px}.view-details-button{bottom:10px;padding:6px 10px;font-size:8px}.favorite-counter{top:42px;right:10px}.cart-panel{width:100%;max-width:100%}.cart-header{padding:15px}.cart-content{padding:12px}.cart-footer{padding:15px}.cart-item-image{width:70px;height:70px}}
</style>