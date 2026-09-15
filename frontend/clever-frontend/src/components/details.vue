<script setup>
import {ref,computed,onMounted,watch} from "vue"
import {RouterLink,useRoute,useRouter} from "vue-router"
import api from "../services/api"
import{notifyCartChanged}from"../services/headerState"

const route=useRoute()
const router=useRouter()
const product=ref(null)
const relatedProducts=ref([])
const categoryProducts=ref([])
const rangeProducts=ref([])
const productRange=ref(null)
const loading=ref(true)
const error=ref(false)
const quantity=ref(1)
const activeImage=ref(null)
const activeTab=ref("description")
const cart=ref([])
const showCart=ref(false)
const getProductImage=(image)=>{
    if(!image||typeof image!=="string")return null
    image=image.trim()
    if(!image)return null
    if(image.startsWith("http://")||image.startsWith("https://"))return image
    if(image.startsWith("data:image"))return image
    const baseURL=api.defaults.baseURL||"http://127.0.0.1:7000/api"
    const serverURL=baseURL.replace(/\/api\/?$/,"").replace(/\/$/,"")
    return `${serverURL}${image.startsWith("/")?image:`/${image}`}`
}
const formatPrice=(price)=>{
    if(price===null||price===undefined||price==="")return"0 FCFA"
    const number=Number(price)
    if(Number.isNaN(number))return"0 FCFA"
    return new Intl.NumberFormat("fr-FR",{minimumFractionDigits:0,maximumFractionDigits:0}).format(number)+" FCFA"
}
const getProductPrice=(item)=>{
    if(!item)return 0
    return Number(
        item.current_price??
        item.promotional_price??
        item.price??
        0
    )||0
}
const getRangePrice=(range)=>{
    if(!range)return 0
    return Number(
        range.current_price??
        range.promotional_price??
        range.price??
        0
    )||0
}
const currentPrice=computed(()=>{
    return getProductPrice(product.value)
})
const stockAvailable=computed(()=>{
    return !!product.value&&Number(product.value.stock)>0
})
const cartItemsCount=computed(()=>{
    return cart.value.reduce(
        (total,item)=>total+Number(item.quantity||0),
        0
    )
})
const cartTotal=computed(()=>{
    return cart.value.reduce(
        (total,item)=>
            total+
            Number(item.price||0)*
            Number(item.quantity||0),
        0
    )
})
const getItemTotal=(item)=>{
    return Number(item.price||0)*
        Number(item.quantity||0)
}
const getProductCartKey=(item)=>{
    if(!item)return null
    const productId=Number(
        item.product_id||
        item.product||
        item.id
    )
    if(!productId||Number.isNaN(productId))return null
    return `product_${productId}`
}
const getRangeCartKey=(item)=>{
    if(!item)return null
    const rangeId=Number(
        item.range_id||
        item.product_range_id||
        item.product_range
    )
    if(!rangeId||Number.isNaN(rangeId))return null
    return `range_${rangeId}`
}
const getCartKey=(item)=>{
    if(!item)return null
    if(item.type==="range"||item.item_type==="range"){
        return getRangeCartKey(item)
    }
    return getProductCartKey(item)
}
const normalizeCartItem=(item)=>{
    if(!item)return null
    if(
        item.type==="range"||
        item.item_type==="range"||
        item.range_id!==undefined||
        item.product_range_id!==undefined||
        item.product_range!==undefined
    ){
        const rangeId=Number(
            item.range_id||
            item.product_range_id||
            item.product_range||
            item.id
        )
        if(!rangeId||Number.isNaN(rangeId))return null
        return{
            type:"range",
            item_type:"range",
            range_id:rangeId,
            product_range:rangeId,
            id:`range_${rangeId}`,
            name:item.name||item.product_range_name||"Gamme",
            slug:item.slug||"",
            image:item.image||item.range_image||item.product_range_image||null,
            price:Number(
                item.price??
                item.unit_price??
                item.current_price??
                item.promotional_price??
                0
            )||0,
            stock:0,
            quantity:Number(item.quantity||1)
        }
    }
    if(
        item.type==="product"||
        item.item_type==="product"||
        item.product_id!==undefined||
        item.product!==undefined
    ){
        const productId=Number(
            item.product_id||
            item.product||
            item.id
        )
        if(!productId||Number.isNaN(productId))return null
        return{
            type:"product",
            item_type:"product",
            product_id:productId,
            product:productId,
            id:`product_${productId}`,
            name:item.name||item.product_name||"Produit",
            slug:item.slug||"",
            image:item.image||item.product_image||item.main_image||null,
            price:Number(
                item.price??
                item.unit_price??
                item.current_price??
                item.promotional_price??
                0
            )||0,
            stock:Number(item.stock||0),
            quantity:Number(item.quantity||1)
        }
    }
    return null
}
const saveCart=()=>{
    try{
        localStorage.setItem(
            "shop_cart",
            JSON.stringify(cart.value)
        )
    }catch(error){
        console.error(
            "Erreur lors de la sauvegarde du panier :",
            error
        )
    }
}
const loadCart=()=>{
    try{
        const savedCart=localStorage.getItem("shop_cart")
        if(!savedCart){
            cart.value=[]
            return
        }
        const parsedCart=JSON.parse(savedCart)
        if(!Array.isArray(parsedCart)){
            cart.value=[]
            return
        }
        cart.value=parsedCart
            .map(normalizeCartItem)
            .filter(Boolean)
        saveCart()
        console.log(
            "Panier chargé depuis produit.vue :",
            cart.value
        )
    }catch(error){
        console.error(
            "Erreur lors du chargement du panier :",
            error
        )
        cart.value=[]
    }
}
const increaseQuantity=()=>{
    if(!product.value)return
    const stock=Number(product.value.stock||0)
    if(stock<=0)return
    if(Number(quantity.value)<stock){
        quantity.value++
    }
}
const decreaseQuantity=()=>{
    if(Number(quantity.value)>1){
        quantity.value--
    }
}
const increaseCartQuantity=(item)=>{
    if(!item)return
    if(item.type==="product"){
        const stock=Number(item.stock||0)
        if(stock>0&&Number(item.quantity)>=stock)return
    }
    item.quantity=Number(item.quantity||0)+1
    saveCart()
}
const decreaseCartQuantity=(item)=>{
    if(!item)return
    const currentQuantity=Number(item.quantity||0)
    if(currentQuantity<=1)return
    item.quantity=currentQuantity-1
    saveCart()
}
const removeFromCart=(item)=>{
    if(!item)return
    const key=getCartKey(item)
    if(!key)return
    cart.value=cart.value.filter(
        cartItem=>getCartKey(cartItem)!==key
    )
    saveCart()
}
const clearCart=()=>{
    cart.value=[]
    saveCart()
}
const closeCart=()=>{
    showCart.value=false
}
const addToCart=(item,quantityToAdd=1,openCart=true)=>{
    if(!item||!item.id)return
    const stock=Number(item.stock||0)
    if(stock<=0)return
    const productId=Number(item.id)
    if(!productId||Number.isNaN(productId))return
    const price=getProductPrice(item)
    const image=item.main_image
        ?getProductImage(item.main_image)
        :item.images?.length
            ?getProductImage(item.images[0].image)
            :null
    const existingProduct=cart.value.find(
        cartItem=>
            cartItem.type==="product"&&
            Number(cartItem.product_id)===productId
    )
    if(existingProduct){
        const newQuantity=
            Number(existingProduct.quantity||0)+
            Number(quantityToAdd||0)
        existingProduct.quantity=Math.min(
            newQuantity,
            stock
        )
        existingProduct.price=price
        existingProduct.image=image
        existingProduct.stock=stock
        existingProduct.name=item.name||existingProduct.name
        existingProduct.slug=item.slug||existingProduct.slug
    }else{
        cart.value.push({
            type:"product",
            item_type:"product",
            product_id:productId,
            product:productId,
            id:`product_${productId}`,
            name:item.name||"Produit",
            slug:item.slug||"",
            image:image,
            price:price,
            quantity:Math.min(
                Number(quantityToAdd)||1,
                stock
            ),
            stock:stock
        })
    }
    saveCart()
    console.log(
        "Produit ajouté depuis la page détail :",
        product.value?.name
    )
    console.log(
        "Panier actuel :",
        cart.value
    )
    if(openCart){
        showCart.value=true
    }
}
const createRangeCartItem=(range)=>{
    if(!range||!range.id)return null
    const rangeId=Number(range.id)
    if(!rangeId||Number.isNaN(rangeId))return null
    return{
        type:"range",
        item_type:"range",
        range_id:rangeId,
        product_range:rangeId,
        id:`range_${rangeId}`,
        name:range.name||"Gamme",
        slug:range.slug||"",
        image:range.image
            ?getProductImage(range.image)
            :null,
        price:getRangePrice(range),
        stock:0,
        quantity:1
    }
}
const addRangeToCart=(range)=>{
    if(!range||!range.id)return
    const rangeId=Number(range.id)
    if(!rangeId||Number.isNaN(rangeId))return
    const existingRange=cart.value.find(
        item=>
            item.type==="range"&&
            Number(item.range_id)===rangeId
    )
    if(existingRange){
        existingRange.quantity=
            Number(existingRange.quantity||0)+1
        existingRange.price=getRangePrice(range)
        existingRange.image=range.image
            ?getProductImage(range.image)
            :existingRange.image
        existingRange.name=range.name||existingRange.name
        existingRange.slug=range.slug||existingRange.slug
    }else{
        const cartItem=createRangeCartItem(range)
        if(cartItem){
            cart.value.push(cartItem)
        }
    }
    saveCart()
    console.log(
        "Gamme ajoutée depuis produit.vue :",
        range.name
    )
    console.log(
        "Panier actuel :",
        cart.value
    )
    showCart.value=true
}
const orderRangeDirectly=(range)=>{
    if(!range||!range.id)return
    const rangeId=Number(range.id)
    if(!rangeId||Number.isNaN(rangeId))return
    const existingRange=cart.value.find(
        item=>
            item.type==="range"&&
            Number(item.range_id)===rangeId
    )
    if(existingRange){
        existingRange.quantity=
            Number(existingRange.quantity||0)+1
    }else{
        const cartItem=createRangeCartItem(range)
        if(cartItem){
            cart.value.push(cartItem)
        }
    }
    saveCart()
    router.push("/panier")
}
const buyNow=()=>{
    if(!product.value||!stockAvailable.value)return
    addToCart(
        product.value,
        quantity.value,
        false
    )
    router.push("/panier")
}
const selectImage=(image)=>{
    activeImage.value=getProductImage(image)
}
const resetProductState=()=>{
    product.value=null
    productRange.value=null
    relatedProducts.value=[]
    categoryProducts.value=[]
    rangeProducts.value=[]
    activeImage.value=null
    activeTab.value="description"
    quantity.value=1
}
const loadRelatedProducts=async()=>{
    if(!product.value)return
    try{
        const response=await api.get("/products/")
        const products=response.data?.results||response.data||[]
        const currentId=product.value.id
        const categoryId=product.value.category
        const subcategoryId=product.value.subcategory
        const rangeId=product.value.product_range
        relatedProducts.value=Array.isArray(products)
            ?products.filter(
                item=>
                    item.id!==currentId&&
                    item.is_active!==false&&
                    item.category===categoryId&&
                    item.subcategory===subcategoryId
            ).slice(0,8)
            :[]
        categoryProducts.value=Array.isArray(products)
            ?products.filter(
                item=>
                    item.id!==currentId&&
                    item.is_active!==false&&
                    item.category===categoryId&&
                    item.subcategory!==subcategoryId
            ).slice(0,8)
            :[]
        rangeProducts.value=Array.isArray(products)
            ?products.filter(
                item=>
                    item.id!==currentId&&
                    item.is_active!==false&&
                    rangeId&&
                    item.product_range===rangeId
            ).slice(0,6)
            :[]
    }catch(error){
        console.error(
            "Erreur lors du chargement des produits associés :",
            error
        )
        relatedProducts.value=[]
        categoryProducts.value=[]
        rangeProducts.value=[]
    }
}
const loadProductRange=async()=>{
    if(!product.value?.product_range){
        productRange.value=null
        return
    }
    try{
        const response=await api.get(
            `/products/product-ranges/${product.value.product_range}/`
        )
        productRange.value=response.data
    }catch(error){
        console.error(
            "Erreur lors du chargement de la gamme :",
            error
        )
        productRange.value=null
    }
}
const loadProduct=async()=>{
    const slug=route.query.slug
    if(!slug){
        resetProductState()
        error.value=true
        loading.value=false
        return
    }
    try{
        loading.value=true
        error.value=false
        resetProductState()
        const response=await api.get(
            `/products/${slug}/`
        )
        product.value=response.data
        if(product.value?.main_image){
            activeImage.value=getProductImage(
                product.value.main_image
            )
        }else if(product.value?.images?.length){
            activeImage.value=getProductImage(
                product.value.images[0].image
            )
        }
        await Promise.all([
            loadRelatedProducts(),
            loadProductRange()
        ])
    }catch(error){
        console.error(
            "Erreur lors du chargement du produit :",
            error
        )
        error.value=true
        product.value=null
    }finally{
        loading.value=false
    }
}
onMounted(()=>{
    loadCart()
    loadProduct()
})
watch(
    ()=>route.query.slug,
    async(newSlug,oldSlug)=>{
        if(newSlug===oldSlug)return
        await loadProduct()
        window.scrollTo({
            top:0,
            behavior:"smooth"
        })
    }
)
</script>

