from django.shortcuts import render
# Importamos la librería de OpenIa.
from openai import OpenAI
# Llamamos la API_KEY de OpenIA de una manera más segura.
from decouple import config
# Permisos para peticion de la API.
from rest_framework.decorators import authentication_classes, permission_classes, api_view
# Cuando se establece IsAuthenticated como permiso para una vista, solo los usuarios autenticados podrán acceder a esa vista. Los usuarios no autenticados no tendrán permiso para realizar la solicitud
from rest_framework.permissions import IsAuthenticated, AllowAny
# Importamos el status.
from rest_framework import status
#
from rest_framework.response import Response
# HHTP RESPONSE.
from django.http import JsonResponse, HttpResponse
#

@api_view(['POST'])
@permission_classes([AllowAny]) 
def obtener_respuesta(request):
    try:
        # Recibimos la pregunta del usuario.
        pregunta = request.data.get('pregunta', '').strip()
        # Si no existe pregunta, enviamos el error.
        if not pregunta:
            return Response({'error': 'Pregunta vacía'}, status=status.HTTP_400_BAD_REQUEST)

        # Simulamos una respuesta porque no tenemos créditos en OpenIA.
        respuesta_demo = f"📎 Modo demo activado. Recibí tu pregunta: “{pregunta}”, pero no tengo acceso al modelo ahora mismo."

        # Alternativa: revisa si estás en entorno demo
        # En caso de Activar OpenIA, solo se debe reestablecer al código de abajo. 
        if True:  # ← Cambia esto a una variable de configuración si deseas
            return Response({'respuesta': respuesta_demo}, status=status.HTTP_200_OK)

        # Funcionando.
        # Código real (cuando vuelvas a tener acceso)
        # client = OpenAI(api_key=config('OPENAI_API_KEY'))
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "Eres un asistente útil."},
        #         {"role": "user", "content": pregunta}
        #     ]
        # )
        # respuesta_real = response.choices[0].message.content
        # return Response({'respuesta': respuesta_real}, status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Response({'error': 'Hubo un problema al procesar tu solicitud.'}, status=status.HTTP_400_BAD_REQUEST)