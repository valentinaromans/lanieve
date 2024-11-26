from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Helado
from .forms import HeladoForm
from django.contrib.auth.decorators import login_required

def lista_helados(request):
    helados = Helado.objects.all()
    return render(request, 'helados/lista_helados.html', {'helados': helados})

def detalle_helado(request, pk):
    helado = get_object_or_404(Helado, pk=pk)
    return render(request, 'helados/detalle_helado.html', {'helado': helado})

@login_required
def crear_helado(request):
    if request.method == 'POST':
        form = HeladoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Helado creado exitosamente.')
            return redirect('helados:lista_helados')
    else:
        form = HeladoForm()
    return render(request, 'helados/crear_helados.html', {'form': form})

@login_required
def editar_helado(request, pk):
    helado = get_object_or_404(Helado, pk=pk)
    if request.method == 'POST':
        form = HeladoForm(request.POST, instance=helado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Helado actualizado exitosamente.')
            return redirect('helados:lista_helados')
    else:
        form = HeladoForm(instance=helado)
    return render(request, 'helados/editar_helado.html', {'form': form})

@login_required
def eliminar_helado(request, pk):
    helado = get_object_or_404(Helado, pk=pk)
    if request.method == 'POST':
        helado.delete()
        messages.success(request, 'Helado eliminado exitosamente.')
        return redirect('helados:lista_helados')
    return render(request, 'helados/eliminar_helado.html', {'helado': helado})
