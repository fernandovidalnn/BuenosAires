from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, PerfilUsuario
from .forms import ProductoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.db import connection
import random
from django.contrib.auth.decorators import login_required
import requests

def home(request):
    return render(request, "core/home.html")

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    tipousu = PerfilUsuario.objects.get(user=user).tipousu
                    if tipousu != 'Bodeguero':
                        return redirect(home)
                    else:
                        data["mesg"] = "¡La cuenta o la password no son correctos!"    
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "core/iniciar_sesion.html", data)


#------------------------------------
#agregado fernando
@login_required
def facturas(request):
    rut = 'admin' if request.user.is_superuser else request.user.perfilusuario.rut
    facturas = []

    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_OBTENER_FACTURAS %s", [rut])
        resultados = cursor.fetchall()

        for fila in resultados:
            facturas.append({
                'nrofac': fila[0],
                'cliente': fila[1],
                'fecha': fila[2],  # Puedes aplicar strftime si quieres mostrarla bonita
                'descripcion': fila[3],
                'monto': fila[4],  # <-- Aquí SIN FORMATO
                'nroGD': fila[5] if fila[5] != 0 else "No aplica",
                'estadoGD': fila[6],
                'nroSS': fila[7] if fila[7] != 0 else "No aplica",
                'estadoSS': fila[8],
            })

    contexto = {
        'facturas': facturas,
        'es_admin': request.user.is_superuser
    }

    return render(request, "core/facturas.html", contexto)




#----------------------------------------------------------
def cerrar_sesion(request):
    logout(request)
    return redirect(home)

def tienda(request):
    listaproductos = []

    with connection.cursor() as cursor:
        cursor.execute("EXEC dbo.SP_OBTENER_EQUIPOS_EN_BODEGA")
        productos = cursor.fetchall()

    for row in productos:
        idprod = row[0]
        nomprod = row[1]
        cantidad = int(row[2])  # viene desde COUNT(*) en el SP

        try:
            producto = Producto.objects.get(idprod=idprod)
            disponibilidad = 'DISPONIBLE' if cantidad > 0 else 'AGOTADO'

            listaproductos.append({
                'idprod': idprod,
                'nomprod': nomprod,
                'descprod': producto.descprod,
                'precio': producto.precio,
                'imagen': producto.imagen.name if producto.imagen else 'default.png',
                'cantidad': cantidad,
                'disponibilidad': disponibilidad,
            })
        except Producto.DoesNotExist:
            continue

    return render(request, "core/tienda.html", {"list": listaproductos})



# https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
# https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
# https://www.transbankdevelopers.cl/referencia/webpay
# https://www.transbankdevelopers.cl/referencia/webpay#ambientes-y-credenciales

# Tipo de tarjeta   Detalle                        Resultado
# ---------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)

# @csrf_exempt
# def ficha(request, id):
#     data = {"mesg": "", "producto": None}

#     # Cuando el usuario hace clic en el boton COMPRAR, se ejecuta el METODO POST del
#     # formulario de ficha.html, con lo cual se redirecciona la página para que
#     # llegue a esta VISTA llamada "FICHA". A continuacion se verifica que sea un POST 
#     # y se valida que se trate de un usuario autenticado que no sea de estaff, 
#     # es decir, se comprueba que la compra sea realizada por un CLIENTE REGISTRADO.
#     # Si se tata de un CLIENTE REGISTRADO, se redirecciona a la vista "iniciar_pago"
#     if request.method == "POST":
#         if request.user.is_authenticated and not request.user.is_staff:
#             return redirect(iniciar_pago, id)
#         else:
#             # Si el usuario que hace la compra no ha iniciado sesión,
#             # entonces se le envía un mensaje en la pagina para indicarle
#             # que primero debe iniciar sesion antes de comprar
#             data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

#     # Si visitamos la URL de FICHA y la pagina no nos envia un METODO POST, 
#     # quiere decir que solo debemos fabricar la pagina y devolvera al browser
#     # para que se muestren los datos de la FICHA
#     data["producto"] = Producto.objects.get(idprod=id)
#     return render(request, "core/ficha.html", data)

