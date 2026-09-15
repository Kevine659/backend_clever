<script setup>
import {ref,computed,onMounted} from "vue"
import {RouterLink,useRouter} from "vue-router"
import api from "../services/api"

const router=useRouter()
const user=ref(null)
const orders=ref([])
const loading=ref(true)
const ordersLoading=ref(true)
const error=ref(false)
const activeOrder=ref(null)
const showEditModal=ref(false)
const showPasswordModal=ref(false)
const savingProfile=ref(false)
const changingPassword=ref(false)
const profileMessage=ref("")
const passwordMessage=ref("")
const profileError=ref("")
const passwordError=ref("")

const editForm=ref({
first_name:"",
last_name:"",
phone:"",
city:"",
address:""
})

const passwordForm=ref({
old_password:"",
new_password:"",
confirm_password:""
})

const isAuthenticated=computed(()=>{
return !!localStorage.getItem("token")
})

const userInitials=computed(()=>{
if(!user.value)return"U"
const first=user.value.first_name?.trim()?.charAt(0)||""
const last=user.value.last_name?.trim()?.charAt(0)||""
if(first||last)return`${first}${last}`.toUpperCase()
return user.value.email?.charAt(0)?.toUpperCase()||"U"
})

const displayName=computed(()=>{
if(!user.value)return"Utilisateur"
if(user.value.full_name)return user.value.full_name
const name=`${user.value.first_name||""} ${user.value.last_name||""}`.trim()
return name||"Utilisateur"
})

const formatPrice=price=>{
const number=Number(price||0)
return new Intl.NumberFormat("fr-FR",{
minimumFractionDigits:0,
maximumFractionDigits:0
}).format(number)+" FCFA"
}

const formatDate=date=>{
if(!date)return"-"
const value=new Date(date)
if(Number.isNaN(value.getTime()))return"-"
return new Intl.DateTimeFormat("fr-FR",{
day:"2-digit",
month:"long",
year:"numeric"
}).format(value)
}

const formatDateTime=date=>{
if(!date)return"-"
const value=new Date(date)
if(Number.isNaN(value.getTime()))return"-"
return new Intl.DateTimeFormat("fr-FR",{
day:"2-digit",
month:"short",
year:"numeric",
hour:"2-digit",
minute:"2-digit"
}).format(value)
}

const getItemImage=item=>{
if(!item)return null
const image=
item.image||
item.product_image||
item.range_image||
item.product_range_image||
item.main_image||
item.product?.main_image||
item.product?.image||
item.product_range?.image||
item.product_range?.main_image||
item.range?.image||
null
if(!image)return null
if(typeof image!=="string")return null
if(image.startsWith("http://")||image.startsWith("https://"))return image
const baseURL=api.defaults.baseURL||""
const cleanBase=baseURL.replace(/\/api\/?$/,"").replace(/\/$/,"")
if(image.startsWith("/"))return`${cleanBase}${image}`
return`${cleanBase}/${image}`
}

const getItemType=item=>{
if(!item)return"PRODUIT"
if(item.item_type==="range")return"GAMME"
if(item.product_range&&!item.product)return"GAMME"
return"PRODUIT"
}

const getItemsCount=order=>{
if(!order)return 0
if(order.items_count!==undefined&&order.items_count!==null){
return Number(order.items_count)||0
}
if(Array.isArray(order.items)){
return order.items.reduce((total,item)=>{
return total+Number(item.quantity||0)
},0)
}
return 0
}

const loadProfile=async()=>{
try{
const response=await api.get("/accounts/profile/")
user.value=response.data
editForm.value={
first_name:user.value.first_name||"",
last_name:user.value.last_name||"",
phone:user.value.phone||"",
city:user.value.city||"",
address:user.value.address||""
}
}catch(err){
console.error("Erreur chargement profil :",err)
error.value=true
}
}

const loadOrders=async()=>{
try{
ordersLoading.value=true
const response=await api.get("/accounts/orders/")
const data=response.data?.results||response.data||[]
orders.value=Array.isArray(data)?data:[]
}catch(err){
console.error("Erreur chargement commandes :",err)
orders.value=[]
}finally{
ordersLoading.value=false
}
}

