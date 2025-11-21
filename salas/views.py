from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Sala, Reserva
from .forms import ReservaForm

def inicio(request):
    salas = Sala.objects.all()
    return render(request, 'salas/inicio.html', {'salas': salas})

def detalle_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    reserva_activa = sala.reservas.filter(fecha_termino__gt=timezone.now()).first()
    return render(request, 'salas/detalle.html', {
        'sala': sala,
        'reserva_activa': reserva_activa
    })

def reservar(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    
    # Verificar que la sala tenga pk válido
    if not sala.pk:
        messages.error(request, 'Error: Sala inválida')
        return redirect('inicio')
    
    if not sala.habilitada:
        messages.error(request, 'Esta sala no está habilitada para reservas')
        return redirect('detalle_sala', pk=pk)
    
    if not sala.disponible:
        messages.error(request, 'Esta sala ya está reservada')
        return redirect('detalle_sala', pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, sala=sala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada exitosamente')
            return redirect('detalle_sala', pk=pk)
        else:
            return render(request, 'salas/reservas.html', {'form': form, 'sala': sala})
    else:
        form = ReservaForm(sala=sala)
        return render(request, 'salas/reservas.html', {'form': form, 'sala': sala})