<template>
    <section class="product-details-section">
        <div class="container">
            <div v-if="loading" class="product-loading">
                <div class="loading-image"></div>
                <div class="loading-content">
                    <div class="loading-line small"></div>
                    <div class="loading-line large"></div>
                    <div class="loading-line medium"></div>
                    <div class="loading-line price"></div>
                    <div class="loading-line button"></div>
                </div>
            </div>
            <div v-else-if="error || !product" class="product-error">
                <i class="fa-solid fa-circle-exclamation"></i>
                <h2>Produit introuvable</h2>
                <p>Le produit demandé n'existe pas ou n'est plus disponible.</p>
                <RouterLink to="/boutique" class="back-shop-button">
                    <i class="fa-solid fa-arrow-left"></i>
                    Retour à la boutique
                </RouterLink>
            </div>
            <div v-else>
                <div class="breadcrumb">
                    <RouterLink to="/">Accueil</RouterLink>
                    <i class="fa-solid fa-chevron-right"></i>
                    <RouterLink to="/boutique">Boutique</RouterLink>
                    <i class="fa-solid fa-chevron-right"></i>
                    <span>{{ product.category_name }}</span>
                    <i class="fa-solid fa-chevron-right"></i>
                    <span>{{ product.subcategory_name }}</span>
                    <i class="fa-solid fa-chevron-right"></i>
                    <span>{{ product.name }}</span>
                </div>
                <div class="product-main">
                    <div class="product-gallery">
                        <div class="main-image-container">
                            <span v-if="product.is_on_sale" class="sale-badge">PROMO</span>
                            <img v-if="activeImage" :src="activeImage" :alt="product.name" class="main-product-image">
                            <div v-else class="no-image">
                                <i class="fa-solid fa-image"></i>
                                <span>Image indisponible</span>
                            </div>
                        </div>
                        <div class="product-thumbnails">
                            <button v-if="product.main_image" type="button" class="thumbnail"
                                :class="{ active: activeImage === getProductImage(product.main_image) }"
                                @click="selectImage(product.main_image)">
                                <img :src="getProductImage(product.main_image)" :alt="product.name">
                            </button>
                            <button v-for="image in product.images" :key="image.id" type="button" class="thumbnail"
                                :class="{ active: activeImage === getProductImage(image.image) }"
                                @click="selectImage(image.image)">
                                <img :src="getProductImage(image.image)" :alt="image.alt_text || product.name">
                            </button>
                        </div>
                    </div>
                    <div class="product-information">
                        <div class="top-product-line">
                            <div>
                                <span class="product-category">{{ product.category_name }}</span>
                                <span class="product-subcategory">{{ product.subcategory_name }}</span>
                                <h1 class="product-title">{{ product.name }}</h1>
                                <span class="product-reference">Référence : {{ product.reference }}</span>
                            </div>
                            <button type="button" class="favorite-button">
                                <i class="fa-regular fa-heart"></i>
                            </button>
                        </div>
                        <div class="rating-row">
                            <div class="product-rating">
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-regular fa-star"></i>
                            </div>
                            <span>4.0</span>
                            <span class="rating-separator">•</span>
                            <span>Avis clients</span>
                        </div>
                        <div class="price-row">
                            <strong :class="{ sale: product.is_on_sale }">
                                {{ formatPrice(currentPrice) }}
                            </strong>
                            <span v-if="product.is_on_sale" class="old-price">
                                {{ formatPrice(product.price) }}
                            </span>
                            <span v-if="product.is_on_sale" class="discount">
                                PROMO
                            </span>
                        </div>
                        <div class="stock">
                            <span :class="{ unavailable: !stockAvailable }"></span>
                            <span v-if="stockAvailable">
                                En stock
                                <span v-if="product.stock">
                                    • {{ product.stock }} disponibles
                                </span>
                            </span>
                            <span v-else>
                                Rupture de stock
                            </span>
                        </div>
                        <div class="customer-message">
                            <div class="customer-message-icon">
                                <i class="fa-solid fa-wand-magic-sparkles"></i>
                            </div>
                            <div>
                                <strong>Une solution pensée pour vos besoins</strong>
                                <p>
                                    Ce produit a été soigneusement sélectionné dans la 
                                    <strong>{{ product.category_name }}</strong>, pour
                                    <strong>{{ product.subcategory_name }}</strong>.
                                    Il vous accompagne efficacement dans vos besoins et vous offre une
                                    expérience adaptée .
                                </p>
                            </div>
                        </div>
                        <p class="product-summary">
                            {{ product.description }}
                        </p>
                        <div class="purchase-title">
                            Quantité
                        </div>
                        <div class="purchase-row">
                            <div class="quantity-selector">
                                <button type="button" @click="decreaseQuantity" :disabled="quantity <= 1">
                                    <i class="fa-solid fa-minus"></i>
                                </button>
                                <span>{{ quantity }}</span>
                                <button type="button" @click="increaseQuantity"
                                    :disabled="!stockAvailable || quantity >= product.stock">
                                    <i class="fa-solid fa-plus"></i>
                                </button>
                            </div>
                            <button type="button" class="add-cart-button" :disabled="!stockAvailable"
                                @click="addToCart(product, quantity)">
                                <i class="fa-solid fa-cart-shopping"></i>
                                Ajouter au panier
                            </button>
                        </div>
                        <button type="button" class="buy-now-button" :disabled="!stockAvailable" @click="buyNow">
                            <i class="fa-solid fa-bag-shopping"></i>
                            Acheter maintenant
                        </button>
                        <div class="delivery-info">
                            <i class="fa-solid fa-truck"></i>
                            <div>
                                <strong>Livraison disponible</strong>
                                <span>Partout au Cameroun</span>
                            </div>
                        </div>
                        <div class="product-mini-info">
                            <div>
                                <i class="fa-solid fa-shield-halved"></i>
                                <span>Paiement sécurisé</span>
                            </div>
                            <div>
                                <i class="fa-solid fa-headset"></i>
                                <span>Service client de qualité</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="details-section">
                    <div class="details-tabs">
                        <button type="button" :class="{ active: activeTab === 'description' }"
                            @click="activeTab = 'description'">Description</button>
                        <button type="button" :class="{ active: activeTab === 'composition' }"
                            @click="activeTab = 'composition'">Composition</button>
                        <button type="button" :class="{ active: activeTab === 'usage' }"
                            @click="activeTab = 'usage'">Utilisation</button>
                        <button type="button" :class="{ active: activeTab === 'precautions' }"
                            @click="activeTab = 'precautions'">Précautions</button>
                    </div>
                    <div class="details-content">
                        <div v-if="activeTab === 'description'">
                            <h3>Pourquoi choisir {{ product.name }} ?</h3>
                            <p>{{ product.description }}</p>
                        </div>
                        <div v-if="activeTab === 'composition'">
                            <h3>Composition</h3>
                            <p v-if="product.composition">{{ product.composition }}</p>
                            <p v-else class="empty-detail">Aucune composition renseignée.</p>
                        </div>
                        <div v-if="activeTab === 'usage'">
                            <h3>Mode d'utilisation</h3>
                            <p v-if="product.usage">{{ product.usage }}</p>
                            <p v-else class="empty-detail">Aucune indication d'utilisation renseignée.</p>
                        </div>
                        <div v-if="activeTab === 'precautions'">
                            <h3>Précautions</h3>
                            <p v-if="product.precautions">{{ product.precautions }}</p>
                            <p v-else class="empty-detail">Aucune précaution renseignée.</p>
                        </div>
                    </div>
                </div>
                <section v-if="product.product_range && productRange" class="range-section">
                    <div class="range-heading">
                        
                        <h2>Découvrez la <span>{{ productRange.name }}</span></h2>
                        <p>soigneusement sélectionnée pour répondre à vos besoins.</p>
                    </div>
                    <div class="range-presentation"
                        :style="{ backgroundImage: productRange.image ? `url(${getProductImage(productRange.image)})` : 'none' }">
                        <div class="range-overlay"></div>
                        <div class="range-content">
                            <p class="range-description">{{ productRange.description || "Découvrez notre gamme de produits soigneusement sélectionnés pour prendre soin de vous." }}</p>
                            <div v-if="getRangePrice(productRange) > 0" class="range-price">
                                
                                <strong>{{ formatPrice(getRangePrice(productRange)) }}</strong>
                            </div>
                            <div class="range-actions">
                                <button type="button" class="range-button range-add-button"
                                    @click="addRangeToCart(productRange)">
                                    <i class="fa-solid fa-cart-plus"></i>
                                    Ajouter au panier
                                </button>
                                <button type="button" class="range-button range-order-button"
                                    @click="orderRangeDirectly(productRange)">
                                    Commander directement
                                    <i class="fa-solid fa-arrow-right"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </section>
                <section v-if="rangeProducts.length > 0" class="related-section">
                    <div class="section-heading">
                        <span class="section-label">
                            <i class="fa-solid fa-layer-group"></i>
                            LA GAMME COMPLÈTE
                        </span>
                        <h2>
                            Les produits de la 
                            <span>{{ productRange?.name }}</span>
                        </h2>
                        <p>
                            Découvrez les autres produits de cette gamme et composez une routine complète adaptée à vos
                            besoins.
                        </p>
                    </div>
                    <div class="products-grid">
                        <article v-for="item in rangeProducts" :key="item.id" class="product-card">
                            <div class="product-card-image">
                                <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                    <img v-if="item.main_image" :src="getProductImage(item.main_image)"
                                        :alt="item.name">
                                    <div v-else class="card-no-image">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                </RouterLink>
                                <span v-if="item.is_on_sale" class="card-sale">PROMO</span>
                            </div>
                            <div class="product-card-content">
                                <span class="card-category">{{ item.subcategory_name }}</span>
                                <h3>
                                    <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                        {{ item.name }}
                                    </RouterLink>
                                </h3>
                                <div class="card-price">
                                    <strong :class="{ sale: item.is_on_sale }">
                                        {{ formatPrice(getProductPrice(item)) }}
                                    </strong>
                                    <span v-if="item.is_on_sale">
                                        {{ formatPrice(item.price) }}
                                    </span>
                                </div>
                                <button type="button" class="card-cart-button" :disabled="Number(item.stock) <= 0"
                                    @click="addToCart(item)">
                                    <i class="fa-solid fa-cart-shopping"></i>
                                    Ajouter au panier
                                </button>
                            </div>
                        </article>
                    </div>
                </section>
                <section v-if="relatedProducts.length > 0" class="related-section">
                    <div class="section-heading">
                        <h2>
                            Découvrez aussi d'autres produits de
                            <span>{{ product.subcategory_name }}</span>
                        </h2>
                        <p>
                            N'hesitez pas à passer votre commande
                        </p>
                    </div>
                    <div class="products-grid">
                        <article v-for="item in relatedProducts" :key="item.id" class="product-card">
                            <div class="product-card-image">
                                <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                    <img v-if="item.main_image" :src="getProductImage(item.main_image)"
                                        :alt="item.name">
                                    <div v-else class="card-no-image">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                </RouterLink>
                                <span v-if="item.is_on_sale" class="card-sale">PROMO</span>
                            </div>
                            <div class="product-card-content">
                                <span class="card-category">{{ item.category_name }}</span>
                                <span class="card-subcategory">{{ item.subcategory_name }}</span>
                                <h3>
                                    <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                        {{ item.name }}
                                    </RouterLink>
                                </h3>
                                <div class="card-price">
                                    <strong :class="{ sale: item.is_on_sale }">
                                        {{ formatPrice(getProductPrice(item)) }}
                                    </strong>
                                    <span v-if="item.is_on_sale">
                                        {{ formatPrice(item.price) }}
                                    </span>
                                </div>
                                <button type="button" class="card-cart-button" :disabled="Number(item.stock) <= 0"
                                    @click="addToCart(item)">
                                    <i class="fa-solid fa-cart-shopping"></i>
                                    Ajouter au panier
                                </button>
                            </div>
                        </article>
                    </div>
                </section>
                <section v-if="categoryProducts.length > 0" class="related-section">
                    <div class="section-heading">
                        <h2>
                            Découvrez également notre sélection
                            <span>{{ product.category_name }}</span>
                        </h2>
                        <p>
                            .
                        </p>
                    </div>
                    <div class="products-grid">
                        <article v-for="item in categoryProducts" :key="item.id" class="product-card">
                            <div class="product-card-image">
                                <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                    <img v-if="item.main_image" :src="getProductImage(item.main_image)"
                                        :alt="item.name">
                                    <div v-else class="card-no-image">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                </RouterLink>
                                <span v-if="item.is_on_sale" class="card-sale">PROMO</span>
                            </div>
                            <div class="product-card-content">
                                <span class="card-category">{{ item.category_name }}</span>
                                <span class="card-subcategory">{{ item.subcategory_name }}</span>
                                <h3>
                                    <RouterLink :to="{ path: '/produit', query: { slug: item.slug } }">
                                        {{ item.name }}
                                    </RouterLink>
                                </h3>
                                <div class="card-price">
                                    <strong :class="{ sale: item.is_on_sale }">
                                        {{ formatPrice(getProductPrice(item)) }}
                                    </strong>
                                    <span v-if="item.is_on_sale">
                                        {{ formatPrice(item.price) }}
                                    </span>
                                </div>
                                <button type="button" class="card-cart-button" :disabled="Number(item.stock) <= 0"
                                    @click="addToCart(item)">
                                    <i class="fa-solid fa-cart-shopping"></i>
                                    Ajouter au panier
                                </button>
                            </div>
                        </article>
                    </div>
                </section>
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
                                        <img v-if="item.image" :src="item.image" :alt="item.name">
                                        <div v-else class="cart-no-image">
                                            <i class="fa-solid fa-image"></i>
                                        </div>
                                    </div>
                                    <div class="cart-item-info">
                                        <h4>{{ item.name }}</h4>
                                        <strong class="cart-item-price">
                                            {{ formatPrice(item.price) }}
                                        </strong>
                                        <div class="cart-item-bottom">
                                            <div class="cart-quantity">
                                                <button type="button" @click="decreaseCartQuantity(item)"
                                                    :disabled="item.quantity <= 1">
                                                    <i class="fa-solid fa-minus"></i>
                                                </button>
                                                <span>{{ item.quantity }}</span>
                                                <button type="button" @click="increaseCartQuantity(item)"
                                                    :disabled="item.quantity >= item.stock">
                                                    <i class="fa-solid fa-plus"></i>
                                                </button>
                                            </div>
                                            <strong class="cart-item-total">
                                                {{ formatPrice(getItemTotal(item)) }}
                                            </strong>
                                        </div>
                                    </div>
                                    <button type="button" class="remove-cart-item" title="Supprimer"
                                        @click="removeFromCart(item)">
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
                                    <span class="delivery-free">À confirmer</span>
                                </div>
                                <div class="summary-total">
                                    <span>Total</span>
                                    <strong>{{ formatPrice(cartTotal) }}</strong>
                                </div>
                            </div>
                            <div class="cart-footer-actions">
                                <button type="button" class="clear-cart-button" @click="clearCart">
                                    <i class="fa-solid fa-trash"></i>
                                    Vider
                                </button>
                                <RouterLink to="/panier" class="checkout-button" @click="closeCart">
                                    <i class="fa-solid fa-arrow-right"></i>
                                    Acheter directement
                                </RouterLink>
                            </div>
                        </div>
                    </template>
                </aside>
            </Transition>
        </div>
    </Transition>
