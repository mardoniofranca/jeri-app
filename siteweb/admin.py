from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Perfil_Usuario
from .models import Projeto, Tarefa


class PerfilUsuarioInline(admin.StackedInline):
    model = Perfil_Usuario
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)

admin.site.register(Projeto)
admin.site.register(Tarefa)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)