#agregado fernando---INICIO--------------------------------

from .models import Producto
from . import dolar  # Importa el valor fijo

@csrf_exempt
def ficha(request, id):
    data = {"mesg": "", "producto": None}

    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(iniciar_pago, id)
        else:
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    producto = Producto.objects.get(idprod=id)
    data["producto"] = producto
    data["precio_usd"] = round(producto.precio / dolar.dolar_actual, 2)

    # 🔹 Agregado: recuperar datos del pago si existen
    pago_info = request.session.pop('pago_info', None)
    if pago_info:
        data.update(pago_info)

    return render(request, "core/ficha.html", data)




#-----------------FIN-------------------------------------




@csrf_exempt
def iniciar_pago(request, id):

    # Esta es la implementacion de la VISTA iniciar_pago, que tiene la responsabilidad
    # de iniciar el pago, por medio de WebPay. Lo primero que hace es seleccionar un 
    # número de orden de compra, para poder así, identificar a la propia compra.
    # Como esta tienda no maneja, en realidad no tiene el concepto de "orden de compra"
    # pero se indica igual
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = Producto.objects.get(idprod=id).precio
    return_url = request.build_absolute_uri('/pago_exitoso/')

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url)
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
    }

    return render(request, "core/iniciar_pago.html", context)


#PROFEEEEEEEEEEEEEEEEEEEEEE
# @csrf_exempt
# def pago_exitoso(request):

#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws: {}".format(token))
#         commercecode = "597055555532"
#         apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
#         tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
#         response = tx.commit(token=token)
#         print("response: {}".format(response))

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)
#         form = PerfilUsuarioForm()

#         context = {
#             "buy_order": response['buy_order'],
#             "session_id": response['session_id'],
#             "amount": response['amount'],
#             "response": response,
#             "token_ws": token,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "rut": perfil.rut,
#             "dirusu": perfil.dirusu,
#             "response_code": response['response_code']
#         }

#         return render(request, "core/pago_exitoso.html", context)
#     else:
#         return redirect(home)

# AGREGADO POR FERNANDO--------INICIO-----------------------------------
#version 1 facturas implementado
# @csrf_exempt
# def pago_exitoso(request):
#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws: {}".format(token))

#         tx = Transaction(options=WebpayOptions(
#             commerce_code="597055555532",
#             api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#             integration_type="TEST"
#         ))
#         response = tx.commit(token=token)
#         print("response:", response)

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)

#         # 🧠 Obtener producto por precio (¡Asegúrate que el precio sea único!)
#         try:
#             producto = Producto.objects.get(precio=response['amount'])
#         except Producto.DoesNotExist:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "No se encontró un producto con ese precio.",
#                 "response": response
#             })
#         except Producto.MultipleObjectsReturned:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "Se encontraron múltiples productos con ese precio. Ajusta tu lógica.",
#                 "response": response
#             })

#         # 📦 Crear la factura en la base de datos usando SP
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
#                 perfil.rut,
#                 producto.idprod,
#                 producto.precio,
#                 producto.nomprod
#             ])
#             nrofac = cursor.fetchone()[0]  # ← Captura el número de factura generado

#         # ✅ Renderizar vista de éxito con información
#         context = {
#             "buy_order": response['buy_order'],
#             "session_id": response['session_id'],
#             "amount": response['amount'],
#             "response": response,
#             "token_ws": token,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "rut": perfil.rut,
#             "dirusu": perfil.dirusu,
#             "response_code": response['response_code'],
#             "nrofac": nrofac  # Puedes mostrarlo si quieres
#         }

#         return render(request, "core/pago_exitoso.html", context)

#     return redirect(home)

#version2 facturas y solicitud de servicio

# @csrf_exempt
# def pago_exitoso(request):
#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws:", token)

#         tx = Transaction(options=WebpayOptions(
#             commerce_code="597055555532",
#             api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#             integration_type="TEST"
#         ))
#         response = tx.commit(token=token)
#         print("response:", response)

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)