</template>

<style scoped>
.product-details-section {
    width: 100%;
    padding: 40px 0 90px;
    background: #fff
}

.breadcrumb {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 30px;
    font-size: 12px;
    color: #999
}

.breadcrumb a {
    color: #777;
    text-decoration: none
}

.breadcrumb a:hover {
    color: #38B04C
}

.breadcrumb i {
    font-size: 8px;
    color: #bbb
}

.breadcrumb span {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis
}

.product-main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 55px;
    align-items: start
}

.product-gallery {
    min-width: 0
}

.main-image-container {
    height: 460px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    background: #fff
}

.main-product-image {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: contain;
    padding: 25px;
    background: #fff;
    transition: transform .4s ease
}

.main-image-container:hover .main-product-image {
    transform: scale(1.03)
}

.sale-badge {
    position: absolute;
    top: 18px;
    left: 18px;
    z-index: 4;
    padding: 7px 12px;
    border-radius: 3px;
    background: #38B04C;
    color: #fff;
    font-size: 10px;
    font-weight: 700
}

.no-image {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    height: 100%;
    color: #aaa
}

.no-image i {
    font-size: 45px
}

.product-thumbnails {
    display: flex;
    gap: 13px;
    margin-top: 14px;
    overflow-x: auto;
    padding: 3px
}

