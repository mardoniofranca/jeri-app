from django.conf import settings

from django.db import models

from django.utils import timezone

from datetime import datetime

STATUS_PROJETO = [
    ('1', 'EM NEGOCIACAO'),
    ('2', 'AGUARDANDO INICIAR'),
    ('3', 'EM EXECUCAO'),
    ('4', 'CONCLUÍDO'),
    ('5', 'BLOQUEADO'),   
]

class Projeto(models.Model):
    id             = models.AutoField(primary_key=True)  # Adicione esta linha   
    data_cadastro  = models.DateTimeField(default=timezone.now)
    data_inicio    = models.DateTimeField(default=timezone.now)
    data_final     = models.DateTimeField(default=timezone.now)
    titulo         = models.CharField(max_length=300)
    descricao      = models.TextField(null=True)
    status_projeto = models.CharField(max_length=20,choices=STATUS_PROJETO,default='CE',null=True)
  
    def save(self, *args, **kwargs):
        for field in self._meta.concrete_fields:

            if isinstance(field, models.CharField):
                value = getattr(self, field.attname)
                if value is not None:
                    setattr(self, field.attname, str(value).upper())

            if isinstance(field, models.DateTimeField):
                value = getattr(self, field.attname)
                if isinstance(value, int):
                    raise ValueError(
                        f"{field.titulo} recebeu int ({value}). Esperado datetime."
                    )

        super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo


ESTADOS_BRASIL = [
    ('AC', 'ACRE'),
    ('AL', 'ALAGOAS'),
    ('AP', 'AMAPÁ'),
    ('AM', 'AMAZONAS'),
    ('BA', 'BAHIA'),
    ('CE', 'CEARÁ'),
    ('DF', 'DISTRITO FEDERAL'),
    ('ES', 'ESPÍRITO SANTO'),
    ('GO', 'GOIÁS'),
    ('MA', 'MARANHÃO'),
    ('MT', 'MATO GROSSO'),
    ('MS', 'MATO GROSSO DO SUL'),
    ('MG', 'MINAS GERAIS'),
    ('PA', 'PARÁ'),
    ('PB', 'PARAÍBA'),
    ('PR', 'PARANÁ'),
    ('PE', 'PERNAMBUCO'),
    ('PI', 'PIAUÍ'),
    ('RJ', 'RIO DE JANEIRO'),
    ('RN', 'RIO GRANDE DO NORTE'),
    ('RS', 'RIO GRANDE DO SUL'),
    ('RO', 'RONDÔNIA'),
    ('RR', 'RORAIMA'),
    ('SC', 'SANTA CATARINA'),
    ('SP', 'SÃO PAULO'),
    ('SE', 'SERGIPE'),
    ('TO', 'TOCANTINS'),
]


ASSUNTOS = [
    ('1', 'JURIDICO'),
    ('2', 'PESSOAL'),
    ('3', 'VELÓRIO'),
    ('4', 'TRANSPORTE'),
    ('5', 'OUTROS'),   
]

TIPO_ATIVO = [
    (1, 'ATIVO'),
    (2, 'INATIVO'),
]


class Cliente(models.Model):
    id            = models.AutoField(primary_key=True)  # Adicione esta linha   
    data_cadastro = models.DateTimeField(default=timezone.now)
    cpf           = models.CharField(max_length=11,null=True)
    nome          = models.CharField(max_length=200)
    lideranca     = models.CharField(max_length=200,null=True)
    endereco      = models.CharField(max_length=200)
    numero        = models.CharField(max_length=20,null=True)
    complemento   = models.CharField(max_length=200, blank=True, null=True)
    bairro        = models.CharField(max_length=100,null=True)
    cidade        = models.CharField(max_length=100,null=True)
    uf            = models.CharField(max_length=20,choices=ESTADOS_BRASIL,default='CE',null=True)
    fone          = models.CharField(max_length=50,null=True)
    email         = models.CharField(max_length=100,null=True)
    zona          = models.CharField(max_length=20,null=True)
    secao         = models.CharField(max_length=20,null=True)
    ativo         = models.IntegerField(choices=TIPO_ATIVO,default=1,null=True)
    data_nasc     = models.DateField(blank=True,null=True)
    observacao    = models.CharField(max_length=300, blank=True, null=True)
    cod_operador  = models.IntegerField(default=1)



    def save(self, *args, **kwargs):
        for field in self._meta.concrete_fields:

            if isinstance(field, models.CharField):
                value = getattr(self, field.attname)
                if value is not None:
                    setattr(self, field.attname, str(value).upper())

            if isinstance(field, models.DateTimeField):
                value = getattr(self, field.attname)
                if isinstance(value, int):
                    raise ValueError(
                        f"{field.name} recebeu int ({value}). Esperado datetime."
                    )

        super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.nome
    
