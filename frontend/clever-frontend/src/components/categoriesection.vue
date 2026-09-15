<script setup>
import { ref, onMounted } from "vue"
import { RouterLink } from "vue-router"
import api from "../services/api"

const categories = ref([])
const loading = ref(true)
const error = ref(false)

const getCategoryImage = (image) => {
    if (!image) {
        return null
    }

    if (
        image.startsWith("http://") ||
        image.startsWith("https://")
    ) {
        return image
    }

    return `http://127.0.0.1:7000${image.startsWith("/") ? image : `/${image}`}`
}

const getCategoryRoute = (category) => {
    const slug = String(category.slug || "").toLowerCase()
    const name = String(category.name || "").toLowerCase()

    if (
        slug.includes("dietetique") ||
        slug.includes("diététique") ||
        name.includes("dietetique") ||
        name.includes("diététique")
    ) {
        return "/dietetique"
    }

    if (
        slug.includes("fertilite") ||
        slug.includes("fertilité") ||
        name.includes("fertilite") ||
        name.includes("fertilité")
    ) {
        return "/fertilite"
    }

    if (
        slug.includes("sante") ||
        slug.includes("santé") ||
        name.includes("sante") ||
        name.includes("santé")
    ) {
        return "/sante"
    }

    if (
        slug.includes("cosmetique") ||
        slug.includes("cosmétiques") ||
        slug.includes("cosmetiques") ||
        name.includes("cosmetique") ||
        name.includes("cosmétiques") ||
        name.includes("cosmetiques")
    ) {
        return "/cosmetiques"
    }

    return "/boutique"
}

const loadCategories = async () => {
    try {
        loading.value = true
        error.value = false

        const response = await api.get(
            "/products/categories/"
        )

        console.log(
            "Catégories reçues :",
            response.data
        )

        categories.value = response.data.results.filter(
            category => category.is_active !== false
        )

        console.log(
            "Catégories finales :",
            categories.value
        )

    } catch (err) {
        console.error(
            "Erreur lors du chargement des catégories :",
            err
        )

        error.value = true
        categories.value = []

    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadCategories()
})
</script>

<template>

    <section class="categories-section">

        <div class="container">

            <div class="categories-header">

                <div class="categories-title">

                    <span class="categories-small-title">
                        <i class="fa-solid fa-layer-group"></i>
                        NOS CATÉGORIES
                    </span>

                    <h2>
                        Découvrez nos
                        <span>univers</span>
                    </h2>

                </div>

                <p class="categories-description">
                    Explorez nos différentes catégories de produits
                    et trouvez facilement ce qui vous correspond.
                </p>

            </div>

            <div v-if="loading" class="categories-loading">

                <div v-for="n in 4" :key="n" class="category-skeleton"></div>

            </div>

            <div v-else-if="error" class="categories-error">

                <i class="fa-solid fa-circle-exclamation"></i>

                <p>
                    Impossible de charger les catégories.
                </p>

                <button type="button" class="retry-button" @click="loadCategories">
                    Réessayer
                </button>

            </div>

            <div v-else-if="categories.length > 0" class="categories-grid">

                <RouterLink v-for="category in categories" :key="category.id" :to="getCategoryRoute(category)"
                    class="category-card">

                    <div class="category-image-wrapper">

                        <img v-if="category.image" :src="getCategoryImage(category.image)" :alt="category.name"
                            class="category-image" />

                        <div v-else class="category-no-image">
                            <i class="fa-solid fa-image"></i>
                        </div>

                        <div class="category-overlay">

                            <span>
                                Voir les produits

                                <i class="fa-solid fa-arrow-right"></i>
                            </span>

                        </div>

                    </div>

                    <div class="category-content">

                        <h3>
                            {{ category.name }}
                        </h3>

                        <div class="category-arrow-wrapper">

                            <i class="fa-solid fa-arrow-right category-arrow"></i>

                        </div>

                    </div>

                </RouterLink>

            </div>

            <div v-else class="categories-empty">

                <i class="fa-solid fa-box-open"></i>

                <p>
                    Aucune catégorie disponible pour le moment.
                </p>

            </div>

        </div>

    </section>

</template>

<style scoped>
.categories-section {
    width: 100%;
    padding: 55px 0 65px;
    background: #fff;
}

.categories-header {
    width: 100%;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 40px;
    margin-bottom: 30px;
}

.categories-title {
    flex: 1;
}

.categories-small-title {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1.2px;
    color: #38b54a;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.categories-small-title i {
    font-size: 11px;
}

.categories-header h2 {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 34px;
    font-weight: 500;
    line-height: 1.1;
    color: #202020;
    margin: 0;
}

.categories-header h2 span {
    color: #38b54a;
}

