from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db import models
from .models import StockTransaction, StockDetail, Product
from .forms import StockTransactionForm, StockDetailForm, ProductForm


def addProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})


def add_transaction(request):
    StockDetailFormSet = inlineformset_factory(
        StockTransaction, StockDetail, form=StockDetailForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        formset = StockDetailFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            transaction = form.save()
            formset.instance = transaction
            formset.save()
            return redirect("inventory")

    else:
        form = StockTransactionForm()
        formset = StockDetailFormSet()

    return render(request, "add_transaction.html", {"form": form, "formset": formset})


def view_inventory(request):
    products = Product.objects.all()

    inventory_data = []

    for product in products:
        stock_ins = (
            StockDetail.objects.filter(
                product=product, transaction__trans_type="IN"
            ).aggregate(total=models.Sum("quantity"))["total"]
            or 0
        )
        stock_outs = (
            StockDetail.objects.filter(
                product=product, transaction__trans_type="OUT"
            ).aggregate(total=models.Sum("quantity"))["total"]
            or 0
        )
        current_stock = int(product.unit) + stock_ins - stock_outs

        inventory_data.append(
            {
                "product": product,
                "stock_in": stock_ins,
                "stock_out": stock_outs,
                "available": current_stock,
            }
        )

    return render(request, "inventory.html", {"inventory_data": inventory_data})


def transaction_history(request):
    transactions = StockTransaction.objects.order_by("-trans_date").prefetch_related(
        "stockdetail_set", "stockdetail_set__product"
    )
    flat_transactions = []
    for txn in transactions:
        for detail in txn.stockdetail_set.all():
            flat_transactions.append(
                {
                    "date": txn.trans_date,
                    "type": txn.get_trans_type_display(),
                    "product": detail.product.prod_name,
                    "unit": detail.product.unit,
                    "quantity": detail.quantity,
                }
            )

    return render(request, "transaction.html", {"flat_transactions": flat_transactions})