.thumbnail {
    width: 78px;
    height: 78px;
    flex-shrink: 0;
    padding: 4px;
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    background: #fff;
    cursor: pointer;
    transition: .25s ease
}

.thumbnail:hover {
    border-color: #38B04C;
    transform: translateY(-2px)
}

.thumbnail.active {
    border: 2px solid #38B04C
}

.thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: contain
}

.product-information {
    min-width: 0;
    padding-top: 3px
}

.top-product-line {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px
}

.product-category {
    display: block;
    margin-bottom: 4px;
    color: #38B04C;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase
}

.product-subcategory {
    display: block;
    margin-bottom: 9px;
    color: #999;
    font-size: 10px
}

.product-title {
    margin: 0 0 7px;
    color: #202020;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 36px;
    font-weight: 500;
    line-height: 1.15
}

.product-reference {
    color: #999;
    font-size: 11px
}

.favorite-button {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid #eee;
    border-radius: 50%;
    background: #fff;
    color: #38B04C;
    cursor: pointer;
    transition: .25s ease
}

.favorite-button:hover {
    background: #38B04C;
    color: #fff
}

.rating-row {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-top: 18px;
    color: #999;
    font-size: 11px
}

.product-rating {
    display: flex;
    gap: 3px
}

.product-rating i {
    color: #38B04C;
    font-size: 11px
}

