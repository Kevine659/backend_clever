import{defineStore}from"pinia"

export const useCartStore=defineStore(
"cart",
{
state:()=>({
items:[],
initialized:false
}),
getters:{
itemsCount:state=>{
return state.items.reduce(
(total,item)=>{
return total+Number(item.quantity||0)
},
0
)
},
total:state=>{
return state.items.reduce(
(total,item)=>{
return total+
Number(item.price||0)*
Number(item.quantity||0)
},
0
)
},
isEmpty:state=>{
return state.items.length===0
}
},
actions:{
initialize(){
if(this.initialized)return
this.load()
this.initialized=true
},
save(){
try{
localStorage.setItem(
"shop_cart",
JSON.stringify(this.items)
)
}catch(error){
console.error(
"Erreur sauvegarde panier :",
error
)
}
},
load(){
try{
const savedCart=
localStorage.getItem("shop_cart")
if(!savedCart){
this.items=[]
return
}
const parsed=JSON.parse(savedCart)
if(!Array.isArray(parsed)){
this.items=[]
return
}
this.items=parsed
.map(item=>this.normalizeItem(item))
.filter(Boolean)
this.save()
}catch(error){
console.error(
"Erreur chargement panier :",
error
)
this.items=[]
}
},
normalizeItem(item){
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
if(!rangeId||Number.isNaN(rangeId)){
return null
}
return{
type:"range",
item_type:"range",
range_id:rangeId,
product_range:rangeId,
id:`range_${rangeId}`,
name:
item.name||
item.product_range_name||
"Gamme",
slug:item.slug||"",
image:
item.image||
item.range_image||
item.product_range_image||
null,
price:Number(
item.price??
item.unit_price??
item.current_price??
item.promotional_price??
0
)||0,
stock:0,
quantity:Number(
item.quantity||1
)
}
}
const productId=Number(
item.product_id||
item.product||
item.id
)
if(!productId||Number.isNaN(productId)){
return null
}
return{
type:"product",
item_type:"product",
product_id:productId,
product:productId,
id:`product_${productId}`,
name:
item.name||
item.product_name||
"Produit",
slug:item.slug||"",
image:
item.image||
item.product_image||
item.main_image||
null,
price:Number(
item.price??
item.unit_price??
item.current_price??
item.promotional_price??
0
)||0,
stock:Number(
item.stock||0
),
quantity:Number(
item.quantity||1
)
}
},
addProduct(product){
if(!product||!product.id)return false
const productId=Number(product.id)
if(!productId||Number.isNaN(productId)){
return false
}
if(Number(product.stock)<=0){
return false
}
const existing=this.items.find(
item=>
item.type==="product"&&
Number(item.product_id)===productId
)
if(existing){
const stock=Number(
product.stock||0
)
if(
stock>0&&
Number(existing.quantity)>=stock
){
return false
}
existing.quantity=
Number(existing.quantity||0)+1
this.save()
return true
}
this.items.push({
type:"product",
item_type:"product",
product_id:productId,
product:productId,
id:`product_${productId}`,
name:product.name||"Produit",
slug:product.slug||"",
image:
product.main_image||
product.image||
null,
price:Number(
product.current_price??
product.promotional_price??
product.price??
0
)||0,
stock:Number(
product.stock||0
),
quantity:1
})
this.save()
return true
},
addRange(range){
if(!range||!range.id)return false
const rangeId=Number(range.id)
if(!rangeId||Number.isNaN(rangeId)){
return false
}
const existing=this.items.find(
item=>
item.type==="range"&&
Number(item.range_id)===rangeId
)
if(existing){
existing.quantity=
Number(existing.quantity||0)+1
this.save()
return true
}
this.items.push({
type:"range",
item_type:"range",
range_id:rangeId,
product_range:rangeId,
id:`range_${rangeId}`,
name:range.name||"Gamme",
slug:range.slug||"",
image:
range.image||
range.range_image||
range.product_range_image||
null,
price:Number(
range.current_price??
range.promotional_price??
range.price??
0
)||0,
stock:0,
quantity:1
})
this.save()
return true
},
increase(item){
if(!item)return false
if(item.type==="product"){
const stock=Number(
item.stock||0
)
if(
stock>0&&
Number(item.quantity)>=stock
){
return false
}
}
item.quantity=
Number(item.quantity||0)+1
this.save()
return true
},
decrease(item){
if(!item)return false
const quantity=
Number(item.quantity||0)
if(quantity<=1)return false
item.quantity=quantity-1
this.save()
return true
},
getKey(item){
if(!item)return null
if(item.type==="range"){
const id=Number(
item.range_id||
item.product_range
)
if(!id||Number.isNaN(id)){
return null
}
return`range_${id}`
}
const id=Number(
item.product_id||
item.product||
item.id
)
if(!id||Number.isNaN(id)){
return null
}
return`product_${id}`
},
remove(item){
const key=this.getKey(item)
if(!key)return
this.items=
this.items.filter(
current=>this.getKey(current)!==key
)
this.save()
},
clear(){
this.items=[]
this.save()
},
getItemTotal(item){
if(!item)return 0
return Number(item.price||0)*
Number(item.quantity||0)
}
}
}
)