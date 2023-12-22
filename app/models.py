from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_item', args=[str(self.id)])


class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discounts = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)

    def total_price(self):
        base_price = sum(item.price for item in self.items.all())
        discount_amount = sum(discount.amount for discount in self.discounts.all())
        tax_amount = (base_price - discount_amount) * sum(tax.rate for tax in self.taxes.all())
        return base_price - discount_amount + tax_amount

    def __str__(self):
        return f"Order #{self.id}"

    def get_absolute_url(self):
        return reverse('view_order', args=[str(self.id)])