#         # 🧠 Obtener producto por precio
#         try:
#             producto = Producto.objects.get(precio=response['amount'])
#         except Producto.DoesNotExist:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "No se encontró un producto con ese precio.",
#                 "response": response
#             })
#         except Producto.MultipleObjectsReturned:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "Se encontraron múltiples productos con ese precio.",
#                 "response": response
#             })

#         # 📦 Crear la factura
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
#                 perfil.rut,
#                 producto.idprod,
#                 producto.precio,
#                 producto.nomprod
#             ])
#             nrofac = cursor.fetchone()[0]

#         # 🛠️ Crear solicitud de instalación
#         from datetime import date
#         fecha_visita = date.today()
#         descripcion_servicio = "Instalación del producto comprado"

#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
#             """, [nrofac, fecha_visita, descripcion_servicio])

#         # ✅ Mostrar resultado al cliente
#         context = {
#             "buy_order": response['buy_order'],
#             "session_id": response['session_id'],
#             "amount": response['amount'],
#             "response": response,
#             "token_ws": token,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "rut": perfil.rut,
#             "dirusu": perfil.dirusu,
#             "response_code": response['response_code'],
#             "nrofac": nrofac
#         }

#         return render(request, "core/pago_exitoso.html", context)

#     return redirect(home)

#version2 facturas, solicitud de servicio ####---GUIA DE DESPACHO----#####
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import connection
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from django.contrib.auth.models import User
from core.models import Producto, PerfilUsuario



#FUNCIONANDOOOO
# @csrf_exempt
# def pago_exitoso(request):
#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws:", token)

#         tx = Transaction(options=WebpayOptions(
#             commerce_code="597055555532",
#             api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#             integration_type="TEST"
#         ))
#         response = tx.commit(token=token)
#         print("response:", response)

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)

#         # 🧠 Obtener producto por precio
#         try:
#             producto = Producto.objects.get(precio=response['amount'])
#         except Producto.DoesNotExist:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "No se encontró un producto con ese precio.",
#                 "response": response
#             })
#         except Producto.MultipleObjectsReturned:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "Se encontraron múltiples productos con ese precio.",
#                 "response": response
#             })

#         # 📦 Crear la factura
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
#                 perfil.rut,
#                 producto.idprod,
#                 producto.precio,
#                 producto.nomprod
#             ])
#             nrofac = cursor.fetchone()[0]

#         # 🛠️ Crear solicitud de instalación
#         fecha_visita = date.today()
#         descripcion_servicio = "Instalación del producto comprado"
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
#             """, [nrofac, fecha_visita, descripcion_servicio])

#         # 🚚 Crear guía de despacho
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_GUIA_DESPACHO %s", [nrofac])
#             nroGD = cursor.fetchone()[0]

#         # ✅ Mostrar resultado al cliente
#         context = {
#             "buy_order": response['buy_order'],
#             "session_id": response['session_id'],
#             "amount": response['amount'],
#             "response": response,
#             "token_ws": token,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "rut": perfil.rut,
#             "dirusu": perfil.dirusu,
#             "response_code": response['response_code'],
#             "nrofac": nrofac,
#             "nroGD": nroGD  # Guía de despacho generada
#         }

#         return render(request, "core/pago_exitoso.html", context)

#     return redirect(home)


#funciona 2.0
# @csrf_exempt
# def pago_exitoso(request):
#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws:", token)

#         tx = Transaction(options=WebpayOptions(
#             commerce_code="597055555532",
#             api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#             integration_type="TEST"
#         ))
#         response = tx.commit(token=token)
#         print("response:", response)

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)

#         # 🧠 Obtener producto por precio
#         try:
#             producto = Producto.objects.get(precio=response['amount'])
#         except Producto.DoesNotExist:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "No se encontró un producto con ese precio.",
#                 "response": response
#             })
#         except Producto.MultipleObjectsReturned:
#             return render(request, "core/pago_exitoso.html", {
#                 "error": "Se encontraron múltiples productos con ese precio.",
#                 "response": response
#             })

#         # 📦 Crear la factura
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
#                 perfil.rut,
#                 producto.idprod,
#                 producto.precio,
#                 producto.nomprod
#             ])
#             nrofac = cursor.fetchone()[0]

