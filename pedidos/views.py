from django.shortcuts import render, get_object_or_404, redirect
from .models import Boleta, Cliente, Pago

# Función para obtener el nombre del cliente desde la tabla Cliente
def get_cliente_nombre(cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)  # Recuperamos el cliente usando la relación con la tabla Cliente
    return cliente.nombre if cliente else "Cliente desconocido"


def pedidos_pendientes(request):
    pedidos = Boleta.objects.filter(estado='procesado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)
        pedido.detalles = pedido.boletadetalle_set.all()  # Relación inversa a través del modelo BoletaDetalle
    return render(request, 'pedidos/pedidos_pendientes.html', {'pedidos': pedidos})


def historial_pedidos(request):
    pedidos = Boleta.objects.filter(estado='finalizado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)
        # Obtener el pago asociado a la boleta
        pago = Pago.objects.filter(boleta=pedido).first()
        pedido.total_pago = pago.total if pago else 0
    return render(request, 'pedidos/historial_pedidos.html', {'pedidos': pedidos})


def detalle_pedido(request, pk):
    pedido = get_object_or_404(Boleta, pk=pk)
    detalles = pedido.boletadetalle_set.all()  # Detalles asociados al pedido
    pago = Pago.objects.filter(boleta=pedido).first()
    total_pago = pago.total if pago else 0

    if request.method == 'POST':  # Confirmar pedido
        pedido.estado = 'finalizado'
        pedido.save()
        return redirect('pedidos:pedidospendientes')

    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total_pago': total_pago,
    })


def confirmar_pedido(request, pedido_id):
    pedido = get_object_or_404(Boleta, id=pedido_id)
    if pedido.estado == 'procesado':
        pedido.estado = 'finalizado' 
        pedido.save()
    return redirect('pedidos:detallepedido', pk=pedido.id)
