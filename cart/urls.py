from django.urls import path

from .views import (
    CartView,
    AddToCartView,
    SyncCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
)


urlpatterns = [

    # Voir le panier
    path(
        "",
        CartView.as_view(),
        name="cart"
    ),

    # Ajouter un produit
    path(
        "add/",
        AddToCartView.as_view(),
        name="cart-add"
    ),

    # Synchroniser le panier visiteur
    # après connexion
    path(
        "sync/",
        SyncCartView.as_view(),
        name="cart-sync"
    ),

    # Modifier quantité
    path(
        "items/<int:pk>/",
        UpdateCartItemView.as_view(),
        name="cart-update"
    ),

    # Supprimer produit
    path(
        "items/<int:pk>/remove/",
        RemoveCartItemView.as_view(),
        name="cart-remove"
    ),

    # Vider panier
    path(
        "clear/",
        ClearCartView.as_view(),
        name="cart-clear"
    ),
]