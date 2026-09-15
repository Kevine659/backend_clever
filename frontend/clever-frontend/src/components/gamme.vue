<script setup>
import {ref,onMounted,onUnmounted,computed} from "vue"
import {useRouter} from "vue-router"
import api from "../services/api"
const router=useRouter()
const productRanges=ref([])
const loading=ref(true)
const error=ref(false)
const currentSlide=ref(0)
const cart=ref([])
const showCart=ref(false)
let autoSlideInterval=null
let touchStartX=0
let touchEndX=0
const getRangeImage=(image)=>{
    if(!image||typeof image!=="string")return null
    image=image.trim()
    if(!image)return null
    if(image.startsWith("http://")||image.startsWith("https://"))return image
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
const getRangePrice=(range)=>{
    if(!range)return 0
    const price=
        range.current_price??
        range.promotional_price??
        range.price??
        0
    return Number(price)||0
}
const loadProductRanges=async()=>{
    try{
        loading.value=true
        error.value=false
        const response=await api.get("/products/product-ranges/")
        const data=response.data?.results||response.data||[]
        productRanges.value=Array.isArray(data)
            ?data.filter(range=>range&&range.is_active!==false)
            :[]
        if(currentSlide.value>=productRanges.value.length){
            currentSlide.value=0
        }
    }catch(err){
        console.error("Erreur lors du chargement des gammes :",err)
        error.value=true
        productRanges.value=[]
    }finally{
        loading.value=false
    }
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
const normalizeLocalCartItem=(item)=>{
    if(!item)return null
    if(
        item.type==="range"||
        item.item_type==="range"||
        item.range_id!==undefined||
        item.product_range_id!==undefined
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
    }catch(err){
        console.error("Erreur sauvegarde panier :",err)
    }
}
const loadCart=()=>{
    try{
        const savedCart=localStorage.getItem("shop_cart")
        if(!savedCart){
            cart.value=[]
            return
        }
        const parsed=JSON.parse(savedCart)
        if(!Array.isArray(parsed)){
            cart.value=[]
            return
        }
        cart.value=parsed
            .map(normalizeLocalCartItem)
            .filter(Boolean)
        saveCart()
        console.log("Panier local chargé depuis Gamme.vue :",cart.value)
    }catch(err){
        console.error("Erreur lors du chargement du panier :",err)
        cart.value=[]
    }
}
const addRangeToCart=(range)=>{
    if(!range||!range.id)return
    const rangeId=Number(range.id)
    if(!rangeId||Number.isNaN(rangeId))return
    const existing=cart.value.find(
        item=>
            item.type==="range"&&
            Number(item.range_id)===rangeId
    )
    if(existing){
        existing.quantity=Number(existing.quantity||0)+1
    }else{
        cart.value.push({
            type:"range",
            item_type:"range",
            range_id:rangeId,
            product_range:rangeId,
            id:`range_${rangeId}`,
            name:range.name||"Gamme",
            slug:range.slug||"",
            image:range.image?getRangeImage(range.image):null,
            price:getRangePrice(range),
            stock:0,
            quantity:1
        })
    }
    saveCart()
    console.log("Après ajout de la gamme :",cart.value)
    showCart.value=true
}
const orderRangeDirectly=(range)=>{
    if(!range||!range.id)return
    const rangeId=Number(range.id)
    if(!rangeId||Number.isNaN(rangeId))return
    const existing=cart.value.find(
        item=>
            item.type==="range"&&
            Number(item.range_id)===rangeId
    )
    if(existing){
        existing.quantity=Number(existing.quantity||0)+1
    }else{
        cart.value.push({
            type:"range",
            item_type:"range",
            range_id:rangeId,
            product_range:rangeId,
            id:`range_${rangeId}`,
            name:range.name||"Gamme",
            slug:range.slug||"",
            image:range.image?getRangeImage(range.image):null,
            price:getRangePrice(range),
            stock:0,
            quantity:1
        })
    }
    saveCart()
    console.log("Commande directe gamme :",cart.value)
    router.push("/panier")
}
const increaseCartQuantity=(item)=>{
    if(!item)return
    if(
        item.type==="product"&&
        Number(item.stock)>0&&
        Number(item.quantity)>=Number(item.stock)
    )return
    item.quantity=Number(item.quantity||0)+1
    saveCart()
}
const decreaseCartQuantity=(item)=>{
    if(!item)return
    const quantity=Number(item.quantity||0)
    if(quantity<=1)return
    item.quantity=quantity-1
    saveCart()
}
const removeFromCart=(item)=>{
    if(!item)return
    const key=
        item.type==="range"
            ?getRangeCartKey(item)
            :getProductCartKey(item)
    if(!key)return
    cart.value=cart.value.filter(current=>{
        const currentKey=
            current.type==="range"
                ?getRangeCartKey(current)
                :getProductCartKey(current)
        return currentKey!==key
    })
    saveCart()
}
const clearCart=()=>{
    cart.value=[]
    saveCart()
}
const cartItemsCount=computed(()=>{
    return cart.value.reduce(
        (total,item)=>{
            return total+Number(item.quantity||0)
        },
        0
    )
})
const cartTotal=computed(()=>{
    return cart.value.reduce(
        (total,item)=>{
            return total+
                Number(item.price||0)*
                Number(item.quantity||0)
        },
        0
    )
})
const getItemTotal=(item)=>{
    return Number(item.price||0)*
        Number(item.quantity||0)
}
const closeCart=()=>{
    showCart.value=false
}
const nextSlide=()=>{
    if(productRanges.value.length<2)return
    currentSlide.value=(
        currentSlide.value+1
    )%productRanges.value.length
}
const previousSlide=()=>{
    if(productRanges.value.length<2)return
    currentSlide.value=(
        currentSlide.value-1+
        productRanges.value.length
    )%productRanges.value.length
}
const goToSlide=(index)=>{
    if(
        index<0||
        index>=productRanges.value.length
    )return
    currentSlide.value=index
    startAutoSlide()
}
const startAutoSlide=()=>{
    stopAutoSlide()
    if(productRanges.value.length>1){
        autoSlideInterval=setInterval(()=>{
            nextSlide()
        },5000)
    }
}
const stopAutoSlide=()=>{
    if(autoSlideInterval){
        clearInterval(autoSlideInterval)
        autoSlideInterval=null
    }
}
const handleTouchStart=(event)=>{
    touchStartX=event.changedTouches[0].screenX
}
const handleTouchEnd=(event)=>{
    touchEndX=event.changedTouches[0].screenX
    const distance=touchStartX-touchEndX
    if(Math.abs(distance)>50){
        if(distance>0){
            nextSlide()
        }else{
            previousSlide()
        }
        startAutoSlide()
    }
}
onMounted(async()=>{
    loadCart()
    await loadProductRanges()
    startAutoSlide()
})
onUnmounted(()=>{
    stopAutoSlide()
})
</script>
<template>
<section class="ranges-section">
<div class="container">
<div class="ranges-header">
<div>
<span class="ranges-small-title">
<i class="fa-solid fa-layer-group"></i>
DECOUVREZ
</span>
<h2>
nos meilleures 
<span>gammes et packs de produits</span>
</h2>
</div>
<p>
Des produits soigneusement sélectionnés pour répondre à vos besoins.
</p>
</div>
<div v-if="loading" class="range-banner-skeleton">
<div class="skeleton-content"></div>
<div class="skeleton-image"></div>
</div>
<div v-else-if="error" class="ranges-error">
<i class="fa-solid fa-circle-exclamation"></i>
<p>Impossible de charger les gammes de produits.</p>
<button type="button" @click="loadProductRanges">
Réessayer
</button>
</div>
<div v-else-if="productRanges.length>0" class="ranges-carousel-wrapper" @mouseenter="stopAutoSlide" @mouseleave="startAutoSlide" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
<div class="ranges-carousel">
<div class="ranges-track" :style="{transform:`translateX(-${currentSlide*100}%)`}">
<article
v-for="range in productRanges"
:key="range.id"
class="range-slide"
>
<div
class="range-slide-content"
:style="{
backgroundImage:range.image
?`url(${getRangeImage(range.image)})`
:'none'
}"
>
<div class="range-overlay"></div>
<div class="range-text">
<span class="range-label">
<i class="fa-solid fa-sparkles"></i>
OFFRES SPECIALES
</span>
<h3>{{ range.name }}</h3>
<p class="range-description">
{{ range.description||"Découvrez notre gamme de produits soigneusement sélectionnés pour prendre soin de vous." }}
</p>
<div class="range-price">
<span>À partir de</span>
<strong>{{ formatPrice(getRangePrice(range)) }}</strong>
</div>
<div class="range-actions">
<button
type="button"
class="range-button add-cart-button"
@click="addRangeToCart(range)"
>
<i class="fa-solid fa-cart-plus"></i>
Ajouter au panier
</button>
<button
type="button"
class="range-button order-button"
@click="orderRangeDirectly(range)"
>
Commander directement
<i class="fa-solid fa-arrow-right"></i>
</button>
</div>
</div>
</div>
</article>
</div>
</div>
<div v-if="productRanges.length>1" class="ranges-controls">
<button
type="button"
class="range-control"
@click="previousSlide"
aria-label="Gamme précédente"
>
<i class="fa-solid fa-arrow-left"></i>
</button>
<div class="range-dots">
<button
v-for="(range,index) in productRanges"
:key="range.id"
type="button"
class="range-dot"
:class="{active:currentSlide===index}"
:aria-label="`Afficher ${range.name}`"
@click="goToSlide(index)"
></button>
</div>
<button
type="button"
class="range-control"
@click="nextSlide"
aria-label="Gamme suivante"
>
<i class="fa-solid fa-arrow-right"></i>
</button>
</div>
</div>
<div v-else class="ranges-empty">
<i class="fa-solid fa-box-open"></i>
<p>Aucune gamme disponible pour le moment.</p>
</div>
</div>
</section>
<Transition name="cart-fade">
<div
v-if="showCart"
class="cart-overlay"
@click.self="closeCart"
>
<Transition name="cart-slide">
<aside
v-if="showCart"
class="cart-panel"
>
<div class="cart-header">
<div class="cart-header-title">
<div class="cart-icon">
<i class="fa-solid fa-cart-shopping"></i>
</div>
<div>
<h3>Mon panier</h3>
<span>
{{ cartItemsCount }}
{{ cartItemsCount>1?"articles":"article" }}
</span>
</div>
</div>
<button
type="button"
class="cart-close-button"
@click="closeCart"
>
<i class="fa-solid fa-xmark"></i>
</button>
</div>
<div
v-if="cart.length===0"
class="empty-cart"
>
<div class="empty-cart-icon">
<i class="fa-solid fa-cart-shopping"></i>
</div>
<h3>Votre panier est vide</h3>
<p>
Ajoutez vos produits préférés pour les retrouver ici.
</p>
<button
type="button"
class="continue-shopping-button"
@click="closeCart"
>
<i class="fa-solid fa-arrow-left"></i>
Continuer mes achats
</button>
</div>
<template v-else>
<div class="cart-content">
<div class="cart-products">
<div
v-for="item in cart"
:key="item.type==='range'?getRangeCartKey(item):getProductCartKey(item)"
class="cart-item"
>
<div class="cart-item-image">
<img
v-if="item.image"
:src="item.image"
:alt="item.name"
@error="$event.target.style.display='none'"
>
<div
v-else
class="cart-no-image"
>
<i class="fa-solid fa-image"></i>
</div>
</div>
<div class="cart-item-info">
<span class="cart-item-type">
{{ item.type==="range"?"GAMME":"PRODUIT" }}
</span>
<h4>{{ item.name }}</h4>
<strong class="cart-item-price">
{{ formatPrice(item.price) }}
</strong>
<div class="cart-item-bottom">
<div class="cart-quantity">
<button
type="button"
@click="decreaseCartQuantity(item)"
:disabled="item.quantity<=1"
>
<i class="fa-solid fa-minus"></i>
</button>
<span>{{ item.quantity }}</span>
<button
type="button"
@click="increaseCartQuantity(item)"
:disabled="item.type==='product'&&item.stock>0&&item.quantity>=item.stock"
>
<i class="fa-solid fa-plus"></i>
</button>
</div>
<strong class="cart-item-total">
{{ formatPrice(getItemTotal(item)) }}
</strong>
</div>
</div>
<button
type="button"
class="remove-cart-item"
title="Supprimer"
@click="removeFromCart(item)"
>
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
<RouterLink
to="/panier"
class="checkout-button"
@click="closeCart"
>
<i class="fa-solid fa-cart-shopping"></i>
Voir mon panier
</RouterLink>
<button
type="button"
class="continue-button"
@click="closeCart"
>
Continuer mes achats
</button>
<button
type="button"
class="clear-cart-button"
@click="clearCart"
>
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
.ranges-section{width:100%;padding:55px 0 65px;background:#fff;}
.ranges-header{width:100%;display:flex;align-items:flex-end;justify-content:space-between;gap:40px;margin-bottom:25px;}
.ranges-small-title{display:flex;align-items:center;gap:7px;font-size:11px;font-weight:600;letter-spacing:1.8px;color:#38B04C;text-transform:uppercase;margin-bottom:10px;}
.ranges-small-title i{font-size:11px;}
.ranges-header h2{margin:0;font-family:Georgia,"Times New Roman",serif;font-size:38px;font-weight:500;line-height:1.1;color:#202020;}
.ranges-header h2 span{color:#38B04C;}
.ranges-header p{max-width:370px;margin:0 0 3px;color:#777;font-size:13px;line-height:1.7;}
.ranges-carousel-wrapper{width:100%;position:relative;overflow:hidden;}
.ranges-carousel{width:100%;position:relative;overflow:hidden;touch-action:pan-y;}
.ranges-track{display:flex;width:100%;transition:transform .8s cubic-bezier(.77,0,.18,1);will-change:transform;}
.range-slide{width:100%;min-width:100%;flex:0 0 100%;position:relative;}
.range-slide-content{width:100%;min-height:330px;display:flex;align-items:center;position:relative;overflow:hidden;background-color:#557f30;background-size:48% auto;background-position:right center;background-repeat:no-repeat;border-radius:2px;}
.range-overlay{position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(20,40,10,.84) 0%,rgba(20,40,10,.68) 32%,rgba(20,40,10,.38) 52%,rgba(20,40,10,.08) 72%,rgba(20,40,10,0) 100%);}
.range-text{width:52%;padding:45px 30px 45px 45px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;position:relative;z-index:3;}
.range-label{display:flex;align-items:center;gap:7px;margin-bottom:10px;color:rgba(255,255,255,.78);font-size:10px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;}
.range-label i{font-size:9px;}
.range-text h3{margin:0 0 15px;color:#fff;font-family:Georgia,"Times New Roman",serif;font-size:40px;font-weight:500;line-height:1.1;}
.range-description{max-width:430px;margin:0 0 18px;color:rgba(255,255,255,.92);font-size:14px;line-height:1.7;}
.range-price{display:flex;align-items:baseline;gap:9px;margin-bottom:20px;}
.range-price span{color:rgba(255,255,255,.82);font-size:11px;}
.range-price strong{color:#fff;font-size:18px;font-weight:700;}
.range-actions{display:flex;align-items:center;flex-wrap:wrap;gap:10px;}
.range-button{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:40px;padding:11px 16px;border:1px solid transparent;border-radius:5px;font-size:10.5px;font-weight:700;text-decoration:none;cursor:pointer;transition:background .25s ease,color .25s ease,border-color .25s ease,transform .25s ease,box-shadow .25s ease;}
.add-cart-button{background:#38B04C;border-color:#38B04C;color:#fff;}
.add-cart-button:hover{background:#2f963f;border-color:#2f963f;transform:translateY(-2px);box-shadow:0 7px 18px rgba(56,176,76,.25);}
.order-button{background:#fff;border-color:#fff;color:#202020;}
.order-button:hover{background:#202020;border-color:#202020;color:#fff;transform:translateY(-2px);box-shadow:0 7px 18px rgba(0,0,0,.15);}
.range-button i{font-size:10px;transition:transform .25s ease;}
.add-cart-button:hover i{transform:translateY(-1px);}
.order-button:hover i{transform:translateX(3px);}
.ranges-controls{width:100%;display:flex;align-items:center;justify-content:center;gap:16px;margin-top:15px;}
.range-control{width:30px;height:30px;min-width:30px;display:flex;align-items:center;justify-content:center;border:1px solid #e4e8e4;border-radius:50%;background:#fff;color:#333;cursor:pointer;transition:.25s ease;}
.range-control:hover{background:#6f9e3c;border-color:#6f9e3c;color:#fff;transform:scale(1.06);}
.range-control i{font-size:8px;}
.range-dots{display:flex;align-items:center;justify-content:center;gap:5px;}
.range-dot{width:6px;height:6px;padding:0;border:0;border-radius:50%;background:#d9ded9;cursor:pointer;transition:width .35s ease,background .25s ease,transform .25s ease;}
.range-dot:hover{transform:scale(1.2);}
.range-dot.active{width:22px;border-radius:10px;background:#6f9e3c;}
.range-banner-skeleton{width:100%;height:330px;display:flex;align-items:center;justify-content:space-between;overflow:hidden;background:linear-gradient(90deg,#e8f4ea 25%,#f5faf6 50%,#e8f4ea 75%);background-size:200% 100%;animation:skeleton 1.5s infinite;}
.skeleton-content{width:45%;height:100px;margin-left:45px;border-radius:8px;background:rgba(255,255,255,.6);}
.skeleton-image{width:40%;height:220px;margin-right:40px;border-radius:50%;background:rgba(255,255,255,.6);}
@keyframes skeleton{0%{background-position:200% 0;}100%{background-position:-200% 0;}}
.ranges-error,.ranges-empty{width:100%;min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#999;}
.ranges-error i,.ranges-empty i{color:#38B04C;font-size:25px;}
.ranges-error p,.ranges-empty p{margin:0;font-size:13px;}
.ranges-error button{padding:9px 17px;border:1px solid #38B04C;border-radius:5px;background:#38B04C;color:#fff;font-size:11px;cursor:pointer;}
.cart-overlay{position:fixed;inset:0;z-index:9999;display:flex;justify-content:flex-end;background:rgba(0,0,0,.45);backdrop-filter:blur(3px);}
.cart-panel{width:440px;max-width:95%;height:100vh;display:flex;flex-direction:column;background:#fff;box-shadow:-10px 0 40px rgba(0,0,0,.15);}
.cart-header{min-height:82px;display:flex;align-items:center;justify-content:space-between;padding:18px 22px;border-bottom:1px solid #eee;}
.cart-header-title{display:flex;align-items:center;gap:12px;}
.cart-icon{width:42px;height:42px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#eef8f0;color:#38B04C;}
.cart-icon i{font-size:15px;}
.cart-header h3{margin:0;color:#202020;font-family:Georgia,"Times New Roman",serif;font-size:21px;font-weight:500;}
.cart-header-title span{color:#999;font-size:10px;}
.cart-close-button{width:34px;height:34px;display:flex;align-items:center;justify-content:center;border:0;border-radius:50%;background:#f6f6f6;color:#555;cursor:pointer;transition:.25s ease;}
.cart-close-button:hover{background:#38B04C;color:#fff;}
.cart-content{flex:1;overflow-y:auto;padding:18px;}
.cart-products{display:flex;flex-direction:column;gap:12px;}
.cart-item{position:relative;display:flex;gap:12px;padding:12px;border:1px solid #eee;border-radius:8px;background:#fff;transition:.25s ease;}
.cart-item:hover{border-color:#dce8df;box-shadow:0 5px 15px rgba(0,0,0,.04);}
.cart-item-image{width:82px;height:82px;flex-shrink:0;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:6px;background:#f9faf9;}
.cart-item-image img{width:100%;height:100%;object-fit:contain;padding:6px;}
.cart-no-image{color:#aaa;}
.cart-item-info{flex:1;min-width:0;padding-right:20px;}
.cart-item-type{display:block;margin-bottom:3px;color:#38B04C;font-size:8px;font-weight:800;letter-spacing:1.3px;}
.cart-item-info h4{margin:2px 0 7px;color:#222;font-family:Georgia,"Times New Roman",serif;font-size:14px;font-weight:600;line-height:1.3;}
.cart-item-price{color:#38B04C;font-size:11px;}
.cart-item-bottom{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:11px;}
.cart-quantity{height:28px;display:flex;align-items:center;border:1px solid #ddd;border-radius:5px;overflow:hidden;}
.cart-quantity button{width:27px;height:100%;display:flex;align-items:center;justify-content:center;border:0;background:#fff;color:#555;cursor:pointer;}
.cart-quantity button:hover:not(:disabled){background:#38B04C;color:#fff;}
.cart-quantity button:disabled{opacity:.35;cursor:not-allowed;}
.cart-quantity button i{font-size:8px;}
.cart-quantity span{width:30px;text-align:center;color:#333;font-size:10px;font-weight:600;}
.cart-item-total{color:#222;font-size:11px;}
.remove-cart-item{position:absolute;top:9px;right:9px;border:0;background:transparent;color:#aaa;cursor:pointer;transition:.2s ease;}
.remove-cart-item:hover{color:#d9534f;}
.remove-cart-item i{font-size:10px;}
.cart-footer{padding:18px 20px;border-top:1px solid #eee;background:#fff;box-shadow:0 -5px 20px rgba(0,0,0,.04);}
.summary-line,.summary-total{display:flex;align-items:center;justify-content:space-between;}
.summary-line{margin-bottom:9px;color:#777;font-size:11px;}
.summary-line strong{color:#333;}
.delivery-free{color:#38B04C;}
.summary-total{margin-top:12px;padding-top:13px;border-top:1px solid #eee;color:#222;font-size:14px;font-weight:600;}
.summary-total strong{color:#38B04C;font-size:17px;}
.checkout-button{width:100%;height:43px;display:flex;align-items:center;justify-content:center;gap:8px;margin-top:16px;border-radius:5px;background:#38B04C;color:#fff;font-size:12px;font-weight:600;text-decoration:none;transition:.25s ease;}
.checkout-button:hover{background:#2f963f;color:#fff;}
.continue-button{width:100%;height:38px;margin-top:8px;border:1px solid #ddd;border-radius:5px;background:#fff;color:#555;font-size:11px;cursor:pointer;}
.continue-button:hover{border-color:#38B04C;color:#38B04C;}
.clear-cart-button{width:100%;margin-top:12px;border:0;background:transparent;color:#999;font-size:10px;cursor:pointer;}
.clear-cart-button:hover{color:#d9534f;}
.empty-cart{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;text-align:center;}
.empty-cart-icon{width:75px;height:75px;display:flex;align-items:center;justify-content:center;margin-bottom:18px;border-radius:50%;background:#f1f8f3;color:#38B04C;}
.empty-cart-icon i{font-size:27px;}
.empty-cart h3{margin:0 0 8px;color:#222;font-family:Georgia,"Times New Roman",serif;font-size:21px;font-weight:500;}
.empty-cart p{max-width:260px;margin:0;color:#999;font-size:11px;line-height:1.7;}
.continue-shopping-button{display:inline-flex;align-items:center;gap:8px;margin-top:20px;padding:10px 16px;border:0;border-radius:5px;background:#38B04C;color:#fff;font-size:11px;cursor:pointer;}
.continue-shopping-button:hover{background:#2f963f;}
.cart-fade-enter-active,.cart-fade-leave-active{transition:opacity .3s ease;}
.cart-fade-enter-from,.cart-fade-leave-to{opacity:0;}
.cart-slide-enter-active,.cart-slide-leave-active{transition:transform .35s ease;}
.cart-slide-enter-from,.cart-slide-leave-to{transform:translateX(100%);}
@media(max-width:991px){
.ranges-header{align-items:flex-start;flex-direction:column;gap:12px;}
.ranges-header h2{font-size:35px;}
.range-slide-content{min-height:300px;background-size:45% auto;}
.range-text{width:60%;padding:35px 25px 35px 30px;}
.range-text h3{font-size:34px;}
}
@media(max-width:576px){
.ranges-section{padding:35px 0 45px;}
.ranges-header h2{font-size:29px;}
.range-slide-content{min-height:455px;background-size:72% auto;background-position:right 20px;align-items:flex-end;}
.range-overlay{background:linear-gradient(180deg,rgba(20,40,10,.05) 0%,rgba(20,40,10,.25) 28%,rgba(20,40,10,.72) 58%,rgba(20,40,10,.9) 100%);}
.range-text{width:100%;min-height:260px;padding:25px 22px;justify-content:flex-end;}
.range-text h3{font-size:30px;}
.range-description{max-width:100%;font-size:12px;}
.range-actions{width:100%;flex-direction:column;align-items:stretch;}
.range-button{width:100%;}
.cart-panel{width:100%;max-width:100%;}
.cart-header{padding:15px;}
.cart-content{padding:12px;}
.cart-footer{padding:15px;}
.cart-item-image{width:70px;height:70px;}
}
</style>