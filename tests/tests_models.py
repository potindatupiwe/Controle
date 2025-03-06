from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

from controle.models import (
    Categorias,
    Departamentos,
    Fornecedores,
    Bens,
    Movimentacoes,
    Relatorios,
)

# Testes para o model Categorias
class CategoriasModelTest(TestCase):
    def test_str_method(self):
        categoria = Categorias.objects.create(nome="Test Categoria", descricao="Descrição da categoria")
        self.assertEqual(str(categoria), "Test Categoria")

# Testes para o model Departamentos
class DepartamentosModelTest(TestCase):
    def test_str_method(self):
        depto = Departamentos.objects.create(nome="Depto Teste", localizacao="Local X")
        self.assertEqual(str(depto), "Depto Teste")

# Testes para o model Fornecedores
class FornecedoresModelTest(TestCase):
    def setUp(self):
        self.categoria = Categorias.objects.create(nome="Cat Fornecedor", descricao="Descrição")
    def test_str_method(self):
        fornecedor = Fornecedores.objects.create(
            nome_empresa="Empresa XYZ", 
            dados_contato="Contato XYZ", 
            categoria=self.categoria
        )
        self.assertEqual(str(fornecedor), "Empresa XYZ")

# Testes para o model Bens
class BensModelTest(TestCase):
    def setUp(self):
        self.categoria = Categorias.objects.create(nome="Cat Bens", descricao="Descrição")
        self.depto = Departamentos.objects.create(nome="Depto Bens", localizacao="Local B")
        self.fornecedor = Fornecedores.objects.create(
            nome_empresa="Fornecedor ABC", 
            dados_contato="Contato ABC", 
            categoria=self.categoria
        )
    def test_str_method(self):
        bem = Bens.objects.create(
            RFID="1111111111111111111",
            nome="Bem Teste",
            descricao="Descrição do bem",
            data_aquisicao=timezone.now().date(),
            valor=100.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.depto,
            fornecedor=self.fornecedor,
        )
        self.assertEqual(str(bem), "Bem Teste")
    def test_future_date_validation(self):
        future_date = timezone.now().date() + datetime.timedelta(days=1)
        bem = Bens(
            RFID="2222222222222222222",
            nome="Bem Futuro",
            descricao="Descrição",
            data_aquisicao=future_date,
            valor=100.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.depto,
            fornecedor=self.fornecedor,
        )
        with self.assertRaises(ValidationError) as context:
            bem.full_clean()  # Chama os validadores, incluindo o clean()
        self.assertIn("A data de aquisição não pode ser no futuro.", str(context.exception))

# Testes para o model Movimentacoes
class MovimentacoesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="movuser", password="senha123")
        self.categoria = Categorias.objects.create(nome="Cat Mov", descricao="Descrição")
        self.depto_origem = Departamentos.objects.create(nome="Origem", localizacao="Local Origem")
        self.depto_destino = Departamentos.objects.create(nome="Destino", localizacao="Local Destino")
        self.fornecedor = Fornecedores.objects.create(
            nome_empresa="Fornecedor Mov", 
            dados_contato="Contato Mov", 
            categoria=self.categoria
        )
        self.bem = Bens.objects.create(
            RFID="3333333333333333333",
            nome="Bem Movimentável",
            descricao="Descrição do bem",
            data_aquisicao=timezone.now().date(),
            valor=200.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.depto_origem,
            fornecedor=self.fornecedor,
        )
    def test_str_method(self):
        mov = Movimentacoes.objects.create(
            ativo=self.bem,
            departamento_origem=self.depto_origem,
            departamento_destino=self.depto_destino,
            responsavel=self.user,
        )
        # Verifica se o __str__ contém o nome do bem e a data/hora
        self.assertIn("Bem Movimentável", str(mov))
        self.assertIn(str(mov.data_hora.date()), str(mov))
    def test_same_department_validation(self):
        mov = Movimentacoes(
            ativo=self.bem,
            departamento_origem=self.depto_origem,
            departamento_destino=self.depto_origem,  # mesmo departamento
            responsavel=self.user,
        )
        with self.assertRaises(ValidationError) as context:
            mov.full_clean()
        self.assertIn("O departamento de destino deve ser diferente do de origem.", str(context.exception))
    def test_inactive_bem_validation(self):
        # Modifica o status do bem para um que não pode ser movimentado
        self.bem.status = "BAIXA"
        self.bem.save()
        mov = Movimentacoes(
            ativo=self.bem,
            departamento_origem=self.depto_origem,
            departamento_destino=self.depto_destino,
            responsavel=self.user,
        )
        with self.assertRaises(ValidationError) as context:
            mov.full_clean()
        self.assertIn("Este bem não está em condições de ser movimentado.", str(context.exception))
    def test_wrong_departamento_origem_validation(self):
        # O bem está em depto_origem, mas passamos um outro departamento na origem
        depto_errado = Departamentos.objects.create(nome="Errado", localizacao="Local Errado")
        mov = Movimentacoes(
            ativo=self.bem,
            departamento_origem=depto_errado,  # incorreto
            departamento_destino=self.depto_destino,
            responsavel=self.user,
        )
        with self.assertRaises(ValidationError) as context:
            mov.full_clean()
        self.assertIn("Este bem não está localizado no departamento de origem informado.", str(context.exception))

# Testes para o model Relatorios
class RelatoriosModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reluser", password="senha123")
    def test_str_method(self):
        rel = Relatorios.objects.create(
            titulo="Relatório Modelo",
            conteudo="Conteúdo do relatório",
            criado_por=self.user,
            types="PERDA"
        )
        self.assertEqual(str(rel), "Relatório Modelo")
