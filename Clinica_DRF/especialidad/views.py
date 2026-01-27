from django.shortcuts import render
from django.core import serializers
from .models import Especialidad
from .serializers import EspecialidadSerializers
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
# Importamos el status.
from rest_framework import status
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
from rest_framework.permissions import IsAuthenticated, AllowAny
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

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def especialidad_doctor(request ):
    try:
        especialidad = Especialidad.objects.all().values()
        # Debemos serializarlos.
        serializer = EspecialidadSerializers(especialidad, many=True)
        print(serializer)
        if serializer.data:
            return Response({'especialidad':serializer.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
        else:
            return Response({'error':1},
                        # Específicamos el status.
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 1}, status=400)
    
#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def insertar_especialidad(request ):
    try:
        data = request.data.copy()
        nombre_especialidad = request.data["nombre_especialidad"]
        valor_especialidad = request.data["valor_especialidad"]
        if not nombre_especialidad:
            return Response({'error': 0}, status=status.HTTP_400_BAD_REQUEST)
        #
        if not valor_especialidad or int(valor_especialidad) <= 0:
            return Response({'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        #
        if Especialidad.objects.filter(nombre_especialidad=nombre_especialidad).exists():
            return Response({'error': 4}, status=status.HTTP_400_BAD_REQUEST)
        #
        dato_serializado = EspecialidadSerializers(data=request.data)
        if dato_serializado.is_valid():
            dato_serializado.save()
            arr = []
            especialidad = Especialidad.objects.all()
            for esp in especialidad:
                print(esp.nombre_especialidad)
                arr.append({
                    'id': esp.id,
                    'nombre_especialidad': esp.nombre_especialidad,
                    'valor_especialidad': esp.valor_especialidad,
                })
            # Debemos serializarlos.
            # serializer = EspecialidadSerializers(especialidad, many=True)
            # print(serializer.data) 
            return Response({'especialidad':arr},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
        else:
            #print(dato_serializado.errors)
            print("Errores de validación:", dato_serializado.errors)
            return Response({'error': 2, 'details': dato_serializado.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 3}, status=400)

#
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_especialidad(request, id):
    try:
        #print(request.data)
        data = request.data.copy()
        valor_especialidad = int(data["valor_especialidad"])
        nombre_especialidad = data["nombre_especialidad"]
        if not nombre_especialidad:
            return Response({'error': 0}, status=status.HTTP_400_BAD_REQUEST)
        print(valor_especialidad)
        if valor_especialidad == 0:
            return Response({'error':1}, status=status.HTTP_400_BAD_REQUEST)
        if not valor_especialidad:
            return Response({'error':3}, status=status.HTTP_400_BAD_REQUEST)
        #print(id)
        especialidad = Especialidad.objects.get(pk=id)
        #print(especialidad)
        serializado = EspecialidadSerializers(especialidad, data=request.data, partial=True)  
        # 
        if not serializado.is_valid():
            return Response({'error':2}, status=status.HTTP_400_BAD_REQUEST)
        # Guardar cambios
        serializado.save()
        # Enviamos todas las especialidades.
        especialidad_full = Especialidad.objects.all().values()
        serializado_full = EspecialidadSerializers(especialidad_full, many=True)
        # Debemos serializarlos.
        return Response({'especialidad':serializado_full.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 4}, status=400)

#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_especialidad(request, id):
    try:
        print(request.data)
        print(id)
        especialidad = Especialidad.objects.get(pk=id)
        especialidad.delete()
        #print(especialidad)
        serializado = EspecialidadSerializers(especialidad, data=request.data, partial=True)  
        # 
        # 3. Guardar cambios
        # serializado.save()
        # Enviamos todas las especialidades.
        especialidad_full = Especialidad.objects.all().values()
        serializado_full = EspecialidadSerializers(especialidad_full, many=True)
        # Debemos serializarlos.
        return Response({'especialidad':serializado_full.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 0}, status=400)

# Listar especialidad en el panel secretaria para la reserva de un paciente REGISTRADO.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_esp_panel_secretaria(request):
    try:
        especialidad = Especialidad.objects.all()
        # Debemos serializarlos.
        serializer = EspecialidadSerializers(especialidad, many=True)
        print(serializer)
        if serializer.data:
            return Response({'especialidad':serializer.data},
                        # Específicamos el status.
                        status=status.HTTP_200_OK)
        else:
            return Response({'error':0},
                        # Específicamos el status.
                        status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 0}, status=400)
