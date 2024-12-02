from django.shortcuts import render, get_object_or_404, redirect
<<<<<<< HEAD
from .models import Boleta, Cliente, Pago
from django.contrib.auth import authenticate
=======
from .models import Boleta, Cliente, Pago, BoletaDetalle
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
import json

<<<<<<< HEAD
@api_view(['POST'])
def RegisterView(request):
    """
    Vista para registrar un nuevo cliente.
    Se reciben los parámetros: nombre, apellido, telefono, email, contraseña.
    """
    if request.method == 'POST':
        # Recibimos los datos del cliente
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        telefono = request.data.get('telefono')
        email = request.data.get('email')
        contrasena = request.data.get('contrasena')

        # Validar que todos los campos estén presentes
        if not all([nombre, apellido, telefono, email, contrasena]):
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe un cliente con ese email
        if Cliente.objects.filter(email=email).exists():
            return Response({"error": "Este email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el cliente en la base de datos
        cliente = Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
        )

        # Encriptar la contraseña antes de guardarla
        cliente.set_password(contrasena)
        cliente.save()

        # Crear el token de autenticación para el nuevo cliente
        token, created = Token.objects.get_or_create(user=cliente)

        return Response({'success': True, 'token': token.key, 'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# API de Login para autenticación basada en token
@api_view(["POST"])
def LoginView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        contrasena = data.get('contrasena')

        cliente = authenticate(request, username=email, password=contrasena)
        if cliente is not None:
            # Generar o recuperar el token de autenticación
            token, created = Token.objects.get_or_create(user=cliente)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


# API de artículos (Clientes)
@api_view(["GET", "POST"])
def api_articulos(request):
    if request.method == "GET":
        articulos = Cliente.objects.all()  # Obtenemos todos los clientes
        # Aquí puedes usar un serializer si necesitas formatear la respuesta de forma más estructurada
        data = [{"id": articulo.id, "nombre": articulo.nombre, "apellido": articulo.apellido, "telefono": articulo.telefono, "email": articulo.email} for articulo in articulos]
        return Response(data)
    elif request.method == "POST":
        return Response({"message": "Metodo POST para artículos no soportado."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# API para obtener, actualizar y eliminar un artículo (Cliente)
@api_view(["GET", "PUT", "DELETE"])
def api_articulos_detalle(request, pk):
    try:
        articulo = Cliente.objects.get(pk=pk)  # Buscamos al cliente por su id
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = {
            "id": articulo.id,
            "nombre": articulo.nombre,
            "apellido": articulo.apellido,
            "telefono": articulo.telefono,
            "email": articulo.email
        }
        return Response(data)

    elif request.method == "PUT":
        # Actualizar el cliente
        data = json.loads(request.body)
        articulo.nombre = data.get('nombre', articulo.nombre)
        articulo.apellido = data.get('apellido', articulo.apellido)
        articulo.telefono = data.get('telefono', articulo.telefono)
        articulo.email = data.get('email', articulo.email)
        articulo.save()
        return Response({"message": "Cliente actualizado correctamente."}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        articulo.delete()
        return Response({"message": "Cliente eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


# Función para obtener el nombre del cliente
@login_required
=======
# Función para obtener el nombre del cliente desde la tabla Cliente
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
def get_cliente_nombre(cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)  # Recuperamos el cliente
    return cliente.nombre if cliente else "Cliente desconocido"


<<<<<<< HEAD
# Vista de pedidos pendientes
@login_required
=======
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
def pedidos_pendientes(request):
    pedidos = Boleta.objects.filter(estado='procesado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)  # Obtenemos el nombre del cliente
        pedido.detalles = pedido.boletadetalle_set.all()  # Relación inversa a través del modelo BoletaDetalle
    return render(request, 'pedidos/pedidos_pendientes.html', {'pedidos': pedidos})


<<<<<<< HEAD
# Vista de historial de pedidos
@login_required
=======
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
def historial_pedidos(request):
    pedidos = Boleta.objects.filter(estado='finalizado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)
        # Obtener el pago asociado a la boleta
        pago = Pago.objects.filter(boleta=pedido).first()
        pedido.total_pago = pago.total if pago else 0
    return render(request, 'pedidos/historial_pedidos.html', {'pedidos': pedidos})


<<<<<<< HEAD
# Vista de detalle del pedido
@login_required
=======
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
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


<<<<<<< HEAD
# Vista para confirmar un pedido
@login_required
=======
>>>>>>> 03473e5075acce8de01d71c730745d9c29fe11d6
def confirmar_pedido(request, pedido_id):
    pedido = get_object_or_404(Boleta, id=pedido_id)
    if pedido.estado == 'procesado':
        # Actualiza el estado del pedido
        pedido.estado = 'realizado'
        pedido.save()

        # Recorre los detalles de la boleta y descuenta el stock
        detalles = BoletaDetalle.objects.filter(id_boleta=pedido)
        for detalle in detalles:
            helado = detalle.id_helado
            if helado.stock >= detalle.cantidad:  # Verifica que haya suficiente stock
                helado.stock -= detalle.cantidad
                helado.save()
            else:
                # Maneja el caso en que el stock no sea suficiente
                raise ValueError(f"Stock insuficiente para el helado {helado.nombre}.")

    return redirect('pedidos:detallepedido', pk=pedido.id)

