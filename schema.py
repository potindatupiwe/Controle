import graphene
from .models import *
from django.db.models import Count, Sum



class CountBensPorCategoria(graphene.ObjectType):
    count_bens = graphene.Int()
    id = graphene.ID()
    name = graphene.String()

class CountBensStatus(graphene.ObjectType):
    count_status = graphene.Int()
    name_status = graphene.String()

class CountMovePorMes(graphene.ObjectType):
    count_mes = graphene.Int()
    num_mes = graphene.Int()

class CountBensPorDpt(graphene.ObjectType):
    count_bens = graphene.Int()
    dpt = graphene.String()

class CountBensPorFornecedor(graphene.ObjectType):
    count_bens_fornecedor = graphene.Int()
    fornecedor = graphene.String()

class BensPorValor(graphene.ObjectType):
    ativo = graphene.String()
    valor = graphene.Decimal()

class Query(graphene.ObjectType):
    count_bens_por_cat = graphene.List(CountBensPorCategoria)
    count_bens_status = graphene.List(CountBensStatus)
    count_move_mes = graphene.List(CountMovePorMes)
    count_bens_dpt = graphene.List(CountBensPorDpt)
    count_fornecedor_bens = graphene.List(CountBensPorFornecedor)
    total_price = graphene.Int()
    bens_valor = graphene.List(BensPorValor)
    def resolve_count_bens_por_cat(self,info):
        categorias = Categorias.objects.annotate(count_bens = Count('bens'))
        return [CountBensPorCategoria(
            count_bens = cls.count_bens,
            id = cls.id,
            name = cls.nome
        )
        for cls in categorias
        ]
    def resolve_count_bens_status(self,info):
        status_list = ['EM_USO','MANUTENCAO','BAIXA']
        return [CountBensStatus(
            count_status = Bens.objects.filter(status = i).count(),
            name_status = i
        )for i in status_list
        
        ]
    def resolve_count_move_mes(self,info):
        return[CountMovePorMes(
            count_mes = Movimentacoes.objects.filter(data_hora__month = mes).count(),
            num_mes = mes
        )
        for mes in range(1,13)
        ]
    def resolve_count_bens_dpt(self,info):
        return[CountBensPorDpt(
            count_bens = Bens.objects.filter(departamento = dpt_int).count(),
            dpt = dpt_int
        )for dpt_int in Departamentos.objects.all()]
    def resolve_count_fornecedor_bens(self,info):
        return[CountBensPorFornecedor(
            count_bens_fornecedor = Bens.objects.filter(fornecedor = fornecedor_int).count(),
            fornecedor = fornecedor_int

        )
        for fornecedor_int in Fornecedores.objects.all()
        ]
    def resolve_total_price(self,info):
        return Bens.objects.aggregate(total = Sum('valor'))['total']
    def resolve_bens_valor(self, info):
        return[BensPorValor(
            ativo=ben,
            valor=ben.valor
        )for ben in Bens.objects.all().order_by('-valor')[:5]]
schema = graphene.Schema(query=Query)