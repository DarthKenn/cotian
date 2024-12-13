from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Venta, Compra
from .forms import ProductoForm, VentaForm
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
import calendar
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
from datetime import datetime
from django.db.models import Avg
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('login')  # Redirigir a la página de inicio de sesión


def lista_productos(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, "administracion/lista_productos.html", {"productos": productos, "form": form})

def filtrar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(id__icontains=query) | Q(precio__icontains=query) | Q(stock__icontains=query)
    )
    productos_data = list(productos.values('id', 'nombre', 'descripcion', 'precio', 'stock'))
    return JsonResponse({'productos': productos_data})

def obtener_precio_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return JsonResponse({'precio': producto.precio})

@login_required
def pagina_principal(request):
    return render(request, "administracion/pagina_principal.html")

def registrar_venta(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')

        if not producto_id or not cantidad:
            messages.error(request, "Debe seleccionar un producto y especificar una cantidad.")
            return render(request, 'registrar_venta.html', {'productos': productos})

        cantidad = int(cantidad)
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            messages.error(request, "El producto seleccionado no existe.")
            return render(request, 'registrar_venta.html', {'productos': productos})

        producto.save()

        precio_total = producto.precio * cantidad
        venta = Venta(
            producto=producto,
            cantidad=cantidad,
            total=precio_total,
        )
        venta.save()  # El número de boleta se genera automáticamente aquí

        messages.success(request, f"Venta registrada exitosamente con boleta #{venta.boleta}.")
        return redirect('registrar_venta')

    return render(request, 'administracion/registrar_venta.html', {'productos': productos})


def lista_ventas(request):
    ventas = Venta.objects.all()  # Recupera todas las ventas registradas
    return render(request, 'administracion/lista_ventas.html', {'ventas': ventas})


def lista_compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    productos = Producto.objects.all()
    return render(request, 'administracion/lista_compras.html', {'compras': compras, 'productos': productos})

def registrar_compra(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        costo_unitario = request.POST.get('costo')

        try:
            producto = Producto.objects.get(id=producto_id)
            cantidad = int(cantidad)
            costo_unitario = float(costo_unitario)
            costo_total = cantidad * costo_unitario

            # Sumar al stock del producto
            producto.stock += cantidad
            producto.save()

            # Registrar la compra
            Compra.objects.create(
                producto=producto,
                cantidad=cantidad,
                costo_unitario=costo_unitario,
                costo_total=costo_total,
                fecha=timezone.now()
            )

            messages.success(request, 'Compra registrada con éxito.')
        except Producto.DoesNotExist:
            messages.error(request, 'El producto seleccionado no existe.')
        except Exception as e:
            messages.error(request, f'Error al registrar la compra: {str(e)}')

    productos = Producto.objects.all()
    return render(request, 'administracion/registrar_compra.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()  # Elimina el producto
    return redirect('lista_productos')  # Redirige nuevamente a la lista de productos

# Vista para cargar el formulario de edición
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductoForm(instance=producto)
        return render(request, 'administracion/editar_producto.html', {'form': form})
    
def comparar_ventas(request):
    promedio_cantidad = None
    promedio_precio = None
    total_productos = None
    total_dinero = None
    mensaje = None

    # Capturamos las fechas del rango enviadas por el usuario
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        # Convertir las fechas en objetos datetime
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)

        if fecha_inicio and fecha_fin:
            # Filtrar las ventas dentro del rango de fechas
            ventas_filtradas = Venta.objects.filter(fecha__date__gte=fecha_inicio, fecha__date__lte=fecha_fin)

            if ventas_filtradas.exists():
                # Calcular promedios
                promedio_cantidad = ventas_filtradas.aggregate(Avg('cantidad'))['cantidad__avg']
                promedio_precio = ventas_filtradas.aggregate(Avg('total'))['total__avg']
                
                # Calcular totales
                total_productos = ventas_filtradas.aggregate(Sum('cantidad'))['cantidad__sum']
                total_dinero = ventas_filtradas.aggregate(Sum('total'))['total__sum']
            else:
                mensaje = "No se encontraron ventas en el periodo seleccionado."
        else:
            mensaje = "Las fechas proporcionadas no son válidas."
    else:
        mensaje = "Por favor, selecciona un rango de fechas."

    return render(request, 'administracion/comparar_ventas.html', {
        'promedio_cantidad': promedio_cantidad,
        'promedio_precio': promedio_precio,
        'total_productos': total_productos,
        'total_dinero': total_dinero,
        'mensaje': mensaje,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })