from ast import Store
from django.contrib import admin
from . import models
# Register your models here.
# admin.site.register(models.DutyModel)
admin.site.register(models.InventoryModel)
admin.site.register(models.ActionModel)
admin.site.register(models.BirlikModel)