.rating-separator {
    color: #ccc
}

.price-row {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-top: 21px
}

.price-row strong {
    color: #202020;
    font-size: 27px;
    font-weight: 700
}

.price-row strong.sale {
    color: #38B04C
}

.old-price {
    color: #999;
    font-size: 14px;
    text-decoration: line-through
}

.discount {
    padding: 5px 8px;
    border-radius: 3px;
    background: #eef8f0;
    color: #38B04C;
    font-size: 9px;
    font-weight: 700
}

.stock {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 15px;
    color: #555;
    font-size: 12px
}

.stock>span:first-child {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #38B04C
}

.stock>span:first-child.unavailable {
    background: #d9534f
}

.customer-message {
    display: flex;
    gap: 13px;
    margin-top: 22px;
    padding: 16px;
    border-left: 3px solid #38B04C;
    background: #f6fbf7
}

.customer-message-icon {
    width: 34px;
    height: 34px;
    min-width: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #38B04C;
    color: #fff
}

.customer-message-icon i {
    font-size: 13px
}

.customer-message strong {
    color: #333;
    font-size: 12px;
    font-weight: 700
}

.customer-message p {
    margin: 6px 0 0;
    color: #777;
    font-size: 11px;
    line-height: 1.7
}

.customer-message p strong {
    color: #38B04C;
    font-size: 11px
}

.product-summary {
    margin: 21px 0 0;
    color: #666;
    font-size: 13px;
    line-height: 1.8
}

.purchase-title {
    margin-top: 25px;
    margin-bottom: 9px;
    color: #333;
    font-size: 12px;
    font-weight: 600
}

.purchase-row {
    display: flex;
    align-items: center;
    gap: 10px
}

.quantity-selector {
    height: 43px;
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
    background: #fff
}

.quantity-selector button {
    width: 34px;
    height: 100%;
    border: 0;
    background: #fff;
    color: #444;
    cursor: pointer
}

