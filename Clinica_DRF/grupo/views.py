from django.shortcuts import render
from .serializers import GroupSerializer
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
# El token de DRF.
from rest_framework.authtoken.models import Token
# Importamos el status.
from rest_framework import status
# 
from rest_framework.permissions import AllowAny
# 
import os
# Verificar si el usuario existe con este import, en caso de no, envía ERROR.
from django.shortcuts import get_object_or_404 
# En Django REST Framework (DRF), los decoradores authentication_classes y 
# permission_classes se utilizan para configurar y aplicar las políticas de autenticación y 
# permisos a las vistas de la API.
# permission_classes; Este decorador se utiliza para especificar las clases de permisos que se 
# deben usar para una vista específica. Los permisos determinan si un usuario tiene el derecho 
# de realizar una acción específica en la API. Algunas de las clases de permisos comunes en DRF incluyen:
# AllowAny: Permite acceso sin restricciones, tanto a usuarios autenticados como no autenticados.
# IsAuthenticated: Permite acceso solo a usuarios autenticados.
# IsAdminUser: Permite acceso solo a usuarios administradores (donde user.is_staff es True).
# IsAuthenticatedOrReadOnly: Permite a los usuarios autenticados realizar cualquier solicitud, 
# y a los usuarios no autenticados solo realizar solicitudes de lectura (GET, HEAD, OPTIONS)
from rest_framework.decorators import authentication_classes, permission_classes
# La clase IsAuthenticated es un permiso en DRF que verifica si el usuario que realiza la solicitud está autenticado.
# Cuando se establece IsAuthenticated como permiso para una vista, solo los usuarios autenticados podrán acceder a esa vista. Los usuarios no autenticados no tendrán permiso para realizar la solicitud
from rest_framework.permissions import IsAuthenticated
# Proceso de Autenticación
# Obtención del Token: Cuando un usuario se autentica, intercambia su nombre de usuario y 
# contraseña por un token único. Este token se genera y almacena en la base de datos asociado al usuario.
# Uso del Token: En solicitudes subsiguientes, el cliente debe incluir este token en el encabezado 
# Authorization de la solicitud HTTP. El formato típico es Authorization: Token <token_value>
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from datetime import datetime, date
# render_to_string; Sirve para enviar el HTML del correo.-------------------
from django.template.loader import render_to_string 
# Mensaje del E-mail.
from django.core.mail import EmailMessage
#
from django.conf import settings
# Acá podemos llamar a todos los valores del la tabla auth_group de DRF.
from django.contrib.auth.models import Group
# Create your views here.
# Create your views here.
@api_view(['POST'])
# Para este formulario NO se necesita token; @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def crear_grupo(request):
    try:
        #print(request.data)
        nombre = request.data["name"]
        if not nombre:
            return Response({'error': 'El nombre del grupo es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        # Verificar si el grupo ya existe
        if Group.objects.filter(name=nombre).exists():
            return Response({'error': 'El grupo ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        dato_serializado = GroupSerializer(data=request.data)
        if dato_serializado.is_valid():
            dato_serializado.save()
            grupo = Group.objects.all()
            # Serializar los datos
            serializer = GroupSerializer(grupo, many=True)
            # Obtener todos los usuarios del grupo
            #pacientes = grupo.user_set.all()
            print(serializer.data)
            return Response({'grupos': serializer.data}, status=status.HTTP_200_OK)
        else:
            #print(dato_serializado.errors)
            # Si la validación falla, devolvemos los errores
            return Response({'error': 2}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'grupo':1},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 0}, status=400)

#
@api_view(['GET'])
# Para este formulario NO se necesita token; @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def listar_grupo(request):
    try:
        grupo = Group.objects.all().values("id","name")
        #print(grupo)
        serializer = GroupSerializer(grupo, many=True)
        #print(serializer.data)
        if serializer.data:
            return Response({'grupos':serializer.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
        else:
            return Response({'error':1},
                        # Específicamos el status.
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 0}, status=400)

@api_view(['PUT'])
# Para este formulario NO se necesita token; @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def editar_grupo(request, id):
    try:
        grupo = Group.objects.get(pk=id)
        # Crear una instancia del serializer con el grupo existente y los nuevos datos
        serializer = GroupSerializer(grupo, data=request.data, partial=True)
        if serializer.is_valid():
            # Guardar los cambios
            serializer.save()
            grupo = Group.objects.all()
            # Serializar los datos
            serializer = GroupSerializer(grupo, many=True)
            return Response({'grupos': serializer.data, 'grupo': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':1}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'grupos':serializer.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 2}, status=400)
#
@api_view(['DELETE'])
# Para este formulario NO se necesita token; @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def eliminar_grupo(request, id):
    try:
        print(id)
        grupo = Group.objects.get(pk=id)
        # Crear una instancia del serializer con el grupo existente y los nuevos datos
        # Guardar los datos del grupo antes de eliminarlo
        serializer = GroupSerializer(grupo)
        grupo_data = serializer.data
        # Eliminar el grupo
        grupo.delete()
        grupo = Group.objects.all()
        # Serializar los datos
        serializer = GroupSerializer(grupo, many=True)
        # Obtener todos los usuarios del grupo
        #pacientes = grupo.user_set.all()
        print(serializer.data)
        return Response({'grupos':serializer.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 2}, status=400)