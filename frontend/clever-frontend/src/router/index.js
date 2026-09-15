import { createRouter, createWebHistory } from "vue-router"
import RegisterViews from "../views/registerviews.vue"
import login from "../views/login.vue"
import homeviews from "../views/homeviews.vue"
import details from "../components/details.vue"
import panier from "../components/panier.vue"
import produits from "../components/produits.vue"
import cosmetique from "../components/cosmetique.vue"
import sante from "../components/sante.vue"
import fertilite from "../components/fertilite.vue"
import dietetique from "../components/dietetique.vue"
import promotions from "../components/promotions.vue"
import favoris from "../components/favoris.vue"
import profil from "../components/profil.vue"
import apropos from "../components/apropos.vue"
import contact from "../components/contact.vue"

const routes = [

    {
        path: "/",
        name: "Home",
        component: homeviews
    },

    {
        path: "/contact",
        name: "Contact",
        component: contact
    },

    
    {
        path: "/a-propos",
        name: "A propos",
        component: apropos
    },

    {
        path: "/produit",
        name: "product-detail",
        component: details
    },

    {
        path: "/profil",
        name: "Profil",
        component: profil
    },


    {
        path: "/favoris",
        name: "Favoris",
        component: favoris
    },

    {
        path: "/promotions",
        name: "Promotions",
        component: promotions
    },

    {
        path: "/dietetique",
        name: "Dietetique",
        component: dietetique
    },

    {
        path: "/fertilite",
        name: "Fertilite",
        component: fertilite
    },

     {
        path: "/sante",
        name: "Sante",
        component: sante
    },

     {
        path: "/cosmetiques",
        name: "Cosmetiques",
        component: cosmetique
    },

    {
        path: "/boutique",
        name: "Boutique",
        component: produits
    },

     {
        path: "/panier",
        name: "panier",
        component: panier
    },


    {
        path: "/inscription",
        name: "register",
        component: RegisterViews
    },

    {
        path: "/connexion",
        name: "login",
        component: login
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router