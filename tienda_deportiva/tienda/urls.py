from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<str:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('orden-exitosa/<int:pedido_id>/', views.orden_exitosa, name='orden_exitosa'),
]