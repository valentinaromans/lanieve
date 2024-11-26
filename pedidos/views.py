from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import Boleta

# Función para obtener el nombre del cliente desde la tabla cliente
def get_cliente_nombre(cliente_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre FROM cliente WHERE id = %s", [cliente_id])
        result = cursor.fetchone()
    return result[0] if result else "Cliente desconocido"


def pedidos_pendientes(request):
    pedidos = Boleta.objects.filter(estado='proceso').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente_id)
    return render(request, 'pedidos/pedidos_pendientes.html', {'pedidos': pedidos})

def historial_pedidos(request):
    pedidos = Boleta.objects.filter(estado='finalizado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente_id)
    return render(request, 'pedidos/historial_pedidos.html', {'pedidos': pedidos})

def detalle_pedido(request, pk):
    pedido = get_object_or_404(Boleta, pk=pk)
    pedido.cliente_nombre = get_cliente_nombre(pedido.cliente_id)

    if request.method == 'POST':  # Confirmar pedido
        pedido.estado = 'finalizado'
        pedido.save()
        return redirect('pedidos:pedidospendientes')  # Redirige a la lista de pendientes

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})

def confirmar_pedido(request, id):
    pedido = get_object_or_404(Boleta, id=id)
    pedido.estado = 'finalizado'
    pedido.save()
    return redirect('pedidos:historialpedidos')
