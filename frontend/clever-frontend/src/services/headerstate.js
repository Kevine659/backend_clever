export const notifyCartChanged=(cart)=>{
    window.dispatchEvent(
        new CustomEvent(
            "cartChanged",
            {
                detail:Array.isArray(cart)?cart:[]
            }
        )
    )
}
export const notifyFavoritesChanged=(favorites)=>{
    window.dispatchEvent(
        new CustomEvent(
            "favoritesChanged",
            {
                detail:Array.isArray(favorites)?favorites:[]
            }
        )
    )
}