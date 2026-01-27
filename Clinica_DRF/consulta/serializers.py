from rest_framework import serializers
from.models import ConsultaModel
class ConsultaSerializers(serializers.ModelSerializer):
    class Meta:
        model = ConsultaModel
        fields = ['id','primer_nombre', 'segundo_nombre','ap_paterno', 'ap_materno', 'email', 'consulta', 'respuesta','consulta_cerrada', 'nombre_usuario', 'fecha_creacion_consulta', 'fecha_respuesta']