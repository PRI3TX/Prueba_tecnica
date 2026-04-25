from django.core.management.base import BaseCommand
from vehiculos.models import Vehiculo
from faker import Faker
import random
from datetime import timedelta

class Command(BaseCommand):
    help = "Genera datos de prueba para Vehiculo"

    def handle(self, *args, **kwargs):
        fake = Faker()
        tipos = ["Turbo", "Sencillo", "Eléctrico"]

        for _ in range(50):
            inicio = fake.date_time_this_year()
            fin = inicio + timedelta(hours=random.randint(1, 10))

            Vehiculo.objects.create(
                codigo=fake.uuid4(),
                placa=fake.license_plate(),
                tipo_vehiculo=random.choice(tipos),
                fecha_inicio=inicio,
                fecha_fin=fin,
                numero_entregas=random.randint(1, 20),
                facturacion=round(random.uniform(100000, 5000000), 2),
                observacion=fake.text(max_nb_chars=50),
                cliente=fake.company(),
                validado=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS("✅ Se generaron 50 registros de prueba"))

