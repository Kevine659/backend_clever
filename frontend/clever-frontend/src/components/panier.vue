<script setup>
import { ref, computed, onMounted } from "vue"
import { RouterLink, useRouter } from "vue-router"
import api from "../services/api"
const router = useRouter()
const cart = ref([])
const submitting = ref(false)
const synchronizing = ref(false)
const successMessage = ref("")
const errorMessage = ref("")
const form = ref({
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
    city: "",
    address: ""
})

/* AUTHENTIFICATION*/
const isAuthenticated = computed(() => {
    return !!localStorage.getItem("token")
})

/* IMAGE URL */
const getProductImage = (image) => {
    if (!image || typeof image !== "string") return null
    image = image.trim()
    if (!image) return null
    if (image.startsWith("http://") || image.startsWith("https://")) return image
    if (image.startsWith("data:image")) return image
    const baseURL = api.defaults.baseURL || "http://127.0.0.1:7000/api"
    const serverURL = baseURL.replace(/\/api\/?$/, "").replace(/\/$/, "")
    return `${serverURL}${image.startsWith("/") ? image : `/${image}`}`
}
/* FORMAT PRIX */
const formatPrice = (price) => {
    if (price === null || price === undefined || price === "") return "0 FCFA"
    const number = Number(price)
    if (Number.isNaN(number)) return "0 FCFA"
    return new Intl.NumberFormat("fr-FR", { minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(number) + " FCFA"
}


/* EXTRAIRE IMAGE */
const extractCartImage = (item) => {
    if (!item) return null
    if (item.product_range_image) return item.product_range_image
    if (item.range_image) return item.range_image
    if (item.product_image) return item.product_image
    if (item.main_image) return item.main_image
    if (item.image) return item.image
    if (item.image_url) return item.image_url
    if (item.main_image_url) return item.main_image_url
    const range = item.product_range_data || item.range_data || (typeof item.product_range === "object" ? item.product_range : null)
    if (range && typeof range === "object") {
        if (range.image) return range.image
        if (range.image_url) return range.image_url
        if (range.main_image) return range.main_image
    }
    const product = item.product_data || item.product_detail || (typeof item.product === "object" ? item.product : null)
    if (product && typeof product === "object") {
        if (product.main_image) return product.main_image
        if (product.image) return product.image
        if (product.image_url) return product.image_url
        if (product.main_image_url) return product.main_image_url
    }
    return null
}
/* DETECTER GAMME */
const isRangeItem = (item) => {
    if (!item) return false
    if (item.type === "range") return true
    if (item.item_type === "range") return true
    if (item.range_id !== undefined && item.range_id !== null) return true
    if (item.product_range_id !== undefined && item.product_range_id !== null) return true
    if (item.product_range !== undefined && item.product_range !== null && typeof item.product_range !== "string" || item.product_range !== undefined && item.product_range !== null && typeof item.product_range === "number") return true
    if (item.product_range_data !== undefined && item.product_range_data !== null) return true
    if (item.range_data !== undefined && item.range_data !== null) return true
    return false
}
/* NORMALISER GAMME */
const normalizeRangeItem = (item) => {
    if (!item) return null
    const range = item.product_range_data || item.range_data || (typeof item.product_range === "object" ? item.product_range : null)
    const rawRangeId =
        item.range_id ??
        item.product_range_id ??
        (typeof item.product_range === "number" ? item.product_range : null) ??
        range?.id
    const rangeId = Number(rawRangeId)
    if (!rangeId || Number.isNaN(rangeId)) return null
    const price =
        item.unit_price ??
        item.price ??
        item.current_price ??
        item.promotional_price ??
        range?.current_price ??
        range?.promotional_price ??
        range?.price ??
        0
    return {
        type: "range",
        item_type: "range",
        range_id: rangeId,
        product_range: rangeId,
        id: `range_${rangeId}`,
        name: item.product_range_name || item.name || range?.name || "Gamme",
        slug: item.slug || range?.slug || "",
        price: Number(price || 0),
        stock: 0,
        image: extractCartImage(item),
        quantity: Number(item.quantity || 1)
    }
}
/* NORMALISER PRODUIT */
const normalizeProductItem = (item) => {
    if (!item) return null
    const product = item.product_data || item.product_detail || (typeof item.product === "object" ? item.product : null)
    const rawProductId =
        item.product_id ??
        (typeof item.product === "number" ? item.product : null) ??
        product?.id
    const productId = Number(rawProductId)
    if (!productId || Number.isNaN(productId)) return null
    const price =
        item.unit_price ??
        item.price ??
        item.current_price ??
        item.promotional_price ??
        product?.current_price ??
        product?.promotional_price ??
        product?.price ??
        0
    const stock =
        item.stock ??
        product?.stock ??
        0
    return {
        type: "product",
        item_type: "product",
        product_id: productId,
        product: productId,
        id: `product_${productId}`,
        name: item.product_name || item.name || product?.name || product?.title || "Produit",
        price: Number(price || 0),
        stock: Number(stock || 0),
        image: extractCartImage(item),
        quantity: Number(item.quantity || 1)
    }
}
/* NORMALISER ARTICLE */
const normalizeCartItem = (item) => {
    if (!item) return null
    if (isRangeItem(item)) {
        return normalizeRangeItem(item)
    }
    return normalizeProductItem(item)
}


/* CLE ARTICLE*/
const getCartKey = (item) => {
    if (!item) return null
    if (item.type === "range") {
        return `range_${Number(item.range_id)}`
    }
    return `product_${Number(item.product_id)}`
}


/* CHARGER PANIER LOCAL */
const loadLocalCart = () => {
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
    } catch (error) {
        console.error("Erreur lors du chargement du panier :", error)
        cart.value = []
    }
}
/* SAUVEGARDER PANIER */
const saveCart = () => {
    try {
        localStorage.setItem("shop_cart", JSON.stringify(cart.value))
    } catch (error) {
        console.error("Erreur lors de la sauvegarde du panier :", error)
    }
}
/* CONSTRUIRE PAYLOAD SYNCHRONISATION */
const buildSyncPayload = () => {
    return cart.value
        .filter(item => item && Number(item.quantity) > 0)
        .map(item => {
            if (item.type === "range") {
                return {
                    type: "range",
                    product_range: Number(item.range_id),
                    quantity: Number(item.quantity)
                }
            }
            return {
                type: "product",
                product: Number(item.product_id),
                quantity: Number(item.quantity)
            }
        })
        .filter(item => {
            if (item.type === "range") {
                return Number(item.product_range) > 0
            }
            return Number(item.product) > 0
        })
}
/* METTRE A JOUR DEPUIS DJANGO */
const updateCartFromServer = (serverCart) => {
    if (!serverCart) {
        return
    }
    const serverItems = Array.isArray(serverCart.items) ? serverCart.items : []
    const localItems = [...cart.value]
    const normalizedServerItems = serverItems.map(normalizeCartItem).filter(Boolean)
    const merged = []
    const keys = new Set()
    for (const serverItem of normalizedServerItems) {
        const key = getCartKey(serverItem)
        if (!key || keys.has(key)) continue
        const localItem = localItems.find(item => getCartKey(item) === key)
        if (!serverItem.image && localItem?.image) {
            serverItem.image = localItem.image
        }
        if (
            (!serverItem.name || serverItem.name === "Produit" || serverItem.name === "Gamme") &&
            localItem?.name
        ) {
            serverItem.name = localItem.name
        }
        if (!serverItem.price && localItem?.price) {
            serverItem.price = localItem.price
        }
        if (!serverItem.slug && localItem?.slug) {
            serverItem.slug = localItem.slug
        }
        if (serverItem.type === "product" && !serverItem.stock && localItem?.stock) {
            serverItem.stock = localItem.stock
        }
        if (!serverItem.quantity && localItem?.quantity) {
            serverItem.quantity = localItem.quantity
        }
        keys.add(key)
        merged.push(serverItem)
    }
    for (const localItem of localItems) {
        const key = getCartKey(localItem)
        if (!key || keys.has(key)) continue
        merged.push(localItem)
        keys.add(key)
    }
    cart.value = merged
    saveCart()
}

/*  SYNCHRONISER PRODUITS ET GAMME */
const syncCartWithServer = async () => {
    if (!isAuthenticated.value) return null
    if (synchronizing.value) return null
    const items = buildSyncPayload()
    console.log("Articles envoyés à Django :", items)
    if (items.length === 0) {
        console.warn("Aucun article valide à synchroniser.")
        return null
    }
    synchronizing.value = true
    try {
        const response = await api.post("/cart/sync/", { items })
        console.log("Réponse synchronisation :", response.data)
        if (response.data?.cart) {
            updateCartFromServer(response.data.cart)
        }
        return response.data
    } catch (error) {
        console.error("Erreur synchronisation panier :", error)
        console.error("Payload envoyé :", { items })
        console.error("Réponse Django :", error.response?.data)
        console.error("Status Django :", error.response?.status)
        throw error
    } finally {
        synchronizing.value = false
    }
}


/* NOMBRE ARTICLE */
const cartItemsCount = computed(() => {
    return cart.value.reduce(
        (total, item) => total + Number(item.quantity || 0),
        0
    )
})


/* TOTAL */
const cartTotal = computed(() => {
    return cart.value.reduce(
        (total, item) => total + Number(item.price || 0) * Number(item.quantity || 0),
        0
    )
})


/* TOTAL LIGNE */
const getItemTotal = (item) => {
    return Number(item.price || 0) * Number(item.quantity || 0)
}

/* AUGMENTER */
const increaseQuantity = async (item) => {
    if (!item) return
    const quantity = Number(item.quantity || 0)
    const stock = Number(item.stock || 0)
    if (item.type === "product" && stock > 0 && quantity >= stock) return
    const oldQuantity = quantity
    item.quantity = quantity + 1
    saveCart()
    if (!isAuthenticated.value) return
    try {
        await syncCartWithServer()
    } catch (error) {
        item.quantity = oldQuantity
        saveCart()
    }
}

/* DIMINUER */
const decreaseQuantity = async (item) => {
    if (!item) return
    const quantity = Number(item.quantity || 0)
    if (quantity <= 1) return
    const oldQuantity = quantity
    item.quantity = quantity - 1
    saveCart()
    if (!isAuthenticated.value) return
    try {
        await syncCartWithServer()
    } catch (error) {
        item.quantity = oldQuantity
        saveCart()
    }
}

/* SUPPRIMER */
const removeItem = async (item) => {
    if (!item) return
    const oldCart = [...cart.value]
    const key = getCartKey(item)
    cart.value = cart.value.filter(product => getCartKey(product) !== key)
    saveCart()
    if (!isAuthenticated.value) return
    try {
        if (cart.value.length === 0) {
            await api.post("/cart/clear/")
        } else {
            await syncCartWithServer()
        }
    } catch (error) {
        cart.value = oldCart
        saveCart()
    }
}


/* VIDER */
const clearCart = async () => {
    const oldCart = [...cart.value]
    cart.value = []
    saveCart()
    if (!isAuthenticated.value) return
    try {
        await api.post("/cart/clear/")
    } catch (error) {
        console.error("Erreur lors du vidage du panier :", error)
        cart.value = oldCart
        saveCart()
    }
}

/* RESET FORMULAIRE */
const resetForm = () => {
    form.value = {
        first_name: "",
        last_name: "",
        phone: "",
        email: "",
        city: "",
        address: ""
    }
}


/* VALIDATION */
const validateForm = () => {
    errorMessage.value = ""
    if (!form.value.first_name.trim()) {
        errorMessage.value = "Veuillez renseigner votre prénom."
        return false
    }
    if (!form.value.last_name.trim()) {
        errorMessage.value = "Veuillez renseigner votre nom."
        return false
    }
    if (!form.value.phone.trim()) {
        errorMessage.value = "Veuillez renseigner votre numéro de téléphone."
        return false
    }
    if (!form.value.email.trim()) {
        errorMessage.value = "Veuillez renseigner votre adresse e-mail."
        return false
    }
    if (!form.value.city.trim()) {
        errorMessage.value = "Veuillez renseigner votre ville."
        return false
    }
    if (!form.value.address.trim()) {
        errorMessage.value = "Veuillez renseigner votre quartier ou adresse."
        return false
    }
    return true
}
/*  WHATSAPP */
const openCommercialWhatsApp = (commercial, order) => {
    if (!commercial?.whatsapp_number) {
        errorMessage.value = "La commande a été enregistrée, mais le numéro WhatsApp du commercial est introuvable."
        return
    }
    let whatsappNumber = String(commercial.whatsapp_number).replace(/\D/g, "")
    if (whatsappNumber.startsWith("0")) {
        whatsappNumber = "237" + whatsappNumber.substring(1)
    }
    if (!whatsappNumber.startsWith("237") && whatsappNumber.length === 9) {
        whatsappNumber = "237" + whatsappNumber
    }
    const orderItems = Array.isArray(order?.items) ? order.items : []
    let itemsMessage = ""
    orderItems.forEach((item, index) => {
        const type = item.product_range ? "GAMME" : "PRODUIT"
        itemsMessage += `${index + 1}. ${type} : ${item.product_name} x ${item.quantity}\n`
        itemsMessage += `   Prix unitaire : ${formatPrice(item.price)}\n`
        itemsMessage += `   Sous-total : ${formatPrice(item.subtotal)}\n\n`
    })
    const message =
        `Commande effectuée sur la boutique Clever.\n\n` +
        `*COMMANDE #${order.id}*\n\n` +
        `*Informations client*\n` +
        `Nom : ${order.first_name} ${order.last_name}\n` +
        `Téléphone : ${order.phone}\n` +
        `Email : ${order.email}\n` +
        `Ville : ${order.city}\n` +
        `Adresse : ${order.address}\n\n` +
        `*Articles commandés*\n` +
        itemsMessage +
        `*TOTAL : ${formatPrice(order.total_amount)}*\n\n` 

    window.location.href = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`
}


/*  PASSER COMMANDE */
const submitOrder = async () => {
    errorMessage.value = ""
    successMessage.value = ""

    if (cart.value.length === 0) {
        errorMessage.value = "Votre panier est vide. Ajoutez au moins un article avant de passer votre commande."
        return
    }
    if (!validateForm()) return
    if (submitting.value || synchronizing.value) return
    submitting.value = true
    try {
        const payload = buildSyncPayload()
        console.log("Panier complet avant commande :", cart.value)
        console.log("Payload complet envoyé à Django :", payload)
        if (payload.length === 0) {
            errorMessage.value = "Aucun article valide n'a été trouvé dans votre panier."
            return
        }
        await syncCartWithServer()
        if (isAuthenticated.value) {
            await syncCartWithServer()

            if (cart.value.length === 0) {
                errorMessage.value = "Votre panier est vide après synchronisation."
                return
            }
        }
        const orderData = {
            first_name: form.value.first_name.trim(),
            last_name: form.value.last_name.trim(),
            phone: form.value.phone.trim(),
            email: form.value.email.trim(),
            city: form.value.city.trim(),
            address: form.value.address.trim(),
            items: payload
        }
        console.log("Données envoyées à /api/orders/ :", orderData)
        const response = await api.post("/orders/", orderData)
        console.log("Commande créée :", response.data)
        const commercial = response.data?.commercial
        const order = response.data?.order
        if (!commercial || !order) {
            throw new Error("Les informations du commercial ou de la commande sont manquantes.")
        }
        successMessage.value = "Commande enregistrée. Redirection vers WhatsApp..."
        cart.value = []
        saveCart()
        resetForm()
        setTimeout(() => {
            openCommercialWhatsApp(commercial, order)
        }, 700)
    } catch (error) {
        console.error("Erreur commande :", error)
        console.error("Réponse exacte Django :", error.response?.data)
        console.error("Status Django :", error.response?.status)
        if (error.response) {
            const responseStatus = error.response.status
            const data = error.response.data
            if (responseStatus === 400) {
                errorMessage.value = data.detail || data.message || data.error || "Les informations envoyées sont incorrectes."
            } else if (responseStatus === 401) {
                errorMessage.value = "Votre session a expiré. Veuillez vous reconnecter."
            } else if (responseStatus === 403) {
                errorMessage.value = "Vous n'avez pas l'autorisation de passer cette commande."
            } else if (responseStatus === 404) {
                errorMessage.value = "Le service de commande est introuvable. Vérifiez vos URLs Django."
            } else if (responseStatus === 409) {
                errorMessage.value = "Certains articles ne sont plus disponibles dans la quantité demandée."
            } else if (responseStatus >= 500) {
                errorMessage.value = "Une erreur est survenue sur le serveur. Veuillez réessayer."
            } else {
                errorMessage.value = "Impossible de passer la commande. Veuillez réessayer."
            }
        } else if (error.request) {
            errorMessage.value = "Impossible de contacter le serveur Django."
        } else {
            errorMessage.value = "Une erreur inattendue est survenue."
        }
    } finally {
        submitting.value = false
    }
}


/* INITIALISATION */
onMounted(async () => {
    loadLocalCart()
    console.log("Panier local chargé :", cart.value)
    if (isAuthenticated.value && cart.value.length > 0) {
        try {
            await syncCartWithServer()
        } catch (error) {
            console.error("Le panier local n'a pas pu être synchronisé :", error)
        }
    }
})
</script>

<template>
    <main class="cart-page">
        <section class="cart-hero">
            <div class="hero-decoration hero-decoration-one"></div>
            <div class="hero-decoration hero-decoration-two"></div>
            <div class="container hero-container">
                <div class="hero-breadcrumb">
                    <RouterLink to="/">Accueil</RouterLink>
                    <i class="fa-solid fa-chevron-right"></i>
                    <span>Panier</span>
                </div>
                <div class="hero-header">
                    <div class="hero-content">
                        <div class="hero-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                        <div class="hero-text">
                            <span class="hero-overline">VOTRE COMMANDE</span>
                            <h1>Finalisez votre <span>commande</span></h1>
                            <p>Votre commande est de <strong>{{ formatPrice(cartTotal) }}</strong>. Veuillez remplir le
                                formulaire et confirmer votre commande.</p>
                        </div>
                    </div>
                    <RouterLink to="/boutique" class="continue-shopping-header">
                        <span class="continue-icon"><i class="fa-solid fa-arrow-left"></i></span>
                        <span>Continuer mes achats</span>
                        <i class="fa-solid fa-arrow-right arrow"></i>
                    </RouterLink>
                </div>
            </div>
        </section>
        <section class="cart-section">
            <div class="container">
                <div v-if="successMessage" class="notification success">
                    <div class="notification-icon"><i class="fa-solid fa-check"></i></div>
                    <div><strong>Commande confirmée</strong>
                        <p>{{ successMessage }}</p>
                    </div>
                </div>
                <div v-if="errorMessage" class="notification error">
                    <div class="notification-icon"><i class="fa-solid fa-exclamation"></i></div>
                    <div><strong>Attention</strong>
                        <p>{{ errorMessage }}</p>
                    </div>
                </div>
                <div v-if="synchronizing" class="sync-message">
                    <i class="fa-solid fa-arrows-rotate fa-spin"></i>
                    <span>Synchronisation du panier...</span>
                </div>
                <div v-if="cart.length === 0 && !successMessage && !synchronizing" class="empty-cart">
                    <div class="empty-cart-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                    <span>VOTRE PANIER</span>
                    <h2>Votre panier est vide</h2>
                    <p>Vous n'avez encore ajouté aucun article à votre panier.</p>
                    <RouterLink to="/boutique" class="primary-button">Découvrir nos produits <i
                            class="fa-solid fa-arrow-right"></i></RouterLink>
                </div>
                <div v-else-if="cart.length > 0" class="checkout-layout">
                    <div class="products-area">
                        <div class="section-title">
                            <div class="title-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                            <div><span>MA SÉLECTION</span>
                                <h2>Votre panier</h2>
                            </div>
                        </div>
                        <div class="cart-top">
                            <div class="items-counter">
                                <span class="counter-number">{{ cartItemsCount }}</span>
                                <div><strong>{{ cartItemsCount > 1 ? "Articles" : "Article" }}</strong><small>dans votre
                                        panier</small></div>
                            </div>
                            <button type="button" class="clear-cart" @click="clearCart"><i
                                    class="fa-regular fa-trash-can"></i> Vider le panier</button>
                        </div>
                        <div class="products-list">
                            <article v-for="item in cart" :key="getCartKey(item)" class="cart-product">
                                <div class="product-image">
                                    <img v-if="getProductImage(item.image)" :src="getProductImage(item.image)"
                                        :alt="item.name">
                                    <div v-else class="image-placeholder"><i class="fa-solid fa-image"></i></div>
                                </div>
                                <div class="product-content">
                                    <div class="product-heading">
                                        <div>
                                            <span class="product-tag">{{ item.type === "range" ? "GAMME" : "PRODUIT"
                                            }}</span>
                                            <h3>{{ item.name }}</h3>
                                        </div>
                                        <button type="button" class="remove-product" title="Supprimer"
                                            @click="removeItem(item)">
                                            <i class="fa-solid fa-xmark"></i>
                                        </button>
                                    </div>
                                    <div class="product-price">{{ formatPrice(item.price) }} <span>/ unité</span></div>
                                    <div class="product-footer">
                                        <div class="quantity">
                                            <button type="button" @click="decreaseQuantity(item)"
                                                :disabled="item.quantity <= 1"><i
                                                    class="fa-solid fa-minus"></i></button>
                                            <strong>{{ item.quantity }}</strong>
                                            <button type="button" @click="increaseQuantity(item)"
                                                :disabled="item.type === 'product' && item.stock > 0 && item.quantity >= item.stock"><i
                                                    class="fa-solid fa-plus"></i></button>
                                        </div>
                                        <div class="line-total">{{ formatPrice(getItemTotal(item)) }}</div>
                                    </div>
                                </div>
                            </article>
                        </div>
                    </div>
                    <div class="form-area">
                        <div class="order-card">
                            <div class="order-header">
                                <div><span>COMMANDE</span>
                                    <h2>Vos coordonnées</h2>
                                </div>
                                <div class="header-user-icon"><i class="fa-solid fa-user"></i></div>
                            </div>
                            <form @submit.prevent="submitOrder">
                                <div class="form-block">
                                    <div class="block-title"><span class="block-number">01</span>
                                        <div><strong>Informations personnelles</strong><small>Comment pouvons-nous vous
                                                contacter ?</small></div>
                                    </div>
                                    <div class="form-grid">
                                        <div class="form-group">
                                            <label>Prénom <b>*</b></label>
                                            <div class="input-box"><i class="fa-regular fa-user"></i><input
                                                    v-model="form.first_name" type="text" placeholder="Votre prénom"
                                                    autocomplete="given-name" required></div>
                                        </div>
                                        <div class="form-group">
                                            <label>Nom <b>*</b></label>
                                            <div class="input-box"><i class="fa-regular fa-user"></i><input
                                                    v-model="form.last_name" type="text" placeholder="Votre nom"
                                                    autocomplete="family-name" required></div>
                                        </div>
                                    </div>
                                    <div class="form-grid">
                                        <div class="form-group">
                                            <label>Téléphone <b>*</b></label>
                                            <div class="input-box"><i class="fa-solid fa-phone"></i><input
                                                    v-model="form.phone" type="tel" placeholder="Ex : 6 XX XX XX XX"
                                                    autocomplete="tel" required></div>
                                        </div>
                                        <div class="form-group">
                                            <label>Adresse e-mail <b>*</b></label>
                                            <div class="input-box"><i class="fa-regular fa-envelope"></i><input
                                                    v-model="form.email" type="email" placeholder="exemple@email.com"
                                                    autocomplete="email" required></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-separator"></div>
                                <div class="form-block">
                                    <div class="block-title"><span class="block-number">02</span>
                                        <div><strong>Adresse de livraison</strong><small>Où souhaitez-vous recevoir
                                                votre commande ?</small></div>
                                    </div>
                                    <div class="form-grid">
                                        <div class="form-group">
                                            <label>Ville <b>*</b></label>
                                            <div class="input-box"><i class="fa-solid fa-city"></i><input
                                                    v-model="form.city" type="text" placeholder="Ex : Douala"
                                                    autocomplete="address-level2" required></div>
                                        </div>
                                        <div class="form-group">
                                            <label>Quartier <b>*</b></label>
                                            <div class="input-box"><i class="fa-solid fa-location-dot"></i><input
                                                    v-model="form.address" type="text" placeholder="Ex : Ndogbong"
                                                    autocomplete="street-address" required></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="summary">
                                    <div class="summary-title">
                                        <div><span>RÉCAPITULATIF</span><strong>Total de la commande</strong></div><i
                                            class="fa-solid fa-receipt"></i>
                                    </div>
                                    <div class="summary-line"><span>{{ cartItemsCount }} {{
                                        cartItemsCount > 1 ? "articles" : "article" }}</span><strong>{{
                                                formatPrice(cartTotal) }}</strong></div>
                                    <div class="summary-total">
                                        <div><span>Total</span><small>Montant de votre commande</small></div><strong>{{
                                            formatPrice(cartTotal) }}</strong>
                                    </div>
                                </div>
                                <button type="submit" class="submit-button" :disabled="submitting || synchronizing">
                                    <template v-if="!submitting"><span>Confirmer ma commande</span><i
                                            class="fa-solid fa-arrow-right"></i></template>
                                    <template v-else><i class="fa-solid fa-spinner fa-spin"></i><span>Enregistrement de
                                            la commande...</span></template>
                                </button>
                                <div class="privacy-note"><i class="fa-solid fa-shield-halved"></i><span>Vos
                                        informations sont utilisées uniquement pour
                                        traiter votre commande.</span></div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
</template>

<style scoped>
.cart-page {
    --green: #38B04C;
    --green-dark: #2F963F;
    --green-soft: #EEF8F0;
    --blue: #00AEEF;
    --blue-soft: #EFFAFF;
    --dark: #202522;
    --text: #343936;
    --muted: #7B837D;
    --border: #E1E8E2;
    --border-dark: #D4DED6;
    --bg: #F7F9F7;
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
}

.cart-hero {
    position: relative;
    overflow: hidden;
    padding: 22px 0 34px;
    background: linear-gradient(120deg, #F1FAF3 0%, #FFFFFF 55%, #F0FAFD 100%);
    border-bottom: 1px solid #E5ECE7;
}

.hero-container {
    position: relative;
    z-index: 2;
}

.hero-decoration {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
}

.hero-decoration-one {
    width: 280px;
    height: 280px;
    right: -110px;
    top: -155px;
    background: rgba(56, 176, 76, .07);
}

.hero-decoration-two {
    width: 200px;
    height: 200px;
    left: -120px;
    bottom: -165px;
    background: rgba(0, 174, 239, .055);
}

.hero-breadcrumb {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 21px;
    color: #929A94;
    font-size: 12px;
}

.hero-breadcrumb a {
    color: var(--green);
    text-decoration: none;
    font-weight: 700;
}

.hero-breadcrumb i {
    font-size: 7px;
    color: #B5BCB7;
}

.hero-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
}

.hero-content {
    display: flex;
    align-items: center;
    gap: 16px;
    max-width: 900px;
}

.hero-icon {
    width: 54px;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border-radius: 15px;
    background: rgba(255, 255, 255, .9);
    color: var(--green);
    border: 1px solid #E3ECE5;
    box-shadow: 0 7px 20px rgba(45, 80, 51, .07);
}

.hero-icon i {
    font-size: 20px;
}

.hero-overline {
    display: block;
    margin-bottom: 4px;
    color: var(--green);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.7px;
}

.hero-content h1 {
    margin: 0;
    color: var(--dark);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 36px;
    font-weight: 500;
    line-height: 1.12;
}

.hero-content h1 span {
    color: var(--green);
}

.hero-content p {
    max-width: 780px;
    margin: 9px 0 0;
    color: #737C76;
    font-size: 14px;
    line-height: 1.65;
}

.hero-content p strong {
    color: var(--green);
    font-size: 16px;
    font-weight: 900;
}

.continue-shopping-header {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    flex-shrink: 0;
    padding: 9px 13px;
    border: 1px solid #DCE7DF;
    border-radius: 10px;
    background: rgba(255, 255, 255, .55);
    color: var(--green);
    font-size: 11px;
    font-weight: 800;
    text-decoration: none;
    transition: .25s ease;
}

.continue-shopping-header:hover {
    background: #fff;
    color: var(--green-dark);
    border-color: #C9DCCA;
    transform: translateX(-2px);
}

.continue-icon {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: var(--green-soft);
}

.continue-shopping-header .arrow {
    margin-left: 2px;
    font-size: 9px;
}

.cart-section {
    padding: 36px 0 70px;
}

.notification {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 22px;
    padding: 13px 16px;
    border-radius: 12px;
}

.notification-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border-radius: 50%;
}

.notification strong {
    display: block;
    margin-bottom: 3px;
    font-size: 14px;
}

.notification p {
    margin: 0;
    font-size: 12px;
}

.notification.success {
    color: #276C34;
    background: #F0FAF2;
    border: 1px solid #D0E8D4;
}

.notification.success .notification-icon {
    background: #DDF2E1;
    color: var(--green);
}

.notification.error {
    color: #983D3D;
    background: #FFF5F5;
    border: 1px solid #F0D5D5;
}

.notification.error .notification-icon {
    background: #FFE3E3;
    color: #D9534F;
}

.sync-message {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 10px;
    background: var(--green-soft);
    color: var(--green);
    font-size: 12px;
    font-weight: 700;
}

.checkout-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.04fr) minmax(430px, .96fr);
    gap: 34px;
    align-items: start;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 13px;
}

.title-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border-radius: 14px;
    background: var(--green-soft);
    color: var(--green);
}

.section-title span {
    display: block;
    margin-bottom: 3px;
    color: var(--green);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.6px;
}

.section-title h2 {
    margin: 0;
    color: var(--dark);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 27px;
    font-weight: 500;
}

.cart-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    padding: 11px 0;
    border-bottom: 1px solid #E2E9E4;
}

.items-counter {
    display: flex;
    align-items: center;
    gap: 10px;
}

.counter-number {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 9px;
    background: var(--green-soft);
    color: var(--green);
    font-size: 13px;
    font-weight: 800;
}

.items-counter div {
    display: flex;
    flex-direction: column;
    gap: 1px;
}

.items-counter strong {
    color: #363B38;
    font-size: 12px;
}

.items-counter small {
    color: #9BA29D;
    font-size: 10px;
}

.clear-cart {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px;
    border: 0;
    background: transparent;
    color: #999;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
}

.clear-cart:hover {
    color: #D9534F;
}

.products-list {
    display: flex;
    flex-direction: column;
}

.cart-product {
    display: flex;
    gap: 15px;
    padding: 18px 0;
    border-bottom: 1px solid #E2E9E4;
}

.cart-product:first-child {
    padding-top: 10px;
}

.product-image {
    width: 108px;
    height: 108px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    overflow: hidden;
    border-radius: 11px;
    background: #fff;
    border: 1px solid #E3E9E4;
}

.product-image img {
    display: block;
    width: 100%;
    height: 100%;
    padding: 8px;
    object-fit: contain;
}

.image-placeholder {
    color: #AAB1AC;
    font-size: 24px;
}

.product-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.product-heading {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}

.product-tag {
    display: block;
    margin-bottom: 3px;
    color: var(--green);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.3px;
}

.product-heading h3 {
    max-width: 350px;
    margin: 0;
    overflow: hidden;
    color: var(--dark);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 18px;
    font-weight: 600;
    white-space: nowrap;
    text-overflow: ellipsis;
}

.remove-product {
    width: 29px;
    height: 29px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 0;
    border-radius: 7px;
    background: #F7F8F7;
    color: #A5AAA7;
    cursor: pointer;
}

.remove-product:hover {
    background: #FFF0F0;
    color: #D9534F;
}

.product-price {
    margin-top: 8px;
    color: var(--green);
    font-size: 13px;
    font-weight: 800;
}

.product-price span {
    color: #A0A6A2;
    font-size: 10px;
    font-weight: 400;
}

.product-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 14px;
}

.quantity {
    height: 34px;
    display: flex;
    align-items: center;
    overflow: hidden;
    border: 1px solid #DCE5DE;
    border-radius: 8px;
    background: #fff;
}

.quantity button {
    width: 34px;
    height: 100%;
    border: 0;
    background: #fff;
    color: #606862;
    cursor: pointer;
}

.quantity button:hover:not(:disabled) {
    background: var(--green);
    color: #fff;
}

.quantity button:disabled {
    opacity: .3;
    cursor: not-allowed;
}

.quantity strong {
    width: 34px;
    text-align: center;
    color: #303532;
    font-size: 12px;
}

.line-total {
    color: var(--dark);
    font-size: 15px;
    font-weight: 800;
}

.order-card {
    position: sticky;
    top: 20px;
    padding: 24px 25px;
    border: 1px solid var(--border-dark);
    border-radius: 18px;
    background: transparent;
    box-shadow: 0 8px 30px rgba(25, 55, 30, .035);
}

.order-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
    padding-bottom: 17px;
    border-bottom: 1px solid #E2E9E4;
}

.order-header span {
    display: block;
    margin-bottom: 4px;
    color: var(--green);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.6px;
}

.order-header h2 {
    margin: 0;
    color: var(--dark);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 25px;
    font-weight: 500;
}

.header-user-icon {
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: var(--blue-soft);
    color: var(--blue);
}

.block-title {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 16px;
}

.block-number {
    width: 31px;
    height: 31px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border-radius: 8px;
    background: var(--green-soft);
    color: var(--green);
    font-size: 10px;
    font-weight: 900;
}

.block-title strong {
    display: block;
    color: #343936;
    font-size: 13px;
}

.block-title small {
    display: block;
    margin-top: 3px;
    color: #929A95;
    font-size: 10px;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.form-group {
    margin-bottom: 14px;
}

.form-group label {
    display: block;
    margin-bottom: 6px;
    color: #454C47;
    font-size: 11px;
    font-weight: 700;
}

.form-group label b {
    color: #D9534F;
}

.input-box {
    position: relative;
}

.input-box i {
    position: absolute;
    left: 14px;
    top: 50%;
    z-index: 2;
    color: #9AA49E;
    font-size: 13px;
    transform: translateY(-50%);
}

.input-box input {
    width: 100%;
    height: 46px;
    box-sizing: border-box;
    padding: 0 12px 0 39px;
    border: 1px solid #D7E1DA;
    outline: none;
    border-radius: 9px;
    background: rgba(255, 255, 255, .32);
    color: #252925;
    font-family: inherit;
    font-size: 12px;
    transition: .25s ease;
}

.input-box input::placeholder {
    color: #A8AFAB;
    font-size: 11px;
}

.input-box input:focus {
    border-color: var(--green);
    background: rgba(255, 255, 255, .7);
    box-shadow: 0 0 0 3px rgba(56, 176, 76, .065);
}

.input-box:focus-within i {
    color: var(--green);
}

.form-separator {
    height: 1px;
    margin: 21px 0;
    background: #E3EAE5;
}

.summary {
    margin-top: 20px;
    padding: 18px;
    border: 1px solid var(--border-dark);
    border-radius: 14px;
}

.summary-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.summary-title span {
    display: block;
    margin-bottom: 3px;
    color: var(--green);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.summary-title strong {
    color: #303632;
    font-size: 14px;
}

.summary-title>i {
    color: var(--green);
    font-size: 18px;
}

.summary-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #777F79;
    font-size: 11px;
}

.summary-line strong {
    color: #343936;
    font-size: 13px;
}

.summary-total {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #DFE8E1;
}

.summary-total span {
    display: block;
    color: #272C28;
    font-size: 15px;
    font-weight: 800;
}

.summary-total small {
    display: block;
    margin-top: 2px;
    color: #9BA19D;
    font-size: 9px;
}

.summary-total strong {
    color: var(--green);
    font-size: 20px;
    font-weight: 900;
    white-space: nowrap;
}

.submit-button {
    width: 100%;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin-top: 18px;
    padding: 0 18px;
    border: 0;
    border-radius: 10px;
    background: var(--green);
    color: #fff;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(56, 176, 76, .22);
    transition: .25s ease;
}

.submit-button:hover:not(:disabled) {
    background: var(--green-dark);
    transform: translateY(-2px);
}

.submit-button:disabled {
    opacity: .65;
    cursor: not-allowed;
}

.privacy-note {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 6px;
    margin-top: 12px;
    color: #9CA29E;
    font-size: 9px;
    line-height: 1.5;
    text-align: center;
}

.privacy-note i {
    margin-top: 1px;
    color: var(--green);
}

.empty-cart {
    min-height: 450px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 35px;
    border: 1px solid var(--border);
    border-radius: 18px;
    text-align: center;
}

.empty-cart-icon {
    width: 88px;
    height: 88px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 19px;
    border-radius: 50%;
    background: var(--green-soft);
    color: var(--green);
}

.empty-cart-icon i {
    font-size: 29px;
}

.empty-cart>span {
    margin-bottom: 6px;
    color: var(--green);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.7px;
}

.empty-cart h2 {
    margin: 0 0 8px;
    color: var(--dark);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 29px;
    font-weight: 500;
}

.empty-cart p {
    margin: 0;
    color: #9AA19C;
    font-size: 12px;
}

.primary-button {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    margin-top: 21px;
    padding: 13px 19px;
    border-radius: 9px;
    background: var(--green);
    color: #fff;
    font-size: 12px;
    font-weight: 800;
    text-decoration: none;
    transition: .25s ease;
}

.primary-button:hover {
    background: var(--green-dark);
    color: #fff;
    transform: translateY(-2px);
}

@media(max-width:1100px) {
    .checkout-layout {
        grid-template-columns: 1fr;
        gap: 38px;
    }

    .order-card {
        position: relative;
        top: 0;
    }
}

@media(max-width:768px) {
    .cart-hero {
        padding: 17px 0 29px;
    }

    .hero-header {
        align-items: flex-start;
        flex-direction: column;
        gap: 17px;
    }

    .hero-content h1 {
        font-size: 31px;
    }

    .hero-content p {
        font-size: 12px;
    }

    .continue-shopping-header {
        margin-left: 61px;
    }

    .cart-section {
        padding: 28px 0 52px;
    }
}

@media(max-width:576px) {
    .hero-content h1 {
        font-size: 27px;
    }

    .hero-content p {
        font-size: 10.5px;
    }

    .continue-shopping-header {
        margin-left: 55px;
    }

    .section-title h2 {
        font-size: 23px;
    }

    .cart-product {
        gap: 10px;
        padding: 14px 0;
    }

    .product-image {
        width: 82px;
        height: 82px;
    }

    .product-heading h3 {
        max-width: 220px;
        font-size: 15px;
    }

    .line-total {
        font-size: 13px;
    }

    .order-card {
        padding: 18px 15px;
        border-radius: 15px;
    }

    .order-header h2 {
        font-size: 22px;
    }

    .form-grid {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .summary-total strong {
        font-size: 18px;
    }

    .empty-cart {
        min-height: 400px;
        padding: 25px;
    }

    .empty-cart h2 {
        font-size: 25px;
    }
}

@media(max-width:400px) {
    .hero-content h1 {
        font-size: 24px;
    }

    .continue-shopping-header {
        margin-left: 0;
    }

    .section-title h2 {
        font-size: 21px;
    }

    .cart-product {
        flex-direction: column;
    }

    .product-image {
        width: 100%;
        height: 150px;
    }

    .product-heading h3 {
        max-width: 190px;
    }

    .product-footer {
        margin-top: 12px;
    }

    .order-card {
        padding: 16px 12px;
    }
}
</style>