#         # 🛠️ Crear solicitud de instalación
#         fecha_visita = date.today()
#         descripcion_servicio = "Instalación del producto comprado"
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
#             """, [nrofac, fecha_visita, descripcion_servicio])

#         # 🚚 Crear guía de despacho
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC SP_CREAR_GUIA_DESPACHO %s", [nrofac])
#             nroGD = cursor.fetchone()[0]

#         # ✅ Guardar datos en sesión y redirigir a ficha
#         request.session['pago_info'] = {
#             "response_code": response['response_code'],
#             "buy_order": response['buy_order'],
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "rut": perfil.rut,
#             "dirusu": perfil.dirusu,
#             "amount": response['amount']
#         }
        
#         # 🔁 Redirigir según origen del pago
#         origen = request.session.pop("pago_origen", None)
#         if origen == "solicitud":
#             return redirect('obtener_solicitudes_de_servicio')
#         else:
#             return redirect('ficha', id=producto.idprod)

#     return redirect(home)

## funciona 3.0
# @csrf_exempt
# def pago_exitoso(request):
#     if request.method == "GET":
#         token = request.GET.get("token_ws")
#         print("commit for token_ws:", token)

#         tx = Transaction(options=WebpayOptions(
#             commerce_code="597055555532",
#             api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#             integration_type="TEST"
#         ))
#         response = tx.commit(token=token)
#         print("response:", response)

#         user = User.objects.get(username=response['session_id'])
#         perfil = PerfilUsuario.objects.get(user=user)

#         # Obtener el origen de la sesión
#         origen = request.session.pop("pago_origen", None)

#         # ✅ Si el pago vino desde una solicitud de servicio
#         if origen == "solicitud":
#             from .models import Factura, SolicitudServicio

#             # Crear factura dummy (sin producto asociado)
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO Factura (rutcli, idprod, precio, descripcion)
#                     VALUES (%s, NULL, %s, %s);
#                     SELECT SCOPE_IDENTITY();
#                 """, [perfil.rut, response['amount'], "Servicio técnico"])
#                 nrofac = cursor.fetchone()[0]

#             # Crear solicitud de servicio con valores de ejemplo
#             fecha_visita = date.today()
#             descripcion_servicio = "Solicitud ingresada desde formulario de servicio"

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
#                 """, [nrofac, fecha_visita, descripcion_servicio])

#             # Guardar en sesión para mostrar mensaje
#             request.session['pago_info'] = {
#                 "response_code": response['response_code'],
#                 "buy_order": response['buy_order'],
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "rut": perfil.rut,
#                 "dirusu": perfil.dirusu,
#                 "amount": response['amount']
#             }

#             return redirect('obtener_solicitudes_de_servicio')

#         # ✅ Si el pago vino desde la ficha de producto (como ya funciona)
#         else:
#             try:
#                 producto = Producto.objects.get(precio=response['amount'])
#             except Producto.DoesNotExist:
#                 return render(request, "core/pago_exitoso.html", {
#                     "error": "No se encontró un producto con ese precio.",
#                     "response": response
#                 })
#             except Producto.MultipleObjectsReturned:
#                 return render(request, "core/pago_exitoso.html", {
#                     "error": "Se encontraron múltiples productos con ese precio.",
#                     "response": response
#                 })

#             with connection.cursor() as cursor:
#                 cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
#                     perfil.rut,
#                     producto.idprod,
#                     producto.precio,
#                     producto.nomprod
#                 ])
#                 nrofac = cursor.fetchone()[0]

#             fecha_visita = date.today()
#             descripcion_servicio = "Instalación del producto comprado"

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
#                 """, [nrofac, fecha_visita, descripcion_servicio])

#             with connection.cursor() as cursor:
#                 cursor.execute("EXEC SP_CREAR_GUIA_DESPACHO %s", [nrofac])
#                 nroGD = cursor.fetchone()[0]

#             request.session['pago_info'] = {
#                 "response_code": response['response_code'],
#                 "buy_order": response['buy_order'],
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "rut": perfil.rut,
#                 "dirusu": perfil.dirusu,
#                 "amount": response['amount']
#             }