const openEditProfile=()=>{
profileMessage.value=""
profileError.value=""
editForm.value={
first_name:user.value?.first_name||"",
last_name:user.value?.last_name||"",
phone:user.value?.phone||"",
city:user.value?.city||"",
address:user.value?.address||""
}
showEditModal.value=true
}

const closeEditProfile=()=>{
if(savingProfile.value)return
showEditModal.value=false
}

const saveProfile=async()=>{
profileMessage.value=""
profileError.value=""
try{
savingProfile.value=true
const response=await api.patch(
"/accounts/profile/",
editForm.value
)
user.value=response.data
profileMessage.value="Votre profil a été mis à jour avec succès."
setTimeout(()=>{
showEditModal.value=false
profileMessage.value=""
},1200)
}catch(err){
console.error("Erreur modification profil :",err)
profileError.value=
err.response?.data?.detail||
"Impossible de mettre à jour votre profil."
}finally{
savingProfile.value=false
}
}

const openPasswordModal=()=>{
passwordMessage.value=""
passwordError.value=""
passwordForm.value={
old_password:"",
new_password:"",
confirm_password:""
}
showPasswordModal.value=true
}

const closePasswordModal=()=>{
if(changingPassword.value)return
showPasswordModal.value=false
}

const changePassword=async()=>{
passwordMessage.value=""
passwordError.value=""
if(
!passwordForm.value.old_password||
!passwordForm.value.new_password||
!passwordForm.value.confirm_password
){
passwordError.value="Veuillez remplir tous les champs."
return
}
if(
passwordForm.value.new_password!==
passwordForm.value.confirm_password
){
passwordError.value="Les nouveaux mots de passe ne correspondent pas."
return
}
if(passwordForm.value.new_password.length<8){
passwordError.value="Le nouveau mot de passe doit contenir au moins 8 caractères."
return
}
try{
changingPassword.value=true
await api.patch(
"/accounts/change-password/",
{
old_password:passwordForm.value.old_password,
new_password:passwordForm.value.new_password
}
)
passwordMessage.value="Votre mot de passe a été modifié avec succès."
setTimeout(()=>{
showPasswordModal.value=false
passwordMessage.value=""
},1200)
}catch(err){
console.error("Erreur changement mot de passe :",err)
const data=err.response?.data
passwordError.value=
data?.detail||
data?.old_password?.[0]||
data?.new_password?.[0]||
"Impossible de modifier le mot de passe."
}finally{
changingPassword.value=false
}
}

const toggleOrder=order=>{
if(activeOrder.value?.id===order.id){
activeOrder.value=null
return
}
activeOrder.value=order
}

const logout=async()=>{
try{
await api.post("/accounts/logout/")
}catch(err){
console.error("Erreur déconnexion :",err)
}finally{
localStorage.removeItem("token")
localStorage.removeItem("user")
router.push("/connexion")
}
}

onMounted(async()=>{
if(!isAuthenticated.value){
router.push("/connexion")
return
}
loading.value=true
await Promise.all([
loadProfile(),
loadOrders()
])
loading.value=false
})
</script>

<template>
<section class="profile-page">
<div class="profile-container">
<div v-if="loading" class="profile-loading">
<i class="fa-solid fa-circle-notch fa-spin"></i>
<span>Chargement de votre espace...</span>
</div>

<div v-else-if="error" class="profile-error">
<i class="fa-solid fa-circle-exclamation"></i>
<h3>Impossible de charger votre profil</h3>
<button type="button" @click="loadProfile">Réessayer</button>
</div>

<template v-else-if="user">
<header class="profile-header">
<div class="header-content">
<span class="header-label">
<i class="fa-solid fa-user"></i>
ESPACE PERSONNEL
</span>
<h1>
Bonjour
<span>{{user.first_name||"cher client"}}</span>
</h1>
<p>
Gérez vos informations personnelles et consultez vos commandes.
</p>
</div>

<div class="header-actions">
<RouterLink to="/boutique" class="shop-button">
<i class="fa-solid fa-bag-shopping"></i>
Continuer mes achats
</RouterLink>

<button type="button" class="logout-button" @click="logout">
<i class="fa-solid fa-right-from-bracket"></i>
Déconnexion
</button>
</div>
</header>

<div class="profile-content">
<aside class="profile-sidebar">
<div class="identity">
<div class="avatar">
{{userInitials}}
</div>

