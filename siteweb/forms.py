from django import forms
from django.contrib.auth.models import User
from .models import Projeto, Tarefa, Perfil_Usuario



class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['usuario', 'titulo', 'descricao', 'data_inicio', 'data_final', 'status_projeto']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do projeto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o projeto'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_final': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'status_projeto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'usuario': 'Responsável',
            'titulo': 'Título do Projeto',
            'descricao': 'Descrição',
            'data_inicio': 'Data de Início',
            'data_final': 'Data Final',
            'status_projeto': 'Status',
        }

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['usuario', 'cod_projeto', 'titulo', 'descricao', 'data_inicio', 'data_final', 'status_tarefa', 'tipo_tarefa']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'cod_projeto': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título da tarefa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva a tarefa'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_final': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'status_tarefa': forms.Select(attrs={'class': 'form-select'}),
            'tipo_tarefa': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'usuario': 'Responsável',
            'cod_projeto': 'Projeto',
            'titulo': 'Título da Tarefa',
            'descricao': 'Descrição',
            'data_inicio': 'Data de Início',
            'data_final': 'Data Final',
            'status_tarefa': 'Status',
            'tipo_tarefa': 'Tipo',
        }


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Deixe em branco para não alterar'}),
        label='Senha',
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Usuário (login)',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'is_active': 'Ativo',
        }


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Perfil_Usuario
        fields = ['fone', 'email', 'grupo', 'papel', 'perfil', 'bio']
        widgets = {
            'fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-select'}),
            'papel': forms.Select(attrs={'class': 'form-select'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descrição sobre o usuário'}),
        }
        labels = {
            'fone': 'Telefone',
            'email': 'E-mail de contato',
            'grupo': 'Grupo',
            'papel': 'Papel',
            'perfil': 'Perfil',
            'bio': 'Biografia',
        }