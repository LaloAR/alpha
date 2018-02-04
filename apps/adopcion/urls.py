from django.urls import path
from apps.adopcion.views import index_adopcion, SolicitudList, SolicitudCreate, SolicitudUpdate, SolicitudDelete

app_name = 'adopcion'

urlpatterns = [
    path('index', index_adopcion),
    path('listar/',SolicitudList.as_view(), name='solicitud_listar'),
    path('nueva/',SolicitudCreate.as_view(), name='solicitud_crear'),
    path('editar/<int:pk>/',SolicitudUpdate.as_view(), name='solicitud_editar'),
    path('eliminar/<int:pk>/',SolicitudDelete.as_view(), name='solicitud_eliminar'),
]