<h2>{{displayName}}</h2>
<p>{{user.email}}</p>

<div class="member">
<i class="fa-regular fa-calendar"></i>
Membre depuis {{formatDate(user.date_joined)}}
</div>
</div>

<div class="sidebar-actions">
<button type="button" @click="openEditProfile">
<i class="fa-solid fa-pen"></i>
Modifier mon profil
</button>

<button type="button" @click="openPasswordModal">
<i class="fa-solid fa-lock"></i>
Sécurité du compte
</button>
</div>

<div class="contact-information">
<span class="side-label">MES COORDONNÉES</span>

<div class="contact-row">
<i class="fa-solid fa-envelope"></i>
<div>
<small>Email</small>
<strong>{{user.email}}</strong>
</div>
</div>

<div class="contact-row">
<i class="fa-solid fa-phone"></i>
<div>
<small>Téléphone</small>
<strong>{{user.phone||"Non renseigné"}}</strong>
</div>
</div>

<div class="contact-row">
<i class="fa-solid fa-location-dot"></i>
<div>
<small>Ville</small>
<strong>{{user.city||"Non renseignée"}}</strong>
</div>
</div>

<div class="contact-row">
<i class="fa-solid fa-house"></i>
<div>
<small>Adresse</small>
<strong>{{user.address||"Non renseignée"}}</strong>
</div>
</div>
</div>
</aside>

<main class="orders-area">
<div class="orders-heading">
<div>
<span class="header-label">
<i class="fa-solid fa-bag-shopping"></i>
MES COMMANDES
</span>

<h2>Mes achats</h2>

<p>
Retrouvez toutes vos commandes dans le tableau ci-dessous.
</p>
</div>

<div class="orders-number">
<strong>{{orders.length}}</strong>
<span>{{orders.length>1?"commandes":"commande"}}</span>
</div>
</div>

<div v-if="ordersLoading" class="orders-loading">
<i class="fa-solid fa-circle-notch fa-spin"></i>
<span>Chargement des commandes...</span>
</div>

<div v-else-if="orders.length===0" class="empty-orders">
<i class="fa-solid fa-receipt"></i>
<h3>Aucune commande</h3>
<p>Vous n'avez pas encore effectué de commande.</p>
<RouterLink to="/boutique">
Découvrir la boutique
</RouterLink>
</div>

<div v-else class="orders-table-wrapper">
<table class="orders-table">
<thead>
<tr>
<th>Commande</th>
<th>Date</th>
<th>Articles</th>
<th>Total</th>
<th>Détails</th>
</tr>
</thead>

<tbody>
<template v-for="order in orders" :key="order.id">
<tr
class="order-row"
:class="{active:activeOrder?.id===order.id}"
@click="toggleOrder(order)"
>
<td>
<div class="command-cell">
<div class="command-icon">
<i class="fa-solid fa-receipt"></i>
</div>

<div>
<span>COMMANDE</span>
<strong>#{{order.id}}</strong>
</div>
</div>
</td>

<td>
<div class="date-cell">
<span>{{formatDateTime(order.created_at)}}</span>
</div>
</td>

<td>
<div class="items-count">
<i class="fa-solid fa-box"></i>
{{getItemsCount(order)}}
</div>
</td>

<td>
<strong class="table-total">
{{formatPrice(order.total_amount)}}
</strong>
</td>

<td>
<button
type="button"
class="details-button"
@click.stop="toggleOrder(order)"
>
<i
class="fa-solid"
:class="
activeOrder?.id===order.id
?'fa-chevron-up'
:'fa-chevron-down'
"
></i>
</button>
</td>
</tr>

<tr
v-if="activeOrder?.id===order.id"
class="details-row"
>
<td colspan="5">
<div class="order-details">
<div class="details-header">
<div>
<span>CONTENU DE LA COMMANDE</span>
<h3>Articles achetés</h3>
</div>
</div>

<div
v-if="!order.items||order.items.length===0"
class="no-items"
>
<i class="fa-solid fa-box-open"></i>
<span>
Aucun article disponible pour cette commande.
</span>
</div>

<div v-else class="items-table">
<div class="items-table-head">
<span>ARTICLE</span>
<span>TYPE</span>
<span>QUANTITÉ</span>
<span>PRIX</span>
</div>

