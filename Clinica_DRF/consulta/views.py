from django.shortcuts import render
from rest_framework.response import Response
#
from usuarios.models import CustomersUsers
from usuarios.serializers import CustomUserSerializer
from secretaria.models import SecretariaModel
from secretaria.serializers import SecretariaSerializer
# Importamos el status.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
# Importamos la clase serializers que hemos creado anteriormente.
#  En el modelo también agregamos la clase serializers, es una buena práctica.
from .models import ConsultaModel
from .serializers import ConsultaSerializers
# ----- Arreglar el formato de las fechas y la hora para el correo de respuesta. 
from django.utils.timezone import localtime
from datetime import timezone
import pytz
from django.template.loader import render_to_string
#
from django.core.mail import EmailMultiAlternatives
# Mensaje del E-mail.
from django.core.mail import EmailMessage
#
from django.conf import settings
from email.mime.image import MIMEImage
import os



# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def consulta_paciente(request):
    try:
        data = request.data.copy()
        primer_nombre = request.data['primer_nombre']
        segundo_nombre = request.data['segundo_nombre']
        ap_paterno = request.data['ap_paterno']
        ap_materno = request.data['ap_materno'] 
        email = request.data['email'] 
        consulta = request.data['consulta']
        # Validaciones.
        if not all([primer_nombre, segundo_nombre, ap_paterno, ap_materno, email, consulta]):
            return Response({'error': 0}, status=status.HTTP_400_BAD_REQUEST)
        dato_serializado = ConsultaSerializers(data=request.data)
        if dato_serializado.is_valid():
            dato_serializado.save()
            return Response({'success': 1}, status=status.HTTP_200_OK)
        else:
            # Si la validación falla, devolvemos los errores
            return Response({'error': 2}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)
#
@api_view(['GET'])
# Para este formulario NO se necesita token; @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def listar_consulta_abierta_paciente(request):
    try:
        consultas = ConsultaModel.objects.filter(consulta_cerrada=0)
        consultas_serializers = ConsultaSerializers(consultas, many=True)
        return Response({'consulta': consultas_serializers.data}, status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)

#
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def responder_consulta_panel_secretaria(request, id_consulta):
    try:
        # 
        data = request.data.copy()
        email_paciente = data['email']
        respuesta = data['respuesta']
        # Validamos que los datos no se encuentre vacíos.
        if not all([email_paciente, respuesta]):
            return Response({'error': 0}, status=status.HTTP_400_BAD_REQUEST)
        data["consulta_cerrada"] = 1
        usuario_registrado = CustomersUsers.objects.get(pk=request.user.id)
        # Buscamos el usuario en la tabla secretaria.
        usuario = SecretariaModel.objects.get(fk_user=usuario_registrado.id)
        nombre_usuario = usuario.primer_nombre + " " + usuario.segundo_nombre + " " +usuario.ap_paterno+" "+usuario.ap_materno
        data["nombre_usuario"] = nombre_usuario
        consulta = ConsultaModel.objects.get(pk=id_consulta)
        #
        consulta_serializers = ConsultaSerializers(consulta, data=data, partial=True)
        if consulta_serializers.is_valid():
            consulta_serializers.save()
            consultas = ConsultaModel.objects.filter(consulta_cerrada=0)
            consultas_serializers = ConsultaSerializers(consultas, many=True)
            correo_respuesta_consulta(id_consulta)
            return Response({'consulta': consultas_serializers.data}, status=status.HTTP_200_OK) 
        else:
            # Si la validación falla, devolvemos los errores
            return Response({'error': 2}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_consulta_cerrada_paciente(request):
    try:
        consultas = ConsultaModel.objects.filter(consulta_cerrada=1)
        consultas_serializers = ConsultaSerializers(consultas, many=True)
        return Response({'consulta': consultas_serializers.data}, status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def respuesta_consulta_cerrada_paciente(request, id_consulta):
    try:
        print("Ingresamos a la respuesta")
        consultas = ConsultaModel.objects.get(pk=id_consulta)
        respuesta = consultas.respuesta
        return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)

def correo_respuesta_consulta(id_consulta):
    try: 
        print("Ingresamos al Correo.....")
        # Creación del correo.
        subject = "Correo de Respuesta"
        pac = ConsultaModel.objects.get(pk=id_consulta)
        nombre_paciente = pac.primer_nombre + " " + pac.segundo_nombre + " " + pac.ap_paterno + " " + pac.ap_materno
        email = pac.email
        #
        chile_tz = pytz.timezone("America/Santiago")
        # Convertir fechas a Chile y formatear
        fecha_creacion_consulta = pac.fecha_creacion_consulta.astimezone(chile_tz).strftime("%d-%m-%Y")
        fecha_respuesta = pac.fecha_respuesta.astimezone(chile_tz).strftime("%d-%m-%Y")
        respuesta = pac.respuesta
        #
        dato = {
            'nombre_paciente': nombre_paciente,
            'email': email,
            'respuesta': respuesta,
            'fecha_consulta': fecha_creacion_consulta,
            'fecha_respuesta': fecha_respuesta,
        }
        # Crearemos el envío de correos.
        template = render_to_string("respuesta_consulta/correo_consulta.html", dato)
        emailSender = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ["matiasfamilycrew@gmail.com"],
        )
        # Ruta absoluta de la imagen
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'img_doc_44.jpg')
        if not os.path.exists(image_path):
            print("⚠️ La imagen no se encontró en la ruta:", image_path)
        else:
            # Adjuntar imagen como contenido embebido especificando el tipo MIME
            with open(image_path, 'rb') as img:
                mime_image = MIMEImage(img.read(), _subtype='jpeg')  # Especificar el subtipo
                mime_image.add_header('Content-ID', '<logo_clinica>')
                emailSender.attach(mime_image)
        # Formato del mensaje en HTML.
        emailSender.content_subtype = "html"
        emailSender.fail_silently = False
        emailSender.send()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 1}, status=400)