from django.db import models
from store.models import Product,Variation
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250 , blank=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    

    @staticmethod
    def convert_to_kg(weight, unit):
        unit = unit.lower()

        if unit in ["g", "gram", "grams"]:
            return weight / 1000
        
        if unit in ["kg", "kilogram", "kilograms"]:
            return weight

        if unit in ["quintal", "qtl", "quintals"]:
            return weight * 100   # 1 quintal = 100 kg

        if unit in ["ltr", "liter", "litre", "liters", "litres"]:
            return weight * 1     # Assuming 1 liter ≈ 1 kg

        # Default fallback
        return weight

    def weight_unit_subtotal(self):
        weight_var = None
        unit_var = None

        for var in self.variations.all():
            if var.variation_category == "weight":
                weight_var = var.variation_value
            elif var.variation_category == "unit":
                unit_var = var.variation_value

        weight = float(weight_var) if weight_var else 0
        unit = unit_var if unit_var else "kg"

        # convert to KG using helper
        weight_kg = self.convert_to_kg(weight, unit)

        price_for_one = weight_kg * self.product.price

        return price_for_one * self.quantity



    def sub_total(self):
        return self.weight_unit_subtotal()

    def __unicode__(self):
        return self.product