<div
v-for="item in order.items"
:key="item.id"
class="item-row"
>
<div class="item-product">
<div class="item-image">
<img
v-if="getItemImage(item)"
:src="getItemImage(item)"
:alt="item.product_name"
@error="$event.target.style.display='none'"
>

<i
v-else
class="fa-solid fa-image"
></i>
</div>

<strong>
{{item.product_name}}
</strong>
</div>

<div class="item-type">
{{getItemType(item)}}
</div>

<div class="item-quantity">
{{item.quantity}}
</div>

<div class="item-price">
{{formatPrice(item.subtotal)}}
</div>
</div>
</div>
</div>
</td>
</tr>
</template>
</tbody>
</table>
</div>
</main>
</div>
</template>
</div>
</section>

<Transition name="modal">
<div
v-if="showEditModal"
class="modal-overlay"
@click.self="closeEditProfile"
>
<div class="modal-box">
<div class="modal-title">
<div>
<span>MON PROFIL</span>
<h2>Modifier mes informations</h2>
</div>

<button
type="button"
@click="closeEditProfile"
>
<i class="fa-solid fa-xmark"></i>
</button>
</div>

<form @submit.prevent="saveProfile">
<div class="form-grid">
<div class="form-group">
<label>Prénom</label>
<input
v-model="editForm.first_name"
type="text"
>
</div>

<div class="form-group">
<label>Nom</label>
<input
v-model="editForm.last_name"
type="text"
>
</div>
</div>

<div class="form-group">
<label>Téléphone</label>
<input
v-model="editForm.phone"
type="tel"
>
</div>

<div class="form-group">
<label>Ville</label>
<input
v-model="editForm.city"
type="text"
>
</div>

<div class="form-group">
<label>Adresse</label>
<textarea
v-model="editForm.address"
rows="3"
></textarea>
</div>

<div
v-if="profileError"
class="message error"
>
{{profileError}}
</div>

<div
v-if="profileMessage"
class="message success"
>
{{profileMessage}}
</div>

<div class="modal-actions">
<button
type="button"
class="cancel"
@click="closeEditProfile"
>
Annuler
</button>

<button
type="submit"
class="save"
:disabled="savingProfile"
>
<i
v-if="savingProfile"
class="fa-solid fa-circle-notch fa-spin"
></i>

{{savingProfile?"Enregistrement...":"Enregistrer"}}
</button>
</div>
</form>
</div>
</div>
</Transition>

<Transition name="modal">
<div
v-if="showPasswordModal"
class="modal-overlay"
@click.self="closePasswordModal"
>
<div class="modal-box">
<div class="modal-title">
<div>
<span>SÉCURITÉ</span>
<h2>Modifier le mot de passe</h2>
</div>

<button
type="button"
@click="closePasswordModal"
>
<i class="fa-solid fa-xmark"></i>
</button>
</div>

<form @submit.prevent="changePassword">
<div class="form-group">
<label>Mot de passe actuel</label>
<input
v-model="passwordForm.old_password"
type="password"
>
</div>

<div class="form-group">
<label>Nouveau mot de passe</label>
<input
v-model="passwordForm.new_password"
type="password"
>
</div>

<div class="form-group">
<label>Confirmation</label>
<input
v-model="passwordForm.confirm_password"
type="password"
>
</div>

<div class="password-info">
<i class="fa-solid fa-circle-info"></i>
Minimum 8 caractères.
</div>

<div
v-if="passwordError"
class="message error"
>
{{passwordError}}
</div>

<div
v-if="passwordMessage"
class="message success"
>
{{passwordMessage}}
</div>

<div class="modal-actions">
<button
type="button"
class="cancel"
@click="closePasswordModal"
>
Annuler
</button>

<button
type="submit"
class="save"
:disabled="changingPassword"
>
<i
v-if="changingPassword"
class="fa-solid fa-circle-notch fa-spin"
></i>

{{changingPassword?"Modification...":"Modifier"}}
</button>
</div>
</form>
</div>
</div>
</Transition>
</template>

