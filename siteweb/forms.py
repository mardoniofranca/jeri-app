from django import forms
from .models import Projeto

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