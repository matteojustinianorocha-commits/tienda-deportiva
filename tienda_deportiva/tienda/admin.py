from django.contrib import admin
from .models import Deporte, Categoria, Producto, ImagenProducto, Pedido, DetallePedido

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 3 # Te muestra 3 casilleros para agregar imágenes rápido

class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]

admin.site.register(Deporte)
admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido)
admin.site.register(DetallePedido)