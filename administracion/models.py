from django.db import models
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # null=False asegura que no puede ser nulo
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta de {self.producto.nombre} - {self.cantidad} unidades"
    

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Compra de {self.producto.nombre} - {self.cantidad} unidades'