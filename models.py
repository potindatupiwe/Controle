from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

class Categorias(models.Model):
    nome = models.CharField(max_length=255, unique=True, blank=False)
    descricao = models.TextField(blank=False)

    def __str__(self):
        return self.nome

class Departamentos(models.Model):
    nome = models.CharField(max_length=255, blank=False)
    localizacao = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.nome

class Fornecedores(models.Model):
    nome_empresa = models.CharField(max_length=255, unique=True, blank=False)
    dados_contato = models.TextField(blank=False)
    categoria = models.ForeignKey('Categorias', on_delete=models.CASCADE, related_name='fornecedores', null=True)
    def __str__(self):
        return self.nome_empresa

class Bens(models.Model):
    STATUS_CHOICES = [
        ('EM_USO', 'Em uso'),
        ('MANUTENCAO', 'Em manutenção'),
        ('BAIXA', 'Baixa'),
    ]
    RFID = models.CharField(max_length=19, primary_key=True)
    nome = models.CharField(max_length=255, blank=False, unique=True)
    descricao = models.TextField(blank=False)
    data_aquisicao = models.DateField()
    valor = models.DecimalField(max_digits=12, decimal_places=1, validators=[MinValueValidator(0.0)])

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_USO')
    categoria = models.ForeignKey(
        'Categorias', on_delete=models.CASCADE, related_name='bens'
    )
    departamento = models.ForeignKey(
        'Departamentos', on_delete=models.CASCADE, related_name='bens'
  )
    fornecedor = models.ForeignKey(
        'Fornecedores', on_delete=models.CASCADE, related_name='bens'
    )

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if self.data_aquisicao > timezone.now().date():
            raise ValidationError(
                {'data_aquisicao': 'A data de aquisição não pode ser no futuro.'}
            )

class Movimentacoes(models.Model):
    ativo = models.ForeignKey(
        'Bens', on_delete=models.CASCADE, related_name='movimentacoes'
    )
    departamento_origem = models.ForeignKey(
        'Departamentos', on_delete=models.CASCADE, related_name='movimentacoes_origem'
    )
    departamento_destino = models.ForeignKey(
        'Departamentos', on_delete=models.CASCADE, related_name='movimentacoes_destino'
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='movimentacoes_responsavel'
    )

    def __str__(self):
        return f"{self.ativo} - {self.data_hora}"

    def clean(self):
        super().clean()

        if self.departamento_origem == self.departamento_destino:
            raise ValidationError(
                {'departamento_destino': 'O departamento de destino deve ser diferente do de origem.'}
            )

        if self.ativo.status == 'BAIXA' or self.ativo.status == 'MANUTENCAO':
            raise ValidationError(
                {'ativo': 'Este bem não está em condições de ser movimentado.'}
            )

        if self.ativo.departamento_id != self.departamento_origem_id:
            raise ValidationError(
                {'departamento_origem': 'Este bem não está localizado no departamento de origem informado.'}
            )

class Relatorios(models.Model):
    TYPE_CHOICES = [
        ("PERDA", 'Perda'),
        ("DANO", 'Dano')
    ]
    img = models.FileField(null = True)
    titulo = models.CharField(max_length=255, blank=False)
    conteudo = models.TextField(blank=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='relatorios_criados'
    )
    modificado_por = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='relatorios_modificados', null=True, blank=True
    )
    types = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False)
    def __str__(self):
        return self.titulo