from django.shortcuts import render, get_object_or_404, redirect
from .models import Boleta, Cliente, Pago
from .forms import RegistroForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import ArticuloSerializer


# Registro de cliente
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar el Cliente
            cliente = form.save(commit=False)
            cliente.set_password(form.cleaned_data['contrasena'])  # 'contrasena' es el campo de la contraseña
            cliente.save()  # Guardamos solo el Cliente, sin necesidad de crear un perfil

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('usuarios:login')  # Redirigir a la página de login
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        contrasena = request.POST['contrasena']
        cliente = authenticate(request, email=email, contrasena=contrasena)
        if cliente:
            login(request, cliente)
            return redirect('productos:lista_productos')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')


# Vista de cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


# API de Login para autenticación basada en token
@api_view(["POST"])
def LoginView(request):
    if request.method == "POST":
        email = request.data.get('email')
        contrasena = request.data.get('contrasena')
        cliente = authenticate(request, username=email, password=contrasena)

        if cliente is not None:
            token, created = Token.objects.get_or_create(user=cliente)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


# API de artículos (Clientes)
@api_view(["GET", "POST"])
def api_articulos(request):
    if request.method == "GET":
        articulos = Cliente.objects.all()  # Obtenemos todos los clientes
        serializer = ArticuloSerializer(articulos, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API para obtener, actualizar y eliminar un artículo (Cliente)
@api_view(["GET", "PUT", "DELETE"])
def api_articulos_detalle(request, pk):
    try:
        articulo = Cliente.objects.get(pk=pk)  # Buscamos al cliente por su id
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ArticuloSerializer(articulo)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ArticuloSerializer(articulo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        articulo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Función para obtener el nombre del cliente
def get_cliente_nombre(cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)  # Recuperamos el cliente
    return cliente.nombre if cliente else "Cliente desconocido"


# Vista de pedidos pendientes
def pedidos_pendientes(request):
    pedidos = Boleta.objects.filter(estado='procesado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)  # Obtenemos el nombre del cliente
        pedido.detalles = pedido.boletadetalle_set.all()  # Relación inversa a través del modelo BoletaDetalle
    return render(request, 'pedidos/pedidos_pendientes.html', {'pedidos': pedidos})


# Vista de historial de pedidos
def historial_pedidos(request):
    pedidos = Boleta.objects.filter(estado='finalizado').order_by('fecha_hora')
    for pedido in pedidos:
        pedido.cliente_nombre = get_cliente_nombre(pedido.cliente.id)
        # Obtener el pago asociado a la boleta
        pago = Pago.objects.filter(boleta=pedido).first()
        pedido.total_pago = pago.total if pago else 0
    return render(request, 'pedidos/historial_pedidos.html', {'pedidos': pedidos})


# Vista de detalle del pedido
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


# Vista para confirmar un pedido
def confirmar_pedido(request, pedido_id):
    pedido = get_object_or_404(Boleta, id=pedido_id)
    if pedido.estado == 'procesado':
        pedido.estado = 'realizado'  # O el estado que corresponda cuando se confirme
        pedido.save()
    return redirect('pedidos:detallepedido', pk=pedido.id)