#             return redirect('ficha', id=producto.idprod)

#     return redirect(home)


@csrf_exempt
def pago_exitoso(request):
    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws:", token)

        tx = Transaction(options=WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type="TEST"
        ))
        response = tx.commit(token=token)
        print("response:", response)

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)

        # Origen del pago
        origen = request.session.pop("pago_origen", None)

        if origen == "solicitud":
            descripcion_servicio = request.session.pop("descsol", "Servicio técnico solicitado").strip()
            fecha_visita = date.today()

            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
                        perfil.rut,
                        9999,
                        response['amount'],
                        descripcion_servicio
                    ])
                    nrofac = cursor.fetchone()[0]

                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
                    """, [nrofac, fecha_visita, descripcion_servicio])

                request.session['pago_info'] = {
                    "response_code": response['response_code'],
                    "buy_order": response['buy_order'],
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "rut": perfil.rut,
                    "dirusu": perfil.dirusu,
                    "amount": response['amount']
                }

                # 👇 Volver al formulario de solicitud con éxito
                request.session["pago_info_servicio"] = {
                    "response_code": response['response_code'],
                    "buy_order": response['buy_order'],
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "rut": perfil.rut,
                    "dirusu": perfil.dirusu,
                    "amount": response['amount']
                    }
                return redirect("crear_solicitud") 
            except Exception as e:
                print("Error al procesar solicitud:", e)
                return render(request, "core/ingresar_solicitud_servicio.html", {
                    "error": "El pago fue aprobado, pero ocurrió un error al registrar la solicitud. Contáctenos."
                })

        else:
            try:
                producto = Producto.objects.get(precio=response['amount'])
            except Producto.DoesNotExist:
                return render(request, "core/pago_exitoso.html", {
                    "error": "No se encontró un producto con ese precio.",
                    "response": response
                })
            except Producto.MultipleObjectsReturned:
                return render(request, "core/pago_exitoso.html", {
                    "error": "Se encontraron múltiples productos con ese precio.",
                    "response": response
                })

            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s", [
                        perfil.rut,
                        producto.idprod,
                        producto.precio,
                        producto.nomprod
                    ])
                    nrofac = cursor.fetchone()[0]

                fecha_visita = date.today()
                descripcion_servicio = "Instalación del producto comprado"

                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC SP_CREAR_SOLICITUD_SERVICIO @nrofac=%s, @fechavisita=%s, @descsol=%s
                    """, [nrofac, fecha_visita, descripcion_servicio])

                with connection.cursor() as cursor:
                    cursor.execute("EXEC SP_CREAR_GUIA_DESPACHO %s", [nrofac])
                    nroGD = cursor.fetchone()[0]

                request.session['pago_info'] = {
                    "response_code": response['response_code'],
                    "buy_order": response['buy_order'],
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "rut": perfil.rut,
                    "dirusu": perfil.dirusu,
                    "amount": response['amount']
                }

                return redirect('ficha', id=producto.idprod)

            except Exception as e:
                print("Error en ficha:", e)
                return render(request, "core/pago_exitoso.html", {
                    "error": "El pago fue exitoso pero no se pudo procesar el pedido.",
                    "response": response
                })

    return redirect(home)





# AGREGADO POR FERNANDO--------FIN-----------------------------------


