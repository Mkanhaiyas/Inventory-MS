from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_inventory, name="inventory"),
    path("add_product", views.addProduct, name="add_product"),
    path("add_transaction", views.add_transaction, name="add_transaction"),
    path("transaction_history", views.transaction_history, name="transaction_history"),
    path(
        "delete_product/<int:product_id>/", views.delete_product, name="delete_product"
    ),
]
