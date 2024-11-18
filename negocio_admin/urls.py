"""
URL configuration for negocio_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from administracion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar-compra/', views.registrar_compra, name='registrar_compra'),
    path('', views.pagina_principal, name='pagina_principal'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/filtrar/', views.filtrar_productos, name='filtrar_productos'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('producto/precio/<int:producto_id>/', views.obtener_precio_producto, name='obtener_precio_producto'),
    path('ventas/registrar/', views.registrar_venta, name='registrar_venta'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/registrar/', views.registrar_compra, name='registrar_compra'),
]
