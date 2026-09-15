import{defineStore}from"pinia"
import{computed,ref}from"vue"
import api from"../services/api"

export const useFavoritesStore=defineStore("favorites",()=>{
const ids=ref([])
const counts=ref({})
const loading=ref(false)
const initialized=ref(false)

const isAuthenticated=()=>{
return !!localStorage.getItem("token")
}

const getGuestId=()=>{
let guestId=localStorage.getItem("guest_id")

if(!guestId){
if(window.crypto&&window.crypto.randomUUID){
guestId=window.crypto.randomUUID()
}else{
guestId="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
/[xy]/g,
c=>{
const r=Math.random()*16|0
const v=c==="x"
?r
:(r&0x3|0x8)
return v.toString(16)
}
)
}
localStorage.setItem(
"guest_id",
guestId
)
}

return guestId
}

const headers=()=>{
if(isAuthenticated())return{}
return{
"X-Guest-ID":getGuestId()
}
}

const count=computed(()=>{
return ids.value.length
})

const isFavorite=productId=>{
return ids.value.includes(
Number(productId)
)
}

const saveGuest=()=>{
if(isAuthenticated())return
localStorage.setItem(
"shop_favorites",
JSON.stringify(ids.value)
)
}

const loadGuest=()=>{
try{
const saved=
localStorage.getItem(
"shop_favorites"
)

if(!saved){
ids.value=[]
return
}

const parsed=JSON.parse(saved)

if(!Array.isArray(parsed)){
ids.value=[]
return
}

ids.value=[
...new Set(
parsed
.map(id=>Number(id))
.filter(
id=>
Number.isFinite(id)&&
id>0
)
)
]
}catch(error){
console.error(
"Erreur favoris invité :",
error
)
ids.value=[]
}
}

const initialize=async()=>{
if(initialized.value)return

loading.value=true

try{
if(!isAuthenticated()){
loadGuest()
}else{
const response=await api.get(
"/favorites/"
,{
headers:headers()
}
)

const data=
response.data?.results||
response.data||
[]

ids.value=Array.isArray(data)
?[
...new Set(
data
.map(item=>{
if(item?.product_id){
return Number(
item.product_id
)
}
if(typeof item?.product==="number"){
return Number(
item.product
)
}
if(typeof item?.product==="string"){
return Number(
item.product
)
}
if(item?.product?.id){
return Number(
item.product.id
)
}
return 0
})
.filter(
id=>
Number.isFinite(id)&&
id>0
)
)
]
:[]
}

const countsResponse=
await api.get(
"/favorites/counts/",
{
headers:headers()
}
)

if(
countsResponse.data&&
typeof countsResponse.data==="object"&&
!Array.isArray(countsResponse.data)
){
counts.value={
...countsResponse.data
}
}
}catch(error){
console.error(
"Erreur initialisation favoris :",
error
)

if(!isAuthenticated()){
loadGuest()
}
}finally{
loading.value=false
initialized.value=true
}
}

const getCount=productId=>{
const value=
counts.value[String(productId)]

return Number(value||0)
}

const add=async product=>{
if(!product?.id)return

const productId=Number(product.id)

if(
!productId||
isFavorite(productId)
)return

try{
loading.value=true

const response=await api.post(
"/favorites/add/",
{
product:productId
},
{
headers:headers()
}
)

ids.value=[
...ids.value,
productId
]

if(!isAuthenticated()){
saveGuest()
}

const serverCount=
response.data?.favorites_count

if(
serverCount!==undefined
){
counts.value={
...counts.value,
[String(productId)]:
Number(serverCount)||0
}
}else{
counts.value={
...counts.value,
[String(productId)]:
getCount(productId)+1
}
}
}catch(error){
console.error(
"Erreur ajout favori :",
error
)
throw error
}finally{
loading.value=false
}
}

const remove=async productId=>{
const id=Number(productId)

if(
!id||
!isFavorite(id)
)return

try{
loading.value=true

const response=await api.delete(
`/favorites/${id}/remove/`,
{
headers:headers()
}
)

ids.value=ids.value.filter(
favoriteId=>favoriteId!==id
)

if(!isAuthenticated()){
saveGuest()
}

counts.value={
...counts.value,
[String(id)]:
Number(
response.data?.favorites_count||0
)
}
}catch(error){
console.error(
"Erreur suppression favori :",
error
)
throw error
}finally{
loading.value=false
}
}

const toggle=async product=>{
const id=Number(product?.id)

if(!id)return

if(isFavorite(id)){
await remove(id)
}else{
await add(product)
}
}

const refresh=async()=>{
initialized.value=false
await initialize()
}

return{
ids,
counts,
loading,
count,
isFavorite,
getCount,
initialize,
add,
remove,
toggle,
refresh
}
})