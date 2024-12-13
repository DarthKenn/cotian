from django.db import models
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    boleta = models.IntegerField(unique=True, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.boleta:  # Solo asigna boleta si no existe
            ultimo_numero_boleta = Venta.objects.all().order_by('-boleta').first()
            self.boleta = (ultimo_numero_boleta.boleta + 1) if ultimo_numero_boleta else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boleta {self.boleta} - {self.producto.nombre}"
    

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Compra de {self.producto.nombre} - {self.cantidad} unidades'