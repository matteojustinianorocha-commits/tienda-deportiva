from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Deporte, Categoria, Pedido, DetallePedido

def inicio(request):
    deporte_filtro = request.GET.get('deporte')
    genero_filtro = request.GET.get('genero')

    productos = Producto.objects.all()

    if deporte_filtro:
        productos = productos.filter(deporte__nombre__iexact=deporte_filtro)
    
    if genero_filtro:
        productos = productos.filter(genero__iexact=genero_filtro)

    return render(request, 'tienda/inicio.html', {
        'productos': productos,
    })
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    talles_list = [t.strip() for t in producto.talles_disponibles.split(',')]
    colores_list = [c.strip() for c in producto.colores_disponibles.split(',')]
    
    # Obtenemos las imágenes adicionales cargadas en el admin
    imagenes_extra = producto.imagenes_extra.all()

    return render(request, 'tienda/detalle_producto.html', {
        'producto': producto,
        'talles_list': talles_list,
        'colores_list': colores_list,
        'imagenes_extra': imagenes_extra,
    })
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        talle = request.POST.get('talle')
        color = request.POST.get('color')
        
        carrito = request.session.get('carrito', {})
        item_key = f"{producto_id}_{talle}_{color}"
        
        if item_key in carrito:
            carrito[item_key]['cantidad'] += 1
        else:
            p = get_object_or_404(Producto, id=producto_id)
            carrito[item_key] = {
                'id': p.id,
                'nombre': p.nombre,
                'precio': float(p.precio),
                'cantidad': 1,
                'imagen': p.imagen,
                'talle': talle,
                'color': color
            }
        
        request.session['carrito'] = carrito
        return redirect('ver_carrito')
    return redirect('detalle_producto', producto_id=producto_id)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(i['precio'] * i['cantidad'] for i in carrito.values())
    return render(request, 'tienda/carrito.html', {'carrito': carrito, 'total_general': total})

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    # Si el identificador existe en el carrito, lo borramos
    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito
        
    return redirect('ver_carrito')

def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito: return redirect('inicio')
    total = sum(i['precio'] * i['cantidad'] for i in carrito.values())
    if request.method == 'POST':
        pedido = Pedido.objects.create(
            nombre_cliente=request.POST.get('nombre'),
            email=request.POST.get('email'),
            direccion=request.POST.get('direccion'),
            ciudad=request.POST.get('ciudad'),
            total=total
        )
        for key, item in carrito.items():
            DetallePedido.objects.create(
                pedido=pedido,
                producto=Producto.objects.get(id=item['id']),
                cantidad=item['cantidad'],
                talle_seleccionado=item['talle'],
                color_seleccionado=item['color'],
                precio_unitario=item['precio']
            )
        request.session['carrito'] = {}
        return redirect('orden_exitosa', pedido_id=pedido.id)
    return render(request, 'tienda/checkout.html', {'total_general': total})

def orden_exitosa(request, pedido_id):
    return render(request, 'tienda/orden_exitosa.html', {'pedido': get_object_or_404(Pedido, id=pedido_id)})