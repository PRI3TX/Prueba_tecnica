from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Vehiculo
from django.http import JsonResponse
import pandas as pd
from django.db.models import Sum, Count


@login_required
def lista_vehiculos(request):
    qs = Vehiculo.objects.all().order_by('-fecha_inicio')

    # Filtros
    placa = request.GET.get('placa')
    if placa:
        qs = qs.filter(placa__icontains=placa)

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        qs = qs.filter(fecha_inicio__range=[fecha_inicio, fecha_fin])

    validado = request.GET.get('validado')
    if validado in ['True', 'False']:
        qs = qs.filter(validado=(validado == 'True'))

    # Dashboard con métricas
    stats = {
        "total_vehiculos": qs.count(),
        "total_facturacion": qs.aggregate(Sum("facturacion"))["facturacion__sum"] or 0,
        "total_entregas": qs.aggregate(Sum("numero_entregas"))["numero_entregas__sum"] or 0,
        "validados": qs.filter(validado=True).count(),
        "no_validados": qs.filter(validado=False).count(),
    }

    return render(request, 'vehiculos/lista.html', {'vehiculos': qs, 'stats': stats})

@login_required
def toggle_validado(request, id):
    v = Vehiculo.objects.get(id=id)
    v.validado = not v.validado
    v.save()
    return JsonResponse({'status': 'ok', 'validado': v.validado})

@login_required
def exportar_csv(request):
    qs = Vehiculo.objects.all().order_by('-fecha_inicio')

    # Aplicar mismos filtros que en lista_vehiculos
    placa = request.GET.get('placa')
    if placa:
        qs = qs.filter(placa__icontains=placa)

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        qs = qs.filter(fecha_inicio__range=[fecha_inicio, fecha_fin])

    validado = request.GET.get('validado')
    if validado in ['True', 'False']:
        qs = qs.filter(validado=(validado == 'True'))

    # Exportar CSV
    import pandas as pd
    df = pd.DataFrame(list(qs.values()))
    response = df.to_csv(index=False)
    return JsonResponse({'csv': response})