@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {"mesg": "", "form": ProductoForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos vehículos con el mismo ID!"

    elif action == 'upd':
        objeto = Producto.objects.get(idprod=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idprod=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Producto.objects.all().order_by('idprod')
    return render(request, "core/administrar_productos.html", data)



#funcionando
# def registrar_usuario(request):
#     if request.method == 'POST':
#         form = RegistrarUsuarioForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             rut = request.POST.get("rut")
#             tipousu = request.POST.get("tipousu")
#             dirusu = request.POST.get("dirusu")
#             PerfilUsuario.objects.update_or_create(user=user, rut=rut, tipousu=tipousu, dirusu=dirusu)
#             return redirect(iniciar_sesion)
#     form = RegistrarUsuarioForm()
#     return render(request, "core/registrar_usuario.html", context={'form': form})

#agregado por fernando --------INICIO-------------------------------------

from django.contrib import messages

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            dirusu = request.POST.get("dirusu")

            PerfilUsuario.objects.update_or_create(
                user=user,
                rut=rut,
                tipousu='Cliente',
                dirusu=dirusu
            )
            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('iniciar_sesion')
        else:
            messages.error(request, "Hubo un error al registrar el usuario. Revisa los datos ingresados.")
    else:
        form = RegistrarUsuarioForm()  # Solo si es GET

    return render(request, "core/registrar_usuario.html", context={'form': form})




#agregado por fernando --------FIN-------------------------------------


def perfil_usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.tipousu = request.POST.get("tipousu")
            perfil.dirusu = request.POST.get("dirusu")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['tipousu'].initial = perfil.tipousu
    form.fields['dirusu'].initial = perfil.dirusu
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)

# def obtener_solicitudes_de_servicio(request):
#     tipousu = PerfilUsuario.objects.get(user=request.user).tipousu
#     data = {'tipousu': tipousu }
#     return render(request, "core/obtener_solicitudes_de_servicio.html", data)


#agregado por fernando
from .models import SolicitudServicio, PerfilUsuario
from datetime import datetime
import os, json

def obtener_solicitudes_de_servicio(request):
    perfil = PerfilUsuario.objects.get(user=request.user)
    tipousu = perfil.tipousu

    if tipousu == "Cliente":
        lista = SolicitudServicio.objects.filter(nrofac__rutcli=perfil)
    elif tipousu == "Técnico":
        lista = SolicitudServicio.objects.filter(ruttec=perfil)
    else:
        lista = SolicitudServicio.objects.all()

    # ✅ Cargar horas modificadas desde archivo compartido
    ruta = os.path.join("core", "horas_temp.json")
    try:
        with open(ruta, "r") as f:
            horas_guardadas = json.load(f)
    except:
        horas_guardadas = {}

    for sol in lista:
        if str(sol.nrosol) in horas_guardadas:
            try:
                sol.hora = datetime.strptime(horas_guardadas[str(sol.nrosol)], "%H:%M").time()
            except:
                sol.hora = horas_guardadas[str(sol.nrosol)]  # fallback string

    # ✅ Leer información de pago si viene desde Webpay
    pago_info = request.session.pop("pago_info", None)

    data = {
        'tipousu': tipousu,
        'lista': lista,
        'es_tecnico': tipousu in ["Técnico", "Administrador"]
    }

    if pago_info:
        data.update(pago_info)

    return render(request, "core/obtener_solicitudes_de_servicio.html", data)



from django.shortcuts import get_object_or_404
from .models import SolicitudServicio
from datetime import datetime

def estado_solicitud(request, nrosol, accion):
    solicitud = get_object_or_404(SolicitudServicio, nrosol=nrosol)

    if accion == "aceptar":
        solicitud.estadosol = "Aceptada"
    elif accion == "cerrar":
        solicitud.estadosol = "Cerrada"

    solicitud.save()
    return redirect('obtener_solicitudes_de_servicio')


#esto funcionaa
# @csrf_exempt
# def modificar_solicitud(request, nrosol):
#     if request.method == 'POST':
#         solicitud = get_object_or_404(SolicitudServicio, nrosol=nrosol)
#         nueva_fecha = request.POST.get('fechavisita')
#         if nueva_fecha:
#             solicitud.fechavisita = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
#             solicitud.save()
#     return redirect('obtener_solicitudes_de_servicio')

#agregado por fernando-------------INICIO--------------

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

import json, os

@csrf_exempt
def modificar_solicitud(request, nrosol):
    if request.method == 'POST':
        nueva_fecha = request.POST.get('fechavisita')
        nueva_hora = request.POST.get('horavisita')

        # Guardar solo la fecha en BD con SP
        if nueva_fecha:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("EXEC SP_ACTUALIZAR_SOLICITUD_DE_SERVICIO %s, %s", [nrosol, nueva_fecha])

        # Guardar la hora temporal en archivo compartido
        if nueva_hora:
            import os, json
            path = os.path.join("core", "horas_temp.json")

            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except:
                data = {}

            data[str(nrosol)] = nueva_hora

            with open(path, "w") as f:
                json.dump(data, f)

    return redirect('obtener_solicitudes_de_servicio')





#agregado por fernando-------------FIN-----------------


@csrf_exempt
def crear_solicitud(request):
    perfil = PerfilUsuario.objects.get(user=request.user)

    # ✅ Leer datos del pago exitoso desde la sesión (si existen)
    pago_info = request.session.pop("pago_info_servicio", None)

    if request.method == "POST":
        tiposol = request.POST.get("tiposol")
        fechavisita = request.POST.get("fechavisita")
        descsol = request.POST.get("descsol")

        from .models import SolicitudServicio, Factura

        try:
            factura = Factura.objects.filter(rutcli=perfil).latest('nrofac')
        except:
            context = {
                "error": "Debe tener al menos una factura para crear una solicitud."
            }
            if pago_info:
                context.update(pago_info)
            return render(request, "core/ingresar_solicitud_servicio.html", context)

        ultimo = SolicitudServicio.objects.all().order_by('-nrosol').first()
        nuevo_nrosol = (ultimo.nrosol + 1) if ultimo else 1

        tecnico = PerfilUsuario.objects.filter(tipousu="Técnico").first()

        solicitud = SolicitudServicio(
            nrosol=nuevo_nrosol,
            nrofac=factura,
            tiposol=tiposol,
            fechavisita=fechavisita,
            ruttec=tecnico,
            descsol=descsol,
            estadosol="Modificada"
        )
        solicitud.save()
        return redirect('obtener_solicitudes_de_servicio')

    # GET: Mostrar formulario con mensaje de pago si existe
    context = {}
    if pago_info:
        context.update(pago_info)

    return render(request, "core/ingresar_solicitud_servicio.html", context)


#funciona
# @csrf_exempt
# def iniciar_pago_servicio(request):
#     if not request.user.is_authenticated:
#         return redirect('iniciar_sesion')

#     buy_order = str(random.randrange(1000000, 99999999))
#     session_id = request.user.username
#     amount = 10000  # Monto fijo o ajustable según lógica
#     return_url = request.build_absolute_uri('/pago_exitoso/')

#     tx = Transaction(options=WebpayOptions(
#         commerce_code="597055555532",
#         api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
#         integration_type="TEST"
#     ))
#     response = tx.create(buy_order, session_id, amount, return_url)

#     perfil = PerfilUsuario.objects.get(user=request.user)

#     context = {
#         "buy_order": buy_order,
#         "session_id": session_id,
#         "amount": amount,
#         "return_url": return_url,
#         "response": response,
#         "token_ws": response['token'],
#         "url_tbk": response['url'],
#         "first_name": request.user.first_name,
#         "last_name": request.user.last_name,
#         "email": request.user.email,
#         "rut": perfil.rut,
#         "dirusu": perfil.dirusu,
#     }

#     return render(request, "core/iniciar_pago.html", context)



# agregado ppr fernando ------------inicio----------------------

@csrf_exempt
def iniciar_pago_servicio(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    # ✅ Guarda el origen para redirigir correctamente después
    origen = request.POST.get("origen")
    if origen:
        request.session["pago_origen"] = origen

        # ✅ Guarda la descripción solo si es una solicitud
        if origen == "solicitud":
            descsol = request.POST.get("descsol")
            if descsol:
                request.session["descsol"] = descsol.strip()

    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = 10000  # Monto fijo o ajustable según lógica
    return_url = request.build_absolute_uri('/pago_exitoso/')

    tx = Transaction(options=WebpayOptions(
        commerce_code="597055555532",
        api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        integration_type="TEST"
    ))
    response = tx.create(buy_order, session_id, amount, return_url)

    perfil = PerfilUsuario.objects.get(user=request.user)

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
    }

    return render(request, "core/iniciar_pago.html", context)





# agregado ppr fernando ------------fin----------------------