.quantity-selector button:hover:not(:disabled) {
    background: #38B04C;
    color: #fff
}

.quantity-selector button:disabled {
    opacity: .35;
    cursor: not-allowed
}

.quantity-selector span {
    width: 38px;
    text-align: center;
    color: #333;
    font-size: 13px;
    font-weight: 600
}

.add-cart-button {
    height: 43px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border: 1px solid #38B04C;
    border-radius: 5px;
    background: #38B04C;
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: .25s ease
}

.add-cart-button:hover:not(:disabled) {
    background: #2f963f
}

.add-cart-button:disabled {
    opacity: .4;
    cursor: not-allowed
}

.buy-now-button {
    width: 100%;
    height: 43px;
    margin-top: 9px;
    border: 0;
    border-radius: 5px;
    background: #202020;
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: .25s ease
}

.buy-now-button:hover:not(:disabled) {
    background: #38B04C
}

.buy-now-button:disabled {
    opacity: .4;
    cursor: not-allowed
}

.delivery-info {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #eee
}

.delivery-info>i {
    color: #38B04C;
    font-size: 17px
}

.delivery-info div {
    display: flex;
    flex-direction: column;
    gap: 4px
}

.delivery-info strong {
    color: #444;
    font-size: 11px
}

.delivery-info span {
    color: #999;
    font-size: 10px
}

.product-mini-info {
    display: flex;
    gap: 28px;
    margin-top: 17px
}

.product-mini-info div {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #999;
    font-size: 10px
}

.product-mini-info i {
    color: #38B04C;
    font-size: 13px
}

.details-section {
    margin-top: 65px
}

.details-tabs {
    display: flex;
    align-items: center;
    gap: 35px;
    border-bottom: 1px solid #eee
}

.details-tabs button {
    position: relative;
    padding: 0 0 14px;
    border: 0;
    background: none;
    color: #777;
    font-size: 12px;
    cursor: pointer
}

.details-tabs button.active {
    color: #38B04C;
    font-weight: 600
}

.details-tabs button.active::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: -1px;
    height: 2px;
    background: #38B04C
}

.details-content {
    padding: 28px 5px 0;
    max-width: 900px
}

.details-content h3 {
    margin: 0 0 12px;
    color: #333;
    font-size: 16px;
    font-weight: 600
}

.details-content p {
    margin: 0;
    color: #666;
    font-size: 12px;
    line-height: 1.9;
    white-space: pre-line
}

.empty-detail {
    color: #aaa !important
}

.range-section,
.related-section {
    margin-top: 70px
}

.range-heading {
    margin-bottom: 23px
}

