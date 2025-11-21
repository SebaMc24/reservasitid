from django.shortcuts import render, redirect, get_object_or_404
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
    if not sala.disponible:
        return redirect('detalle_sala', pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.save()
            return redirect('detalle_sala', pk=pk)
    else:
        form = ReservaForm()
    return render(request, 'salas/reservar.html', {'form': form, 'sala': sala})