from django.db import models


# Product Model/Schema
class Product(models.Model):  # prodmast
    prod_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    unit = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ("prod_name", "category", "unit")

    def __str__(self):
        return self.prod_name


# Stock Transaction Model/Schema
class StockTransaction(models.Model):  # stckmain
    TRANSACTION_TYPE_CHOICES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]

    trans_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    trans_date = models.DateField()

    def __str__(self):
        return f"{self.trans_type} - {self.trans_date}"


# Stock Details Model/Schema
class StockDetail(models.Model):  # stckdetail
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.prod_name} - {self.quantity}"