.categories-description {
    max-width: 360px;
    font-size: 11px;
    line-height: 1.7;
    color: #777;
    margin: 0 0 2px;
}

.categories-grid {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
}

.category-card {
    width: 100%;
    display: block;
    background: #fff;
    border: 1px solid #edf1ed;
    border-radius: 10px;
    overflow: hidden;
    text-decoration: none;
    box-shadow: 0 5px 20px rgba(0, 0, 0, .04);
    transition:
        transform .3s ease,
        box-shadow .3s ease,
        border-color .3s ease;
}

.category-card:hover {
    transform: translateY(-6px);
    border-color: rgba(56, 181, 74, .25);
    box-shadow: 0 12px 30px rgba(0, 0, 0, .09);
}

.category-image-wrapper {
    width: 100%;
    height: 190px;
    position: relative;
    overflow: hidden;
    background: #f6faf6;
}

.category-image {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
    object-position: center;
    transition: transform .45s ease;
}

.category-card:hover .category-image {
    transform: scale(1.06);
}

.category-no-image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38b54a;
    font-size: 30px;
    background: #f5faf5;
}

.category-overlay {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 35px 15px 12px;
    background: linear-gradient(to top,
            rgba(0, 0, 0, .55),
            transparent);
    opacity: 0;
    transform: translateY(8px);
    transition:
        opacity .3s ease,
        transform .3s ease;
}

.category-card:hover .category-overlay {
    opacity: 1;
    transform: translateY(0);
}

.category-overlay span {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    font-size: 9px;
    font-weight: 500;
    color: #fff;
}

.category-overlay i {
    font-size: 8px;
    transition: transform .2s ease;
}

.category-card:hover .category-overlay i {
    transform: translateX(3px);
}

.category-content {
    width: 100%;
    height: 55px;
    padding: 0 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.category-content h3 {
    margin: 0;
    font-size: 12px;
    font-weight: 500;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.category-arrow-wrapper {
    width: 26px;
    height: 26px;
    min-width: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(56, 181, 74, .08);
    transition:
        background .25s ease,
        transform .25s ease;
}

.category-arrow {
    font-size: 9px;
    color: #38b54a;
    transition:
        transform .25s ease,
        color .25s ease;
}

.category-card:hover .category-arrow-wrapper {
    background: #38b54a;
    transform: translateX(2px);
}

.category-card:hover .category-arrow {
    color: #fff;
    transform: translateX(2px);
}

.categories-loading {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
}

.category-skeleton {
    width: 100%;
    height: 245px;
    border-radius: 10px;
    background:
        linear-gradient(90deg,
            #f1f4f1 25%,
            #fafafa 50%,
            #f1f4f1 75%);
    background-size: 200% 100%;
    animation: skeleton 1.5s infinite;
}

@keyframes skeleton {

    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }

}

.categories-error,
.categories-empty {
    width: 100%;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: #999;
}

.categories-error i,
.categories-empty i {
    font-size: 25px;
    color: #38b54a;
}

.categories-error p,
.categories-empty p {
    font-size: 11px;
    margin: 0;
}

.retry-button {
    border: 1px solid #38b54a;
    background: #38b54a;
    color: #fff;
    font-size: 10px;
    padding: 8px 15px;
    border-radius: 5px;
    cursor: pointer;
    transition: all .25s ease;
}

.retry-button:hover {
    background: #2f9d40;
    border-color: #2f9d40;
}

@media(max-width:991px) {

    .categories-section {
        padding: 45px 0 55px;
    }

    .categories-header {
        align-items: flex-start;
        flex-direction: column;
        gap: 12px;
    }

    .categories-description {
        max-width: 500px;
    }

    .categories-grid,
    .categories-loading {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

}

@media(max-width:576px) {

    .categories-section {
        padding: 35px 0 45px;
    }

    .categories-header {
        margin-bottom: 22px;
    }

    .categories-header h2 {
        font-size: 29px;
    }

    .categories-grid,
    .categories-loading {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .category-image-wrapper {
        height: 145px;
    }

    .category-content {
        height: 48px;
        padding: 0 10px;
    }

    .category-content h3 {
        font-size: 10px;
    }

    .category-arrow-wrapper {
        width: 22px;
        height: 22px;
        min-width: 22px;
    }

    .category-arrow {
        font-size: 8px;
    }

    .category-overlay {
        display: none;
    }

}

@media(max-width:400px) {

    .categories-grid,
    .categories-loading {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .category-image-wrapper {
        height: 125px;
    }

    .category-content {
        padding: 0 8px;
    }

    .category-content h3 {
        font-size: 9px;
    }

    .category-arrow-wrapper {
        width: 20px;
        height: 20px;
        min-width: 20px;
    }

    .category-arrow {
        font-size: 7px;
    }

}
</style>