from django.db import models

# Create your models here.
class InventoryModel(models.Model):
    barcode=models.IntegerField() # . штрих-код
    product_name = models.CharField(max_length=256) #  наименование товара
    quantity = models.FloatField() # . количество
    remained = models.FloatField() # остался
    sales = models.FloatField() # . продано
    del_price = models.DecimalField(max_digits=20, decimal_places=3) # цена
    selling_price = models.DecimalField(max_digits=20, decimal_places=3) # Продающий цена
    birlik = models.CharField(max_length=50) # yidinitsa izmirenie

    updated = models.DateTimeField(auto_now=True) # обновленнo
    created = models.DateTimeField(auto_now_add=True) # создана

    def __str__(self):
        return self.product_name

class BirlikModel(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ActionModel(models.Model):
    barcode = models.CharField(max_length=50)
    product_name = models.CharField(max_length=256)
    quantity = models.FloatField()
    selling_price = models.DecimalField(max_digits=20, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DecimalField(max_digits=20, decimal_places=3)
    del_price = models.DecimalField(max_digits=20, decimal_places=3)
    birlik = models.CharField(max_length=50)

    empty = models.CharField(max_length=50,default='empty')
    empty_number = models.IntegerField(default='0000000')

    def __str__(self):
        return f"{self.product_name , str(self.created)[0:10]}"