<style scoped>
.profile-page{
min-height:100vh;
background:#f7f9f7;
padding:25px 0 70px;
color:#202520
}
.profile-container{
width:min(1180px,92%);
margin:auto
}
.profile-header{
display:flex;
align-items:flex-end;
justify-content:space-between;
gap:30px;
padding-bottom:25px;
border-bottom:1px solid #dfe6df
}
.header-label{
display:flex;
align-items:center;
gap:8px;
color:#38B04C;
font-size:10px;
font-weight:800;
letter-spacing:1.8px
}
.profile-header h1{
margin:8px 0 7px;
font-family:Georgia,"Times New Roman",serif;
font-size:38px;
font-weight:500;
line-height:1.1
}
.profile-header h1 span{
color:#38B04C
}
.profile-header p{
margin:0;
color:#777;
font-size:13px
}
.header-actions{
display:flex;
gap:9px
}
.shop-button,
.logout-button{
height:40px;
display:flex;
align-items:center;
justify-content:center;
gap:8px;
padding:0 16px;
border-radius:2px;
font-size:11px;
font-weight:700;
transition:.25s ease
}
.shop-button{
background:#38B04C;
color:#fff;
text-decoration:none
}
.shop-button:hover{
background:#2f963f;
color:#fff
}
.logout-button{
border:1px solid #d9dfd9;
background:transparent;
color:#555;
cursor:pointer
}
.logout-button:hover{
border-color:#d9534f;
color:#d9534f
}
.profile-content{
display:grid;
grid-template-columns:275px minmax(0,1fr);
gap:45px;
padding-top:25px
}
.profile-sidebar{
border-right:1px solid #dfe6df;
padding-right:30px
}
.identity{
padding-bottom:20px;
border-bottom:1px solid #dfe6df;
text-align:center
}
.avatar{
width:80px;
height:80px;
display:flex;
align-items:center;
justify-content:center;
margin:0 auto 12px;
border-radius:50%;
background:#38B04C;
color:#fff;
font-size:23px;
font-weight:800
}
.identity h2{
margin:0 0 4px;
font-family:Georgia,"Times New Roman",serif;
font-size:21px;
font-weight:500
}
.identity p{
margin:0;
color:#888;
font-size:11px;
overflow:hidden;
text-overflow:ellipsis
}
.member{
margin-top:12px;
color:#38B04C;
font-size:10px
}
.sidebar-actions{
display:flex;
flex-direction:column;
padding:16px 0;
border-bottom:1px solid #dfe6df
}
.sidebar-actions button{
display:flex;
align-items:center;
gap:9px;
padding:9px 0;
border:0;
background:transparent;
color:#444;
font-size:11px;
text-align:left;
cursor:pointer;
transition:.2s ease
}
.sidebar-actions button:hover{
color:#38B04C
}
.sidebar-actions i{
width:17px;
color:#38B04C
}
.contact-information{
padding-top:20px
}
.side-label{
display:block;
margin-bottom:13px;
color:#38B04C;
font-size:9px;
font-weight:800;
letter-spacing:1.3px
}
.contact-row{
display:flex;
align-items:flex-start;
gap:10px;
padding:8px 0
}
.contact-row>i{
width:17px;
padding-top:2px;
color:#38B04C
}
.contact-row small{
display:block;
margin-bottom:2px;
color:#999;
font-size:9px
}
.contact-row strong{
display:block;
color:#333;
font-size:10px;
font-weight:600;
line-height:1.4;
word-break:break-word
}
.orders-area{
min-width:0
}
.orders-heading{
display:flex;
align-items:flex-end;
justify-content:space-between;
gap:20px;
padding-bottom:16px;
border-bottom:1px solid #dfe6df
}
.orders-heading h2{
margin:7px 0 5px;
font-family:Georgia,"Times New Roman",serif;
font-size:27px;
font-weight:500
}
.orders-heading p{
margin:0;
color:#888;
font-size:11px
}
.orders-number{
display:flex;
align-items:baseline;
gap:4px;
color:#38B04C
}
.orders-number strong{
font-size:23px
}
.orders-number span{
font-size:10px;
font-weight:700
}
.orders-table-wrapper{
margin-top:14px;
width:100%;
overflow-x:auto
}
.orders-table{
width:100%;
border-collapse:collapse;
table-layout:fixed;
background:transparent
}
.orders-table th{
padding:10px 10px;
border-bottom:2px solid #dfe6df;
color:#888;
font-size:8px;
font-weight:800;
letter-spacing:.9px;
text-align:left;
text-transform:uppercase
}
.orders-table th:nth-child(1){
width:24%
}
.orders-table th:nth-child(2){
width:25%
}
.orders-table th:nth-child(3){
width:16%
}
.orders-table th:nth-child(4){
width:24%
}
.orders-table th:nth-child(5){
width:11%
}
.order-row{
cursor:pointer;
transition:.2s ease
}
.order-row:hover,
.order-row.active{
background:#f1f7f2
}
.order-row td{
padding:12px 10px;
border-bottom:1px solid #e3e8e3;
vertical-align:middle
}
.command-cell{
display:flex;
align-items:center;
gap:9px
}
.command-icon{
width:34px;
height:34px;
display:flex;
align-items:center;
justify-content:center;
background:#eef8f0;
color:#38B04C
}
.command-cell span{
display:block;
margin-bottom:2px;
color:#999;
font-size:7px
}
.command-cell strong{
color:#222;
font-size:12px
}
.date-cell span{
color:#555;
font-size:9px;
line-height:1.4
}
.items-count{
display:inline-flex;
align-items:center;
gap:5px;
color:#555;
font-size:9px;
font-weight:700
}
.items-count i{
color:#38B04C
}
.table-total{
color:#38B04C;
font-size:11px
}
.details-button{
width:28px;
height:28px;
display:flex;
align-items:center;
justify-content:center;
border:0;
background:transparent;
color:#555;
cursor:pointer
}
.details-button:hover{
color:#38B04C
}
.details-row td{
padding:0;
border-bottom:1px solid #dfe6df;
background:#fafcf9
}
.order-details{
padding:18px 12px 22px
}
.details-header{
padding-bottom:11px;
border-bottom:1px solid #dfe6df
}
.details-header span{
display:block;
color:#38B04C;
font-size:8px;
font-weight:800;
letter-spacing:1.2px
}
.details-header h3{
margin:5px 0 0;
font-family:Georgia,"Times New Roman",serif;
font-size:18px;
font-weight:500
}
.items-table{
margin-top:8px
}
.items-table-head{
display:grid;
grid-template-columns:minmax(0,1fr) 85px 95px 120px;
gap:12px;
padding:8px 0;
border-bottom:1px solid #dfe6df;
color:#999;
font-size:7px;
font-weight:800;
letter-spacing:.8px
}
.item-row{
display:grid;
grid-template-columns:minmax(0,1fr) 85px 95px 120px;
align-items:center;
gap:12px;
padding:10px 0;
border-bottom:1px solid #e5e9e5
}
.item-row:last-child{
border-bottom:0
}
.item-product{
display:flex;
align-items:center;
gap:11px;
min-width:0
}
.item-image{
width:58px;
height:58px;
display:flex;
align-items:center;
justify-content:center;
flex-shrink:0;
overflow:hidden;
background:#f1f4f1
}
.item-image img{
width:100%;
height:100%;
object-fit:contain;
padding:4px
}
.item-image i{
color:#aeb6ae;
font-size:17px
}
.item-product strong{
overflow:hidden;
color:#252925;
font-family:Georgia,"Times New Roman",serif;
font-size:12px;
font-weight:500;
text-overflow:ellipsis
}
.item-type{
color:#38B04C;
font-size:8px;
font-weight:800
}
.item-quantity{
color:#333;
font-size:10px;
font-weight:700
}
.item-price{
color:#38B04C;
font-size:11px;
font-weight:800;
text-align:right
}
.no-items{
display:flex;
align-items:center;
justify-content:center;
gap:9px;
padding:25px;
color:#999;
font-size:10px
}
.no-items i{
color:#38B04C;
font-size:18px
}
.empty-orders{
min-height:280px;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
text-align:center
}
.empty-orders>i{
margin-bottom:15px;
color:#38B04C;
font-size:30px
}
.empty-orders h3{
margin:0 0 6px;
font-family:Georgia,"Times New Roman",serif;
font-size:20px;
font-weight:500
}
.empty-orders p{
margin:0;
color:#888;
font-size:11px
}
.empty-orders a{
margin-top:16px;
padding:10px 16px;
background:#38B04C;
color:#fff;
text-decoration:none;
font-size:10px;
font-weight:700
}
.orders-loading,
.profile-loading{
min-height:220px;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
gap:10px;
color:#888;
font-size:11px
}
.orders-loading i,
.profile-loading i{
color:#38B04C;
font-size:23px
}
.profile-error{
min-height:400px;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center
}
.profile-error>i{
color:#d9534f;
font-size:32px;
margin-bottom:13px
}
.profile-error h3{
font-family:Georgia,"Times New Roman",serif;
font-size:20px;
font-weight:500
}
.profile-error button{
border:0;
padding:9px 16px;
background:#38B04C;
color:#fff;
cursor:pointer
}
.modal-overlay{
position:fixed;
inset:0;
z-index:10000;
display:flex;
align-items:center;
justify-content:center;
padding:20px;
background:rgba(20,30,22,.55);
backdrop-filter:blur(5px)
}
.modal-box{
width:520px;
max-width:100%;
max-height:90vh;
overflow:auto;
background:#fff;
box-shadow:0 25px 70px rgba(0,0,0,.25)
}
.modal-title{
display:flex;
align-items:flex-start;
justify-content:space-between;
padding:25px;
border-bottom:1px solid #e0e6e0
}
.modal-title span{
color:#38B04C;
font-size:9px;
font-weight:800;
letter-spacing:1.5px
}
.modal-title h2{
margin:7px 0 0;
font-family:Georgia,"Times New Roman",serif;
font-size:23px;
font-weight:500
}
.modal-title button{
width:32px;
height:32px;
border:0;
background:#f2f4f2;
color:#555;
cursor:pointer
}
.modal-box form{
padding:25px
}
.form-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:15px
}
.form-group{
margin-bottom:16px
}
.form-group label{
display:block;
margin-bottom:7px;
color:#555;
font-size:11px;
font-weight:700
}
.form-group input,
.form-group textarea{
width:100%;
box-sizing:border-box;
padding:11px;
border:1px solid #dce3dc;
outline:none;
background:#fff;
color:#333;
font-family:inherit;
font-size:12px
}
.form-group input{
height:42px
}
.form-group textarea{
resize:vertical
}
.form-group input:focus,
.form-group textarea:focus{
border-color:#38B04C
}
.message,
.password-info{
padding:10px;
margin-bottom:15px;
font-size:11px
}
.message.error{
background:#fff0f0;
color:#d9534f
}
.message.success{
background:#eef8f0;
color:#2f963f
}
.password-info{
background:#f2f6f3;
color:#657065
}
.modal-actions{
display:flex;
justify-content:flex-end;
gap:10px
}
.cancel,
.save{
height:40px;
padding:0 18px;
border-radius:0;
font-size:11px;
font-weight:700;
cursor:pointer
}
.cancel{
border:1px solid #d9dfd9;
background:#fff;
color:#555
}
.save{
border:0;
background:#38B04C;
color:#fff
}
.save:disabled{
opacity:.6;
cursor:not-allowed
}
.modal-enter-active,
.modal-leave-active{
transition:.2s ease
}
.modal-enter-from,
.modal-leave-to{
opacity:0
}
@media(max-width:1000px){
.profile-content{
grid-template-columns:240px minmax(0,1fr);
gap:30px
}
.profile-sidebar{
padding-right:22px
}
.orders-table th:nth-child(2),
.orders-table td:nth-child(2){
min-width:135px
}
}
@media(max-width:800px){
.profile-page{
padding-top:20px
}
.profile-header{
align-items:flex-start;
flex-direction:column
}
.profile-content{
grid-template-columns:1fr;
padding-top:20px
}
.profile-sidebar{
padding-right:0;
padding-bottom:25px;
border-right:0;
border-bottom:1px solid #dfe6df
}
.orders-table{
min-width:700px
}
.orders-table-wrapper{
overflow-x:auto
}
}
@media(max-width:600px){
.profile-page{
padding:20px 0 50px
}
.profile-container{
width:92%
}
.profile-header h1{
font-size:31px
}
.header-actions{
width:100%;
flex-direction:column
}
.shop-button,
.logout-button{
width:100%
}
.orders-heading{
align-items:flex-start;
flex-direction:column
}
.orders-number{
margin-top:8px
}
.orders-table{
min-width:680px
}
.item-row,
.items-table-head{
grid-template-columns:minmax(0,1fr) 70px 75px 100px
}
.form-grid{
grid-template-columns:1fr;
gap:0
}
}
</style>