from django.contrib import admin
from django.urls import path
from siteweb.views import login_view, menu_view, novo_projeto_view, nova_tarefa_view,novo_usuario_view,detalhe_projeto_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('menu/', menu_view, name='menu'),
    path('projetos/novo/', novo_projeto_view, name='novo_projeto'),
    path('projetos/<int:pk>/editar/', novo_projeto_view, name='editar_projeto'),
    path('projetos/<int:pk>/detalhe/', detalhe_projeto_view, name='detalhe_projeto'),


    path('tarefa/novo/', nova_tarefa_view, name='nova_tarefa'),
    path('tarefa/<int:pk>/editar/', nova_tarefa_view, name='editar_tarefa'),
    path('usuarios/novo/', novo_usuario_view, name='novo_usuario'),
    path('usuarios/<int:pk>/editar/', novo_usuario_view, name='editar_usuario'),

]