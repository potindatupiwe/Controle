from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

from controle.models import Bens, Relatorios, Categorias, Departamentos, Fornecedores

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Cria usuário e grupos
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_group = Group.objects.create(name='Administradores')
        self.func_group = Group.objects.create(name='Funcionários')
        self.gerencia_group = Group.objects.create(name='Gerencia')
        self.user.groups.add(self.gerencia_group)
        self.client.login(username='testuser', password='12345')
        
        # Cria objetos necessários para os testes
        self.categoria = Categorias.objects.create(nome="Informatica", descricao="Equipamentos de TI")
        self.departamento_origem = Departamentos.objects.create(nome="TI", localizacao="Primeiro andar")
        self.departamento_destino = Departamentos.objects.create(nome="RH", localizacao="Segundo andar")
        self.fornecedor = Fornecedores.objects.create(
            nome_empresa="Fornecedor 1", 
            dados_contato="Contato", 
            categoria=self.categoria
        )
        # Lembre que o campo RFID é a chave primária
        self.bens = Bens.objects.create(
            RFID="1234567890123456789",
            nome="Computador",
            descricao="Computador Dell",
            data_aquisicao=timezone.now().date(),
            valor=1000.0,
            status="EM_USO",
            categoria=self.categoria,
            departamento=self.departamento_origem,
            fornecedor=self.fornecedor
        )
        self.relatorio = Relatorios.objects.create(
            titulo="Relatório Teste",
            conteudo="Conteúdo Teste",
            criado_por=self.user,
            types="PERDA"
        )
        # Notamos que as views de movimentações e os CRUD administrativos não possuem _urls_ definidas;
        # portanto, os testes para essas views foram omitidos.

    # ––– Testes para as views de Bens –––

   

    def test_add_bens_view(self):
        data = {
            "RFID": "9876543210987654321",
            "nome": "Mesa",
            "descricao": "Mesa de escritório",
            "data_aquisicao": timezone.now().date().isoformat(),
            "valor": "500.0",
            "status": "EM_USO",
            "categoria": self.categoria.id,
            "departamento": self.departamento_origem.id,
            "fornecedor": self.fornecedor.id,
        }
        response = self.client.post(reverse('add_bens'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bens.objects.filter(nome="Mesa").exists())

   

   

    def test_update_bens_view(self):
        data = {
            "RFID": self.bens.RFID,
            "nome": "Monitor",
            "descricao": "Monitor LED",
            "data_aquisicao": self.bens.data_aquisicao.isoformat(),
            "valor": "1200.0",
            "status": "EM_USO",
            "categoria": self.categoria.id,
            "departamento": self.departamento_origem.id,
            "fornecedor": self.fornecedor.id,
        }
        response = self.client.post(reverse('update_bens', args=[self.bens.RFID]), data)
        self.assertEqual(response.status_code, 302)
        self.bens.refresh_from_db()
        self.assertEqual(self.bens.nome, "Monitor")

    # ––– Testes para as views de Relatórios –––

    def test_view_relatorio_list(self):
        response = self.client.get(reverse('show_relatorio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gerencia/show_relatorio.html')
        self.assertContains(response, "Relatório Teste")

    def test_add_relatorio_perda_view(self):
        data = {
            "titulo": "Perda",
            "conteudo": "Item perdido",
            "criado_por": self.user.id
        }
        response = self.client.post(reverse('add_relatorio_perda'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Relatorios.objects.filter(titulo="Perda").exists())

    def test_add_relatorio_dano_view(self):
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "img": image,
            "titulo": "Dano",
            "conteudo": "Item danificado",
            "criado_por": self.user.id
        }
        response = self.client.post(reverse('add_relatorio_dano'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Relatorios.objects.filter(titulo="Dano").exists())

   
   
    def test_view_relatorio_detail(self):
        response = self.client.get(reverse('show_detail_relatorio', args=[self.relatorio.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gerencia/show_detail_relatorio.html')

    # ––– Testes para as views de Usuários –––

    def test_view_user_list(self):
        response = self.client.get(reverse('show_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gerencia/show_user.html')
        self.assertContains(response, "testuser")

    def test_view_detail_user(self):
        response = self.client.get(reverse('show_detail_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gerencia/show_detail_user.html')

    def test_add_user_view(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "new@example.com",
            "group": "Gerencia"
        }
        response = self.client.post(reverse('add_user'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_user_view(self):
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "group": "Gerencia"
        }
        response = self.client.post(reverse('update_user', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated@example.com")

    def test_delete_user_view(self):
        # Como o usuário criado em setUp está relacionado a Movimentações e Relatórios,
        # criamos um usuário temporário sem relações para testar a exclusão.
        temp_user = User.objects.create_user(username='tempuser', password='temp123')
        response = self.client.post(reverse('delete_user', args=[temp_user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=temp_user.id).exists())

    # ––– Testes para login/logout –––

    def test_custom_login_view(self):
        # Efetua logout para testar a página de login
        self.client.logout()
        data = {"username": "testuser", "password": "12345", "email": "test@example.com"}
        response = self.client.post(reverse('login'), data)
        # Em muitas configurações o login redireciona (302) após autenticação
        self.assertIn(response.status_code, [200, 302])
        # Verifica se o usuário está autenticado acessando uma view protegida
        response2 = self.client.get(reverse('list_bens'), follow=True)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.context['user'].is_authenticated)

    def test_custom_logout_view(self):
        # Se a LogoutView não aceitar GET, utiliza POST
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        response2 = self.client.get(reverse('login'), follow=True)
        self.assertFalse(response2.context['user'].is_authenticated)
