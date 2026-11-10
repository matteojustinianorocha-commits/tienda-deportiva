from django.db import models

class Deporte(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): return self.nombre

class Producto(models.Model):
    GENERO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer'), ('U', 'Unisex')]
    TIPO_PRODUCTO_CHOICES = [('indumentaria', 'Indumentaria'), ('calzado', 'Calzado')]

    nombre = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES, default='indumentaria')
    talles_disponibles = models.CharField(max_length=100, default="S, M, L, XL") # Por defecto para ropa
    colores_disponibles = models.CharField(max_length=150, default="Morado, Blanco, Negro")
    descripcion = models.TextField(blank=True, default="Producto deportivo de alto rendimiento.")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=200)
    destacado = models.BooleanField(default=False)

    def __str__(self): 
        return f"{self.nombre} ({self.get_tipo_producto_display()})"
# NUEVO: Modelo para asociar múltiples imágenes y colores a un producto
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes_extra', on_delete=models.CASCADE)
    color = models.CharField(max_length=50, help_text="Debe coincidir exactamente con el color (Ej: Morado, Blanco, Negro)")
    archivo_imagen = models.CharField(max_length=200, help_text="Nombre del archivo (Ej: remera_blanca.jpg)")

    def __str__(self):
        return f"{self.producto.nombre} - {self.color}"

class Pedido(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=250)
    ciudad = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=50, default='Aprobado (Simulado)')
    def __str__(self): return f"Pedido #{self.id} - {self.nombre_cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    talle_seleccionado = models.CharField(max_length=20, default="Standard")
    color_seleccionado = models.CharField(max_length=30, default="Standard")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)