.range-section{margin-top:70px}
.range-heading{margin-bottom:25px}
.range-small-title{display:flex;align-items:center;gap:7px;margin-bottom:10px;color:#38B04C;font-size:10px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase}
.range-heading h2{margin:0;color:#202020;font-family:Georgia,"Times New Roman",serif;font-size:32px;font-weight:500}
.range-heading h2 span{color:#38B04C}
.range-heading p{margin:9px 0 0;color:#777;font-size:12px;line-height:1.7}
.range-presentation{width:100%;min-height:330px;display:flex;align-items:center;position:relative;overflow:hidden;background-color:#557f30;background-size:48% auto;background-position:right center;background-repeat:no-repeat;border-radius:2px}
.range-overlay{position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(20,40,10,.82) 0%,rgba(20,40,10,.68) 32%,rgba(20,40,10,.38) 52%,rgba(20,40,10,.08) 72%,rgba(20,40,10,0) 100%)}
.range-content{width:52%;padding:45px 30px 45px 45px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;position:relative;z-index:3}
.range-label{margin-bottom:10px;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.8px;text-transform:uppercase}
.range-content h3{margin:0 0 15px;color:#fff;font-family:Georgia,"Times New Roman",serif;font-size:40px;font-weight:500;line-height:1.1}
.range-description{max-width:430px;margin:0 0 18px;color:rgba(255,255,255,.92);font-size:14px;line-height:1.7}
.range-price{display:flex;align-items:baseline;gap:9px;margin-bottom:20px}
.range-price span{color:rgba(255,255,255,.82);font-size:11px}
.range-price strong{color:#fff;font-size:18px;font-weight:700}
.range-actions{display:flex;align-items:center;flex-wrap:wrap;gap:10px}
.range-button{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:40px;padding:11px 16px;border:1px solid transparent;border-radius:5px;font-size:10.5px;font-weight:700;cursor:pointer;transition:background .25s ease,color .25s ease,border-color .25s ease,transform .25s ease}
.range-add-button{background:#38B04C;border-color:#38B04C;color:#fff}
.range-add-button:hover{background:#2f963f;border-color:#2f963f;transform:translateY(-2px)}
.range-order-button{background:#fff;border-color:#fff;color:#202020}
.range-order-button:hover{background:#202020;border-color:#202020;color:#fff;transform:translateY(-2px)}
.range-button i{font-size:10px}
.range-add-button:hover i{transform:translateY(-1px)}
.range-order-button:hover i{transform:translateX(3px)}
@media(max-width:991px){
.range-presentation{min-height:300px;background-size:45% auto}
.range-content{width:60%;padding:35px 25px 35px 30px}
.range-content h3{font-size:34px}
}
@media(max-width:576px){
.range-section{margin-top:50px}
.range-heading h2{font-size:25px}
.range-presentation{min-height:455px;background-size:72% auto;background-position:right 20px;align-items:flex-end}
.range-overlay{background:linear-gradient(180deg,rgba(20,40,10,.05) 0%,rgba(20,40,10,.25) 28%,rgba(20,40,10,.72) 58%,rgba(20,40,10,.9) 100%)}
.range-content{width:100%;min-height:260px;padding:25px 22px;justify-content:flex-end}
.range-content h3{font-size:30px}
.range-description{max-width:100%;font-size:12px}
.range-actions{width:100%;flex-direction:column;align-items:stretch}
.range-button{width:100%}
}
.range-small-title,
.section-label {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 10px;
    color: #38B04C;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px
}

.range-heading h2,
.section-heading h2 {
    margin: 0;
    color: #202020;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 32px;
    font-weight: 500
}

.range-heading h2 span,
.section-heading h2 span {
    color: #38B04C
}

.range-presentation {
    width: 100%;
    min-height: 360px;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    background-color: #557f30;
    background-size: 48% auto;
    background-position: right center;
    background-repeat: no-repeat;
    border-radius: 3px
}

.range-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(20, 40, 10, .82), rgba(20, 40, 10, .5) 45%, rgba(20, 40, 10, 0) 100%)
}

.range-content {
    width: 55%;
    padding: 45px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    position: relative;
    z-index: 2
}

.range-label {
    margin-bottom: 10px;
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.8px
}

.range-content h3 {
    margin: 0 0 15px;
    color: #fff;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 40px;
    font-weight: 500
}

.range-description {
    max-width: 520px;
    margin: 0;
    color: rgba(255, 255, 255, .94);
    font-size: 13px;
    line-height: 1.7
}

.range-price {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 20px
}

.range-price strong {
    color: #fff;
    font-size: 25px;
    font-weight: 700
}

.range-price span {
    color: rgba(255, 255, 255, .65);
    font-size: 13px;
    text-decoration: line-through
}

.range-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 16px
}

.range-cart-button {
    height: 42px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 0 17px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: .25s ease
}

.range-cart-add-button {
    border: 1px solid #38B04C;
    background: #38B04C;
    color: #fff
}

.range-cart-add-button:hover:not(:disabled) {
    background: #2f963f
}

.range-cart-add-button:disabled {
    opacity: .45;
    cursor: not-allowed
}

.range-cart-buy-button {
    border: 1px solid rgba(255, 255, 255, .85);
    background: #fff;
    color: #202020
}

.range-cart-buy-button:hover:not(:disabled) {
    background: #38B04C;
    border-color: #38B04C;
    color: #fff
}

.range-cart-buy-button:disabled {
    opacity: .45;
    cursor: not-allowed
}

.section-heading {
    margin-bottom: 25px
}

.section-heading p {
    max-width: 650px;
    margin: 9px 0 0;
    color: #777;
    font-size: 12px;
    line-height: 1.7
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 17px
}

.product-card {
    overflow: hidden;
    border: 1px solid #eee;
    border-radius: 7px;
    background: #fff;
    transition: .3s ease
}

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, .07)
}

.product-card-image {
    height: 220px;
    position: relative;
    overflow: hidden;
    background: #fff
}

.product-card-image a {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center
}

.product-card-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 12px;
    transition: .4s ease
}

.product-card:hover .product-card-image img {
    transform: scale(1.05)
}

.card-no-image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #aaa
}

.card-no-image i {
    font-size: 35px
}

.card-sale {
    position: absolute;
    top: 9px;
    left: 9px;
    padding: 5px 7px;
    border-radius: 3px;
    background: #38B04C;
    color: #fff;
    font-size: 8px;
    font-weight: 700
}

.product-card-content {
    padding: 13px
}

.card-category {
    display: block;
    margin-bottom: 4px;
    color: #38B04C;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase
}

.card-subcategory {
    display: block;
    margin-bottom: 7px;
    color: #999;
    font-size: 8px
}

.product-card-content h3 {
    height: 37px;
    margin: 0 0 8px;
    overflow: hidden
}

.product-card-content h3 a {
    color: #222;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none
}

.product-card-content h3 a:hover {
    color: #38B04C
}

.card-price {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 11px
}

.card-price strong {
    color: #222;
    font-size: 12px;
    font-weight: 700
}

.card-price strong.sale {
    color: #38B04C
}

.card-price span {
    color: #aaa;
    font-size: 8px;
    text-decoration: line-through
}

.card-cart-button {
    width: 100%;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    border: 0;
    border-radius: 4px;
    background: #38B04C;
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    cursor: pointer
}

.card-cart-button:hover:not(:disabled) {
    background: #2f963f
}

.card-cart-button:disabled {
    opacity: .4;
    cursor: not-allowed
}

.product-loading {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 55px
}

.loading-image {
    height: 460px;
    border-radius: 8px;
    background: linear-gradient(90deg, #f4f4f4 25%, #fff 50%, #f4f4f4 75%);
    background-size: 200% 100%;
    animation: loadingAnimation 1.5s infinite
}

.loading-content {
    padding-top: 20px
}

.loading-line {
    height: 14px;
    margin-bottom: 16px;
    border-radius: 4px;
    background: linear-gradient(90deg, #f4f4f4 25%, #fff 50%, #f4f4f4 75%);
    background-size: 200% 100%;
    animation: loadingAnimation 1.5s infinite
}

.loading-line.small {
    width: 25%
}

.loading-line.large {
    width: 75%;
    height: 36px
}

.loading-line.medium {
    width: 50%
}

.loading-line.price {
    width: 30%;
    height: 28px;
    margin-top: 25px
}

.loading-line.button {
    width: 60%;
    height: 43px;
    margin-top: 20px
}

@keyframes loadingAnimation {
    0% {
        background-position: 200% 0
    }

    100% {
        background-position: -200% 0
    }
}

.product-error {
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 11px;
    text-align: center
}

.product-error i {
    color: #38B04C;
    font-size: 40px
}

.product-error h2 {
    margin: 5px 0 0;
    color: #202020;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 32px;
    font-weight: 500
}

.product-error p {
    margin: 0;
    color: #888;
    font-size: 12px
}

.back-shop-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 11px;
    padding: 10px 17px;
    border-radius: 5px;
    background: #38B04C;
    color: #fff;
    font-size: 11px;
    text-decoration: none
}

.cart-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    justify-content: flex-end;
    background: rgba(0, 0, 0, .45);
    backdrop-filter: blur(2px)
}

.cart-panel {
    width: 430px;
    max-width: 95vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #fff;
    box-shadow: -10px 0 35px rgba(0, 0, 0, .15)
}

.cart-header {
    height: 76px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 22px;
    border-bottom: 1px solid #eee;
    flex-shrink: 0
}

.cart-header-title {
    display: flex;
    align-items: center;
    gap: 11px
}

.cart-icon {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #eef8f0;
    color: #38B04C
}

.cart-icon i {
    font-size: 14px
}

.cart-header h3 {
    margin: 0;
    color: #202020;
    font-size: 16px;
    font-weight: 600
}

.cart-header span {
    display: block;
    margin-top: 3px;
    color: #999;
    font-size: 10px
}

.cart-close-button {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0;
    border-radius: 50%;
    background: #f6f6f6;
    color: #555;
    cursor: pointer
}

.cart-close-button:hover {
    background: #38B04C;
    color: #fff
}

.cart-content {
    flex: 1;
    overflow-y: auto;
    padding: 15px 20px
}

.cart-products {
    display: flex;
    flex-direction: column;
    gap: 12px
}

.cart-item {
    position: relative;
    display: flex;
    gap: 11px;
    padding: 11px;
    border: 1px solid #eee;
    border-radius: 7px;
    background: #fff
}

.cart-item-image {
    width: 70px;
    height: 75px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    background: #f8faf8;
    overflow: hidden
}

.cart-item-image img {
    width: 100%;
    height: 100%;
    object-fit: contain
}

.cart-no-image {
    color: #aaa;
    font-size: 20px
}

.cart-item-info {
    min-width: 0;
    flex: 1;
    padding-right: 18px
}

.cart-item-info h4 {
    margin: 0 0 5px;
    color: #333;
    font-size: 11px;
    font-weight: 600;
    line-height: 1.4
}

.cart-item-price {
    display: block;
    color: #38B04C;
    font-size: 10px
}

.cart-item-bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 9px
}

.cart-quantity {
    height: 28px;
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden
}

.cart-quantity button {
    width: 27px;
    height: 100%;
    border: 0;
    background: #fff;
    color: #555;
    cursor: pointer
}

.cart-quantity button:hover:not(:disabled) {
    background: #38B04C;
    color: #fff
}

.cart-quantity button:disabled {
    opacity: .3;
    cursor: not-allowed
}

.cart-quantity span {
    width: 28px;
    text-align: center;
    color: #333;
    font-size: 10px;
    font-weight: 600
}

.cart-item-total {
    color: #202020;
    font-size: 10px
}

.remove-cart-item {
    position: absolute;
    top: 9px;
    right: 9px;
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0;
    background: transparent;
    color: #aaa;
    cursor: pointer
}

.remove-cart-item:hover {
    color: #d9534f
}

.remove-cart-item i {
    font-size: 10px
}

.cart-footer {
    padding: 17px 20px;
    border-top: 1px solid #eee;
    background: #fff;
    flex-shrink: 0
}

.cart-summary {
    display: flex;
    flex-direction: column;
    gap: 9px
}

.summary-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #777;
    font-size: 11px
}

.summary-line strong {
    color: #333;
    font-size: 11px
}

.delivery-free {
    color: #999
}

.summary-total {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 11px;
    margin-top: 3px;
    border-top: 1px solid #eee;
    color: #222;
    font-size: 13px;
    font-weight: 600
}

.summary-total strong {
    color: #38B04C;
    font-size: 15px
}

.cart-footer-actions {
    display: flex;
    gap: 8px;
    margin-top: 13px
}

.clear-cart-button {
    height: 40px;
    padding: 0 14px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #fff;
    color: #777;
    font-size: 10px;
    cursor: pointer
}

.clear-cart-button:hover {
    border-color: #d9534f;
    color: #d9534f
}

.checkout-button {
    height: 40px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    border-radius: 5px;
    background: #38B04C;
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    text-decoration: none
}

.checkout-button:hover {
    background: #2f963f;
    color: #fff
}

.empty-cart {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px;
    text-align: center
}

.empty-cart-icon {
    width: 70px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #f3f9f4;
    color: #38B04C
}

.empty-cart-icon i {
    font-size: 25px
}

.empty-cart h3 {
    margin: 18px 0 7px;
    color: #333;
    font-size: 15px
}

.empty-cart p {
    max-width: 250px;
    margin: 0;
    color: #999;
    font-size: 10px;
    line-height: 1.7
}

.continue-shopping-button {
    margin-top: 18px;
    height: 38px;
    padding: 0 15px;
    display: flex;
    align-items: center;
    gap: 7px;
    border: 0;
    border-radius: 5px;
    background: #38B04C;
    color: #fff;
    font-size: 10px;
    cursor: pointer
}

.continue-shopping-button:hover {
    background: #2f963f
}

.cart-fade-enter-active,
.cart-fade-leave-active {
    transition: opacity .25s ease
}

.cart-fade-enter-from,
.cart-fade-leave-to {
    opacity: 0
}

.cart-slide-enter-active,
.cart-slide-leave-active {
    transition: transform .3s ease
}

.cart-slide-enter-from,
.cart-slide-leave-to {
    transform: translateX(100%)
}

@media(max-width:991px) {

    .product-main,
    .product-loading {
        grid-template-columns: 1fr;
        gap: 40px
    }

    .products-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr))
    }

    .range-content {
        width: 62%;
        padding: 35px 25px 35px 30px
    }
}

