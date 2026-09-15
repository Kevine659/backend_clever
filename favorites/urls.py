from django.urls import path

from .views import (
    FavoriteListView,
    FavoriteAddView,
    FavoriteRemoveView,
    FavoriteCountView,
    FavoriteCountsView,
)


urlpatterns = [
    path(
        "",
        FavoriteListView.as_view(),
        name="favorite-list"
    ),
    path(
        "add/",
        FavoriteAddView.as_view(),
        name="favorite-add"
    ),
    path(
        "counts/",
        FavoriteCountsView.as_view(),
        name="favorite-counts"
    ),
    path(
        "<int:product_id>/count/",
        FavoriteCountView.as_view(),
        name="favorite-count"
    ),
    path(
        "<int:product_id>/remove/",
        FavoriteRemoveView.as_view(),
        name="favorite-remove"
    ),
]