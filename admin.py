from django.contrib import admin
from .models import *

admin.site.register(Categorias)
admin.site.register(Departamentos)
admin.site.register(Fornecedores)
admin.site.register(Bens)
admin.site.register(Movimentacoes)
admin.site.register(Relatorios)

