from django.contrib import admin
from django.urls import path
from siteweb.views import login_view, menu_view, cliente_view, atendimento_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('menu/', menu_view, name='menu'),
    path('cliente/', cliente_view, name='cliente'),
    path('atendimento/', atendimento_view, name='atendimento'),
]