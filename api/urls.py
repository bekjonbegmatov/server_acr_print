
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [
    # Admin
    path('', views.getRoutes , name="Imdex"),
    # Inventory Model
    path('inventory/<int:pk>', views.inventory_details, name='inventory_details'),
    path('inventory/all', views.getInventoryProducts, name='invAll'),
    path('inventory/create', views.createInventoryProduct, name="createInventoryProduct"),

    # Refund product from action to inventory
    path('refund' , views.refund_inventory_product , name='refund products'),

    path('actions/all', views.getActions, name="getActions"),
    path('action/<int:pk>', views.action_delete, name='inventory_details'),
    path('action/create', views.createAction, name="createAction"),

    # path('actions/export/excel', views.export_action_to_excel, name="export exsel action"),
    path('report/export/excel', views.report_actions_and_kresit_to_excel, name="export exsel action"),

    path('brlik/all', views.getBriliks, name='Barcha brlilani olish'),
    path('brlik/<int:pk>', views.brlik_detailes, name='brlik uzgartirish'),
    path('brlik/create', views.postBirlik , name=' clrate brlik'),

]
