from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import datetime

from controle.forms_models import (
    AddItemForm,
    AddMoveForm,
    AddRelatorioDanoForm,
    AddRelatorioPerdaForm,
    AddUserForm,
    AddCategoriasForm,
    AddDepartamentosForm,
    AddFornecedoresForm,

)
from controle.forms import *
from controle.models import Bens, Movimentacoes, Categorias, Departamentos, Fornecedores, Relatorios

class FormsTests(TestCase):
    def setUp(self):
        # Criação de objetos necessários para preencher os campos de FK dos formulários
        self.categoria = Categorias.objects.create(nome="Test Cat", descricao="Descrição da categoria")
        self.depto = Departamentos.objects.create(nome="Test Dept", localizacao="Local")
        self.another_depto = Departamentos.objects.create(nome="Outro Dept", localizacao="Outro Local")
        self.fornecedor = Fornecedores.objects.create(nome_empresa="Test Fornec", dados_contato="Contato", categoria=self.categoria)
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

    # Testes para AddItemForm
    def test_add_item_form_valid(self):
        data = {
            "RFID": "1234567890123456789",
            "nome": "Item Test",
            "descricao": "Descrição do item",
            "data_aquisicao": timezone.now().date().isoformat(),
            "valor": "100.0",
            "status": "EM_USO",
            "categoria": self.categoria.id,
            "departamento": self.depto.id,
            "fornecedor": self.fornecedor.id,
        }
        form = AddItemForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_item_form_invalid_future_date(self):
        future_date = (timezone.now().date() + datetime.timedelta(days=1)).isoformat()
        data = {
            "RFID": "9876543210987654321",
            "nome": "Item Futuro",
            "descricao": "Descrição item futuro",
            "data_aquisicao": future_date,
            "valor": "150.0",
            "status": "EM_USO",
            "categoria": self.categoria.id,
            "departamento": self.depto.id,
            "fornecedor": self.fornecedor.id,
        }
        form = AddItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("data_aquisicao", form.errors)

   

    # Testes para AddMoveForm
    def test_add_move_form_valid(self):
        # Cria um item para movimentação cujo departamento atual é 'depto'
        item = Bens.objects.create(
            RFID="1111111111111111111",
            nome="Item Move",
            descricao="Item para movimentar",
            data_aquisicao=timezone.now().date(),
            valor=200.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.depto,
            fornecedor=self.fornecedor,
        )
        data = {
            "ativo": item.RFID,  # chave primária do bem
            "departamento_origem": self.depto.id,
            "departamento_destino": self.another_depto.id,  # departamento diferente
            "responsavel": self.user.id,
        }
        form = AddMoveForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_move_form_invalid_same_department(self):
        item = Bens.objects.create(
            RFID="2222222222222222222",
            nome="Item Move Invalid",
            descricao="Item para movimentar",
            data_aquisicao=timezone.now().date(),
            valor=300.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.depto,
            fornecedor=self.fornecedor,
        )
        data = {
            "ativo": item.RFID,
            "departamento_origem": self.depto.id,
            "departamento_destino": self.depto.id,  # mesmo departamento de origem e destino
            "responsavel": self.user.id,
        }
        form = AddMoveForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("departamento_destino", form.errors)

    # Testes para AddRelatorioDanoForm
    def test_add_relatorio_dano_form_valid(self):
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "titulo": "Relatório Dano",
            "conteudo": "Conteúdo de dano",
            "criado_por": self.user.id,
        }
        form = AddRelatorioDanoForm(data=data, files={"img": image})
        self.assertTrue(form.is_valid())

    def test_add_relatorio_dano_form_missing_fields(self):
        form = AddRelatorioDanoForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ["img", "titulo", "conteudo", "criado_por"]
        for field in required_fields:
            self.assertIn(field, form.errors)

    # Testes para AddRelatorioPerdaForm
    def test_add_relatorio_perda_form_valid(self):
        data = {
            "titulo": "Relatório Perda",
            "conteudo": "Conteúdo de perda",
            "criado_por": self.user.id,
        }
        form = AddRelatorioPerdaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_relatorio_perda_form_missing_fields(self):
        form = AddRelatorioPerdaForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ["titulo", "conteudo", "criado_por"]
        for field in required_fields:
            self.assertIn(field, form.errors)

    # Testes para AddUserForm
    def test_add_user_form_valid(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "new@example.com",
        }
        form = AddUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_user_form_invalid_email(self):
        data = {
            "username": "userinvalid",
            "password": "pass123",
            "email": "not-an-email",
        }
        form = AddUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    # Testes para AddCategoriasForm
    def test_add_categorias_form_valid(self):
        data = {
            "nome": "Categoria Form",
            "descricao": "Descrição da categoria"
        }
        form = AddCategoriasForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_categorias_form_missing_fields(self):
        form = AddCategoriasForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["nome", "descricao"]:
            self.assertIn(field, form.errors)

    # Testes para AddDepartamentosForm
    def test_add_departamentos_form_valid(self):
        data = {
            "nome": "Departamento Form",
            "localizacao": "Localização"
        }
        form = AddDepartamentosForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_departamentos_form_missing_fields(self):
        form = AddDepartamentosForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["nome", "localizacao"]:
            self.assertIn(field, form.errors)

    # Testes para AddFornecedoresForm
    def test_add_fornecedores_form_valid(self):
        data = {
            "nome_empresa": "Empresa Form",
            "dados_contato": "Contato Form",
            "categoria": self.categoria.id,
        }
        form = AddFornecedoresForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_fornecedores_form_missing_fields(self):
        form = AddFornecedoresForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["nome_empresa", "dados_contato", "categoria"]:
            self.assertIn(field, form.errors)

    # Testes para LoginForm
    def test_login_form_valid(self):
        # Cria um usuário para o login
        User.objects.create_user(username="loginuser", password="loginpass", email="login@example.com")
        data = {
            "username": "loginuser",
            "password": "loginpass",
            "email": "login@example.com"
        }
        # Note que AuthenticationForm geralmente espera um request; para testes, podemos passar None
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_fields(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["username", "password", "email"]:
            self.assertIn(field, form.errors)
