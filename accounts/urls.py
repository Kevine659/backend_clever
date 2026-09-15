# 

from django.urls import path

from .views import (
    ProfileView,
    MyOrdersView,
)

urlpatterns = [
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),
    path(
        "orders/",
        MyOrdersView.as_view(),
        name="my-orders"
    ),
]