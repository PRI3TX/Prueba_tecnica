from django.db import models

class Vehiculo(models.Model):
    TIPOS = [
        ("Turbo", "Turbo"),
        ("Sencillo", "Sencillo"),
        ("Eléctrico", "Eléctrico"),
    ]

    codigo = models.CharField(max_length=50)
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    numero_entregas = models.IntegerField()
    facturacion = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.placa} - {self.tipo_vehiculo}"