class Atendimento(models.Model):
    protocolo        = models.AutoField(primary_key=True) 
    data_atendimento = models.DateTimeField(default=timezone.now)

    cpf_cliente      = models.CharField(max_length=11,default='99999999999',null=True)
    titulo           = models.CharField(max_length=200)
    assunto          = models.CharField(max_length=20,choices=ASSUNTOS,default='CE',null=True)
    observacao       = models.TextField(max_length=300, blank=True, null=True)
    cod_operador     = models.IntegerField(default=1)


    def save(self, *args, **kwargs):
        for field in self._meta.concrete_fields:

            if isinstance(field, models.CharField):
                value = getattr(self, field.attname)
                if value is not None:
                    setattr(self, field.attname, str(value).upper())

            if isinstance(field, models.DateTimeField):
                value = getattr(self, field.attname)
                if isinstance(value, int):
                    raise ValueError(
                        f"{field.name} recebeu int ({value}). Esperado datetime."
                    )

        super().save(*args, **kwargs)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.protocolo)
    
class Movimentacao(models.Model):
    cod_movimentacao    = models.AutoField(primary_key=True) 
    protocolo           = models.IntegerField() 
    data_movimentacao   = models.DateTimeField(default=timezone.now)
    descricao           = models.CharField(max_length=200)
    cod_operador        = models.IntegerField(default=1)

   

    def save(self, *args, **kwargs):
        for field in self._meta.concrete_fields:

            if isinstance(field, models.CharField):
                value = getattr(self, field.attname)
                if value is not None:
                    setattr(self, field.attname, str(value).upper())

            if isinstance(field, models.DateTimeField):
                value = getattr(self, field.attname)
                if isinstance(value, int):
                    raise ValueError(
                        f"{field.name} recebeu int ({value}). Esperado datetime."
                    )

        super().save(*args, **kwargs)

    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cod_movimentacao)
   
class Cliente_Hist(models.Model):
    OPERACAO_CHOICES = (
        ('ALTERACAO', 'Alteração'),
        ('EXCLUSAO', 'Exclusão'),
    )

    id = models.AutoField(primary_key=True)  # Adicione esta linha

    cliente_id_original     = models.IntegerField()
    nome                    = models.CharField(max_length=200)
    lideranca               = models.CharField(max_length=200,default='Não informado')

    fone                    = models.CharField(max_length=50)
    endereco                = models.CharField(max_length=200)
    complemento             = models.CharField(max_length=200, blank=True, null=True)

    numero                  = models.CharField(max_length=20)
    email                   = models.CharField(max_length=100)
    bairro                  = models.CharField(max_length=100)
    cidade                  = models.CharField(max_length=100)
    uf                      = models.CharField(max_length=20,choices=ESTADOS_BRASIL,default='CE',null=True)
    zona                    = models.CharField(max_length=20)
    secao                   = models.CharField(max_length=20)
    ativo                   = models.IntegerField(default=1)
    data_nasc               = models.DateField(blank=True,null=True)


    observacao              = models.CharField(max_length=300, blank=True, null=True)

    
    operacao                = models.CharField(max_length=10, choices=OPERACAO_CHOICES)
    data_hora               = models.DateTimeField(default=timezone.now)
    cod_operador            = models.IntegerField(default=1)


    def __str__(self):
        return f'{self.nome} - {self.operacao} - {self.data_hora}'