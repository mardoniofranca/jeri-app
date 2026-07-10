from django.contrib import admin
from django.urls import path
from siteweb.views import login_view, menu_view, novo_projeto_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('menu/', menu_view, name='menu'),
    path('projetos/novo/', novo_projeto_view, name='novo_projeto'),

]