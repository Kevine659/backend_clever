from django.urls import path

from .views import (
    OrderListCreateView,
    OrderDetailView,
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderStatusView,
    
)


urlpatterns = [

   

    # Commandes
    path(
        "",
        OrderListCreateView.as_view(),
        name="order-list-create"
    ),

    path(
        "<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail"
    ),

    # Administration
    path(
        "admin/",
        AdminOrderListView.as_view(),
        name="admin-order-list"
    ),

    path(
        "admin/<int:pk>/",
        AdminOrderDetailView.as_view(),
        name="admin-order-detail"
    ),

    path(
        "admin/<int:pk>/status/",
        AdminOrderStatusView.as_view(),
        name="admin-order-status"
    ),
]