@media(max-width:768px) {
    .product-details-section {
        padding: 30px 0 65px
    }

    .main-image-container,
    .loading-image {
        height: 390px
    }

    .product-title {
        font-size: 30px
    }

    .range-presentation {
        min-height: 500px;
        background-size: 72% auto;
        background-position: right 20px;
        align-items: flex-end
    }

    .range-overlay {
        background: linear-gradient(180deg, rgba(20, 40, 10, .05), rgba(20, 40, 10, .3) 35%, rgba(20, 40, 10, .9) 100%)
    }

    .range-content {
        width: 100%;
        min-height: 315px;
        padding: 25px 22px;
        justify-content: flex-end
    }

    .range-content h3 {
        font-size: 30px
    }

    .range-description {
        font-size: 12px
    }

    .range-actions {
        width: 100%;
        flex-direction: column;
        align-items: stretch
    }

    .range-cart-button {
        width: 100%
    }

    .products-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr))
    }

    .section-heading h2 {
        font-size: 28px
    }

    .cart-panel {
        width: 400px
    }
}

@media(max-width:576px) {
    .product-main {
        gap: 28px
    }

    .main-image-container,
    .loading-image {
        height: 320px
    }

    .product-title {
        font-size: 27px
    }

    .product-thumbnails {
        gap: 8px
    }

    .thumbnail {
        width: 62px;
        height: 62px
    }

    .price-row strong {
        font-size: 24px
    }

    .product-summary {
        font-size: 12px
    }

    .customer-message {
        padding: 13px
    }

    .customer-message p {
        font-size: 10px
    }

    .purchase-row {
        gap: 6px
    }

    .add-cart-button {
        font-size: 10px;
        padding: 0 8px
    }

    .product-mini-info {
        gap: 14px
    }

    .details-section {
        margin-top: 48px
    }

    .details-tabs {
        gap: 22px;
        overflow-x: auto
    }

    .details-tabs button {
        font-size: 10px;
        white-space: nowrap
    }

    .range-section,
    .related-section {
        margin-top: 50px
    }

    .range-heading h2,
    .section-heading h2 {
        font-size: 25px
    }

    .range-presentation {
        min-height: 510px;
        background-size: 75% auto
    }

    .range-content {
        min-height: 320px;
        padding: 22px
    }

    .range-content h3 {
        font-size: 29px
    }

    .range-description {
        font-size: 11px
    }

    .range-price strong {
        font-size: 22px
    }

    .range-actions {
        gap: 8px
    }

    .products-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px
    }

    .product-card-image {
        height: 165px
    }

    .product-card-content {
        padding: 9px
    }

    .product-card-content h3 a {
        font-size: 13px
    }

    .card-cart-button {
        height: 34px;
        font-size: 9px
    }

    .cart-panel {
        width: 100%;
        max-width: 100%
    }

    .cart-header {
        height: 68px;
        padding: 0 16px
    }

    .cart-content {
        padding: 12px
    }

    .cart-footer {
        padding: 14px 12px
    }
}
</style>