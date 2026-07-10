from django.conf import settings

from django.db import models

from django.utils import timezone

from datetime import datetime

from django.db.models.signals import post_save

from django.dispatch import receiver



class Projeto(models.Model):

    STATUS_PROJETO = [
    ('1', 'EM NEGOCIACAO'),
    ('2', 'AGUARDANDO INICIAR'),
    ('3', 'EM EXECUCAO'),
    ('4', 'CONCLUÍDO'),
    ('5', 'BLOQUEADO'),   
    ]
    
    id             = models.AutoField(primary_key=True)  # Adicione esta linha   
    usuario        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projetos',
        verbose_name='Responsável',
        null=True,
        blank=True
    )

    data_cadastro  = models.DateTimeField(default=timezone.now)
    data_inicio    = models.DateTimeField(default=timezone.now)
    data_final     = models.DateTimeField(default=timezone.now)
    titulo         = models.CharField(max_length=300)
    descricao      = models.TextField(null=True)
    status_projeto = models.CharField(max_length=20,choices=STATUS_PROJETO,default='1',null=True)
  
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo


class Tarefa(models.Model):

    TIPO_TAREFA = [
    ('1', 'DOCUMENTAÇÃO'),
    ('2', 'CÓDIGO'),
    ('3', 'ANÁLISE'),
    ('4', 'PLANEJAMENTO'),
    ('5', 'GESTÃO'),   
    ]

    STATUS_TAREFA = [
    ('1', 'EM PLANEJAMENTO'),
    ('2', 'AGUARDANDO INICIAR'),
    ('3', 'EM EXECUCAO'),
    ('4', 'CONCLUÍDO'),
    ('5', 'BLOQUEADO'),   
    ]
    
    id             = models.AutoField(primary_key=True)  # Adicione esta linha   
    usuario        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tarefas',
        verbose_name='Responsável',
        null=True,
        blank=True
    )

    cod_projeto  = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='projetos',
        verbose_name='Projeto',
        null=True,
        blank=True
    )

    data_cadastro  = models.DateTimeField(default=timezone.now)
    data_inicio    = models.DateTimeField(default=timezone.now)
    data_final     = models.DateTimeField(default=timezone.now)
    titulo         = models.CharField(max_length=300)
    descricao      = models.TextField(null=True)
    status_tarefa  = models.CharField(max_length=20,choices=STATUS_TAREFA,default='1',null=True)
    tipo_tarefa    = models.CharField(max_length=20,choices=TIPO_TAREFA,default='1',null=True)
  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo



class Perfil_Usuario(models.Model):

    PERFIL = [
    ('1', 'GESTOR'),
    ('2', 'EXECUTOR'),
    ('3', 'GERAL'),  
    ]

    GRUPO = [
    ('1', 'SUPER'),
    ('2', 'ADM'),
    ('3', 'USER'),
    ('4', 'AUDITOR'),
    ('5', 'CONSULTA'),   
    ]

    PAPEL = [
    ('1', 'DIRETOR'),
    ('2', 'COORDENADOR'),
    ('3', 'GESTOR'),
    ('4', 'PROGRAMADOR'),
    ('5', 'ANALISTA'),   
    ('6', 'TESTE'),  
    ('7', 'SUPORTE'), 
    ]
    usuario     = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    fone        = models.CharField(max_length=30, blank=True, null=True)
    email       = models.CharField(max_length=30, blank=True, null=True)
    grupo       = models.CharField(max_length=20,choices=GRUPO,default='1',null=True)
    papel       = models.CharField(max_length=20,choices=PAPEL,default='1',null=True)
    perfil      = models.CharField(max_length=20,choices=PERFIL,default='1',null=True)
    bio         = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


# Cria o Perfil_Usuario automaticamente quando um novo User é criado
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil_Usuario.objects.create(usuario=instance)