<script setup>
import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"
</script>

<template>
<div class="app">
<Header/>
<main>
<RouterView/>
</main>
<Footer/>
</div>
</template>

<style>
*{
box-sizing:border-box;
}
html,body,#app{
margin:0;
padding:0;
width:100%;
min-height:100%;
}
body{
font-family:"Montserrat",Arial,sans-serif;
color:#333;
background:#fff;
}
main{
min-height:500px;
}
</style>