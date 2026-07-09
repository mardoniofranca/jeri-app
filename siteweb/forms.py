from django.forms import ModelForm
from .models import Cliente, Atendimento

class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[campo] = valor.upper()
        return cleaned_data


class FormAtendimento(ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'cpf_cliente' in self.fields:
            self.fields['cpf_cliente'].widget.attrs['readonly'] = True


    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[campo] = valor.upper()
        return cleaned_data